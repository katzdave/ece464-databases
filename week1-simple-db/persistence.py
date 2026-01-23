"""
Persistence layer for the in-memory database.
Implements record-based file storage with Write-Ahead Logging (WAL).
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class OperationType(Enum):
    """Types of operations for the WAL."""
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    CREATE_TABLE = "CREATE_TABLE"
    DROP_TABLE = "DROP_TABLE"


class StorageEngine:
    """
    Manages on-disk storage for database tables.
    
    File Structure:
        db_name/
            schema/
                table_name.schema.json      # Table schema definition
            data/
                table_name.records          # One JSON record per line
            wal/
                transaction.log             # Write-Ahead Log for durability
    """
    
    def __init__(self, db_name: str, base_path: str = "./data"):
        self.db_name = db_name
        self.base_path = Path(base_path)
        self.db_path = self.base_path / db_name
        
        # Create directory structure
        self.schema_path = self.db_path / "schema"
        self.data_path = self.db_path / "data"
        self.wal_path = self.db_path / "wal"
        
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.schema_path.mkdir(parents=True, exist_ok=True)
        self.data_path.mkdir(parents=True, exist_ok=True)
        self.wal_path.mkdir(parents=True, exist_ok=True)
    
    def _get_schema_file(self, table_name: str) -> Path:
        """Get the path to a table's schema file."""
        return self.schema_path / f"{table_name}.schema.json"
    
    def _get_data_file(self, table_name: str) -> Path:
        """Get the path to a table's data file."""
        return self.data_path / f"{table_name}.records"
    
    def _get_wal_file(self) -> Path:
        """Get the path to the Write-Ahead Log."""
        return self.wal_path / "transaction.log"
    
    def _write_wal_entry(self, operation: OperationType, table_name: str, 
                         record: Optional[Dict[str, Any]] = None,
                         old_record: Optional[Dict[str, Any]] = None):
        """Write an operation to the Write-Ahead Log."""
        wal_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation.value,
            "table": table_name,
            "record": record,
            "old_record": old_record
        }
        
        wal_file = self._get_wal_file()
        with open(wal_file, 'a') as f:
            f.write(json.dumps(wal_entry) + '\n')
    
    def save_schema(self, table_name: str, schema: Dict[str, Any]):
        """Save table schema to disk."""
        schema_file = self._get_schema_file(table_name)
        
        # Convert Field objects to serializable dict
        serializable_schema = {}
        for field_name, field_obj in schema.items():
            serializable_schema[field_name] = {
                "type": field_obj.field_type.__name__,
                "primary_key": field_obj.primary_key,
                "nullable": field_obj.nullable,
                "unique": field_obj.unique
            }
        
        with open(schema_file, 'w') as f:
            json.dump({
                "table_name": table_name,
                "schema": serializable_schema,
                "created_at": datetime.now().isoformat()
            }, f, indent=2)
        
        self._write_wal_entry(OperationType.CREATE_TABLE, table_name)
    
    def load_schema(self, table_name: str) -> Optional[Dict[str, Any]]:
        """Load table schema from disk."""
        schema_file = self._get_schema_file(table_name)
        
        if not schema_file.exists():
            return None
        
        with open(schema_file, 'r') as f:
            return json.load(f)
    
    def save_records(self, table_name: str, records: List[Dict[str, Any]]):
        """
        Save all records to disk (overwrites existing file).
        Uses JSON Lines format - one record per line.
        """
        data_file = self._get_data_file(table_name)
        
        with open(data_file, 'w') as f:
            for record in records:
                f.write(json.dumps(record) + '\n')
    
    def load_records(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Load all records from disk.
        Reads JSON Lines format.
        """
        data_file = self._get_data_file(table_name)
        
        if not data_file.exists():
            return []
        
        records = []
        with open(data_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:  # Skip empty lines
                    records.append(json.loads(line))
        
        return records
    
    def append_record(self, table_name: str, record: Dict[str, Any]):
        """
        Append a single record to the data file.
        More efficient than rewriting the entire file.
        """
        data_file = self._get_data_file(table_name)
        
        # Write to WAL first
        self._write_wal_entry(OperationType.INSERT, table_name, record)
        
        # Then append to data file
        with open(data_file, 'a') as f:
            f.write(json.dumps(record) + '\n')
    
    def update_records(self, table_name: str, records: List[Dict[str, Any]], 
                       updated_records: List[Dict[str, Any]]):
        """
        Update records (requires rewriting file).
        Logs changes to WAL.
        """
        # Log updates to WAL
        for old_rec, new_rec in zip(records, updated_records):
            self._write_wal_entry(OperationType.UPDATE, table_name, new_rec, old_rec)
        
        # Note: The caller should save all records after updates
    
    def delete_records(self, table_name: str, records: List[Dict[str, Any]]):
        """
        Delete records (requires rewriting file).
        Logs deletions to WAL.
        """
        # Log deletions to WAL
        for record in records:
            self._write_wal_entry(OperationType.DELETE, table_name, old_record=record)
        
        # Note: The caller should save all records after deletions
    
    def drop_table(self, table_name: str):
        """Delete all files for a table."""
        schema_file = self._get_schema_file(table_name)
        data_file = self._get_data_file(table_name)
        
        self._write_wal_entry(OperationType.DROP_TABLE, table_name)
        
        if schema_file.exists():
            schema_file.unlink()
        if data_file.exists():
            data_file.unlink()
    
    def list_tables(self) -> List[str]:
        """List all tables by scanning schema files."""
        tables = []
        if self.schema_path.exists():
            for schema_file in self.schema_path.glob("*.schema.json"):
                table_name = schema_file.stem.replace('.schema', '')
                tables.append(table_name)
        return tables
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the database on disk."""
        stats = {
            "db_name": self.db_name,
            "db_path": str(self.db_path),
            "tables": {},
            "total_size_bytes": 0
        }
        
        for table_name in self.list_tables():
            data_file = self._get_data_file(table_name)
            schema_file = self._get_schema_file(table_name)
            
            table_size = 0
            record_count = 0
            
            if data_file.exists():
                table_size = data_file.stat().st_size
                record_count = sum(1 for _ in open(data_file))
            
            stats["tables"][table_name] = {
                "records": record_count,
                "size_bytes": table_size,
                "data_file": str(data_file),
                "schema_file": str(schema_file)
            }
            
            stats["total_size_bytes"] += table_size
        
        # Add WAL info
        wal_file = self._get_wal_file()
        if wal_file.exists():
            stats["wal_size_bytes"] = wal_file.stat().st_size
            stats["wal_entries"] = sum(1 for _ in open(wal_file))
        else:
            stats["wal_size_bytes"] = 0
            stats["wal_entries"] = 0
        
        return stats
    
    def checkpoint(self):
        """
        Checkpoint the WAL - clear it after confirming all data is saved.
        In a production system, this would be more sophisticated.
        """
        wal_file = self._get_wal_file()
        if wal_file.exists():
            # Archive the old WAL
            archive_name = f"transaction.{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            archive_path = self.wal_path / archive_name
            wal_file.rename(archive_path)
            
            # Create new empty WAL
            wal_file.touch()
    
    def replay_wal(self) -> List[Dict[str, Any]]:
        """
        Read the WAL entries (useful for recovery).
        Returns list of operations.
        """
        wal_file = self._get_wal_file()
        
        if not wal_file.exists():
            return []
        
        operations = []
        with open(wal_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    operations.append(json.loads(line))
        
        return operations
    
    def compact(self, table_name: str):
        """
        Compact a table's data file by rewriting it.
        Useful after many deletes/updates.
        """
        records = self.load_records(table_name)
        self.save_records(table_name, records)
    
    def export_table_to_json(self, table_name: str, output_file: str):
        """Export a table to a standard JSON file."""
        records = self.load_records(table_name)
        with open(output_file, 'w') as f:
            json.dump({
                "table": table_name,
                "records": records,
                "count": len(records),
                "exported_at": datetime.now().isoformat()
            }, f, indent=2)
    
    def import_table_from_json(self, table_name: str, input_file: str) -> int:
        """Import records from a JSON file."""
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        records = data.get("records", [])
        self.save_records(table_name, records)
        
        return len(records)
