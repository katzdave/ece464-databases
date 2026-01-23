"""
Simple In-Memory Database System
Supports table definition via decorators, CRUD operations, and flexible querying.
"""

from typing import Any, Dict, List, Optional, Callable, Type, get_type_hints
from dataclasses import dataclass, field, fields
from copy import deepcopy
import inspect


class Field:
    """Represents a field in a table with type and constraints."""
    def __init__(self, field_type: Type, primary_key: bool = False, nullable: bool = True, unique: bool = False):
        self.field_type = field_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.unique = unique
    
    def validate(self, value: Any) -> bool:
        """Validate a value against field constraints."""
        if value is None:
            return self.nullable
        
        # Type checking
        if not isinstance(value, self.field_type):
            try:
                # Try to coerce the type
                self.field_type(value)
            except (ValueError, TypeError):
                return False
        
        return True


class Table:
    """Represents a table in the database with schema and data."""
    def __init__(self, name: str, schema: Dict[str, Field]):
        self.name = name
        self.schema = schema
        self.data: List[Dict[str, Any]] = []
        self.primary_key_field = next((name for name, field in schema.items() if field.primary_key), None)
        self._next_id = 1
    
    def _validate_record(self, record: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate a record against the table schema."""
        # Check all schema fields are present
        for field_name, field_def in self.schema.items():
            if field_name not in record:
                if not field_def.nullable and field_name != self.primary_key_field:
                    return False, f"Missing required field: {field_name}"
                record[field_name] = None
        
        # Validate each field
        for field_name, value in record.items():
            if field_name not in self.schema:
                return False, f"Unknown field: {field_name}"
            
            field_def = self.schema[field_name]
            if not field_def.validate(value):
                return False, f"Invalid value for field {field_name}: {value}"
            
            # Check unique constraint
            if field_def.unique and value is not None:
                for existing in self.data:
                    if existing.get(field_name) == value:
                        return False, f"Duplicate value for unique field {field_name}: {value}"
        
        return True, None
    
    def insert(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a record into the table."""
        record = deepcopy(record)
        
        # Auto-generate primary key if needed
        if self.primary_key_field and self.primary_key_field not in record:
            record[self.primary_key_field] = self._next_id
            self._next_id += 1
        
        # Validate record
        valid, error = self._validate_record(record)
        if not valid:
            raise ValueError(f"Invalid record: {error}")
        
        self.data.append(record)
        return record
    
    def select(self, where: Optional[Callable[[Dict[str, Any]], bool]] = None, 
               order_by: Optional[str] = None,
               limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Query records from the table."""
        results = self.data if where is None else [r for r in self.data if where(r)]
        
        if order_by:
            reverse = False
            if order_by.startswith('-'):
                reverse = True
                order_by = order_by[1:]
            results = sorted(results, key=lambda x: x.get(order_by, ''), reverse=reverse)
        
        if limit is not None:
            results = results[:limit]
        
        return deepcopy(results)
    
    def update(self, where: Callable[[Dict[str, Any]], bool], 
               updates: Dict[str, Any]) -> int:
        """Update records matching the where clause."""
        count = 0
        for record in self.data:
            if where(record):
                # Validate updates
                test_record = {**record, **updates}
                # Temporarily remove from data for unique checks
                self.data.remove(record)
                valid, error = self._validate_record(test_record)
                self.data.append(record)  # Add back
                
                if not valid:
                    raise ValueError(f"Invalid update: {error}")
                
                record.update(updates)
                count += 1
        
        return count
    
    def delete(self, where: Callable[[Dict[str, Any]], bool]) -> int:
        """Delete records matching the where clause."""
        to_delete = [r for r in self.data if where(r)]
        for record in to_delete:
            self.data.remove(record)
        return len(to_delete)
    
    def count(self) -> int:
        """Return the number of records in the table."""
        return len(self.data)


class Database:
    """Main database class managing multiple tables."""
    def __init__(self, name: str = "default", persist: bool = False, base_path: str = "./data"):
        self.name = name
        self.tables: Dict[str, Table] = {}
        self.persist = persist
        self.storage = None
        
        if persist:
            from persistence import StorageEngine
            self.storage = StorageEngine(name, base_path)
    
    def create_table(self, name: str, schema: Dict[str, Field]) -> Table:
        """Create a new table in the database."""
        if name in self.tables:
            raise ValueError(f"Table {name} already exists")
        
        table = Table(name, schema)
        self.tables[name] = table
        
        # Save schema to disk if persistence is enabled
        if self.persist and self.storage:
            self.storage.save_schema(name, schema)
        
        return table
    
    def get_table(self, name: str) -> Table:
        """Get a table by name."""
        if name not in self.tables:
            raise ValueError(f"Table {name} does not exist")
        return self.tables[name]
    
    def drop_table(self, name: str) -> None:
        """Drop a table from the database."""
        if name in self.tables:
            del self.tables[name]
            
            # Remove from disk if persistence is enabled
            if self.persist and self.storage:
                self.storage.drop_table(name)
    
    def list_tables(self) -> List[str]:
        """List all table names in the database."""
        return list(self.tables.keys())
    
    def save(self):
        """Save all tables to disk."""
        if not self.persist or not self.storage:
            raise RuntimeError("Database was not initialized with persistence enabled")
        
        for table_name, table in self.tables.items():
            self.storage.save_records(table_name, table.data)
        
        return len(self.tables)
    
    def load(self):
        """Load all tables from disk."""
        if not self.persist or not self.storage:
            raise RuntimeError("Database was not initialized with persistence enabled")
        
        # Discover tables from schema files
        table_names = self.storage.list_tables()
        
        for table_name in table_names:
            # Load schema
            schema_data = self.storage.load_schema(table_name)
            if not schema_data:
                continue
            
            # Reconstruct schema
            schema = {}
            for field_name, field_info in schema_data["schema"].items():
                # Convert type name back to type
                type_map = {
                    "int": int,
                    "str": str,
                    "float": float,
                    "bool": bool
                }
                field_type = type_map.get(field_info["type"], str)
                
                schema[field_name] = Field(
                    field_type=field_type,
                    primary_key=field_info["primary_key"],
                    nullable=field_info["nullable"],
                    unique=field_info["unique"]
                )
            
            # Create table
            table = Table(table_name, schema)
            
            # Load records
            records = self.storage.load_records(table_name)
            table.data = records
            
            # Update next_id based on existing records
            if table.primary_key_field:
                existing_ids = [r.get(table.primary_key_field, 0) for r in records]
                if existing_ids:
                    table._next_id = max(existing_ids) + 1
            
            self.tables[table_name] = table
        
        return len(self.tables)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        stats = {
            "name": self.name,
            "persist": self.persist,
            "tables": {}
        }
        
        for table_name, table in self.tables.items():
            stats["tables"][table_name] = {
                "records": len(table.data),
                "schema_fields": len(table.schema)
            }
        
        if self.persist and self.storage:
            disk_stats = self.storage.get_stats()
            stats["disk"] = disk_stats
        
        return stats
    
    def checkpoint(self):
        """Checkpoint the Write-Ahead Log."""
        if self.persist and self.storage:
            self.storage.checkpoint()
    
    def export_table(self, table_name: str, output_file: str):
        """Export a table to JSON."""
        if self.persist and self.storage:
            self.storage.export_table_to_json(table_name, output_file)


# Global database instance
_default_db = Database()


def table(db: Database = None):
    """
    Decorator to convert a dataclass into a database table.
    
    Usage:
        @table()
        @dataclass
        class Student:
            id: int = field(metadata={'primary_key': True})
            name: str
            age: int
            gpa: float = field(metadata={'nullable': True})
    """
    def decorator(cls):
        if not hasattr(cls, '__dataclass_fields__'):
            raise ValueError(f"{cls.__name__} must be a dataclass")
        
        # Extract schema from dataclass
        schema = {}
        for field_name, field_obj in cls.__dataclass_fields__.items():
            field_type = field_obj.type
            
            # Get metadata
            metadata = field_obj.metadata or {}
            primary_key = metadata.get('primary_key', False)
            nullable = metadata.get('nullable', field_obj.default is not None or field_obj.default_factory is not None)
            unique = metadata.get('unique', False)
            
            schema[field_name] = Field(
                field_type=field_type,
                primary_key=primary_key,
                nullable=nullable,
                unique=unique
            )
        
        # Create table in database
        target_db = db or _default_db
        table_name = cls.__name__.lower()
        target_db.create_table(table_name, schema)
        
        # Add helper methods to the class
        cls._table_name = table_name
        cls._db = target_db
        
        @classmethod
        def insert(cls_self, **kwargs):
            """Insert a record into the table."""
            table_obj = cls_self._db.get_table(cls_self._table_name)
            return table_obj.insert(kwargs)
        
        @classmethod
        def select(cls_self, where=None, order_by=None, limit=None):
            """Query records from the table."""
            table_obj = cls_self._db.get_table(cls_self._table_name)
            return table_obj.select(where=where, order_by=order_by, limit=limit)
        
        @classmethod
        def update(cls_self, where, **kwargs):
            """Update records in the table."""
            table_obj = cls_self._db.get_table(cls_self._table_name)
            return table_obj.update(where=where, updates=kwargs)
        
        @classmethod
        def delete(cls_self, where):
            """Delete records from the table."""
            table_obj = cls_self._db.get_table(cls_self._table_name)
            return table_obj.delete(where=where)
        
        @classmethod
        def count(cls_self):
            """Count records in the table."""
            table_obj = cls_self._db.get_table(cls_self._table_name)
            return table_obj.count()
        
        cls.insert = insert
        cls.select = select
        cls.update = update
        cls.delete = delete
        cls.count = count
        
        return cls
    
    return decorator


def get_db() -> Database:
    """Get the default database instance."""
    return _default_db
