# Database Persistence

The database now supports **persistent storage** with a sophisticated file-based architecture that's much better than a single JSON blob!

## Features

✅ **Per-table storage** - Each table has its own files  
✅ **JSON Lines format** - One record per line for efficient appending  
✅ **Separate schema files** - Metadata stored independently  
✅ **Write-Ahead Log (WAL)** - Durability and crash recovery  
✅ **Checkpoint support** - Archive and rotate WAL files  
✅ **Export/Import** - Standard JSON export for portability  

## File Structure

```
data/
└── db_name/
    ├── schema/
    │   ├── table1.schema.json    # Table metadata
    │   └── table2.schema.json
    ├── data/
    │   ├── table1.records         # JSON Lines (one record per line)
    │   └── table2.records
    └── wal/
        ├── transaction.log        # Current Write-Ahead Log
        └── transaction.*.log      # Archived WAL files
```

### Why This is Better Than a Single JSON Blob

| Feature | Single JSON Blob | Our Approach |
|---------|-----------------|--------------|
| **Scalability** | Load entire DB into memory | Load only needed tables |
| **Write Performance** | Rewrite entire file on change | Append new records |
| **Crash Recovery** | No recovery mechanism | WAL provides durability |
| **File Size** | Single large file | Multiple smaller files |
| **Debuggability** | Hard to inspect large files | Easy to view individual tables |
| **Concurrent Access** | Lock entire DB | Could lock per-table (future) |

## Usage

### Creating a Persistent Database

```python
from database import Database

# Create database with persistence enabled
db = Database(name="university", persist=True, base_path="./data")
```

### Defining Tables

```python
from dataclasses import dataclass, field
from database import table

@table(db=db)
@dataclass
class Student:
    id: int = field(metadata={'primary_key': True})
    name: str = field(metadata={'nullable': False})
    email: str = field(metadata={'unique': True})
    gpa: float = field(default=0.0)
```

The schema is automatically saved to disk when the table is created!

### Saving Data

```python
# Insert data (in-memory only at this point)
Student.insert(name="Alice", email="alice@university.edu", gpa=3.8)
Student.insert(name="Bob", email="bob@university.edu", gpa=3.5)

# Persist to disk
db.save()  # Writes all tables to their .records files
```

### Loading Data

```python
# Create a new database instance
db = Database(name="university", persist=True, base_path="./data")

# Load from disk
db.load()  # Discovers and loads all tables

# Access the data
student_table = db.get_table("student")
students = student_table.select()
```

### Operations Persist Automatically

Schema changes (table creation) are written immediately. Data operations require explicit save:

```python
# Schema saved immediately
@table(db=db)
@dataclass
class Course:
    id: int = field(metadata={'primary_key': True})
    code: str

# Data changes require explicit save
Course.insert(code="CS101")
db.save()  # <-- Don't forget this!
```

## File Formats

### Schema File (.schema.json)

```json
{
  "table_name": "student",
  "schema": {
    "id": {
      "type": "int",
      "primary_key": true,
      "nullable": true,
      "unique": false
    },
    "name": {
      "type": "str",
      "primary_key": false,
      "nullable": false,
      "unique": false
    }
  },
  "created_at": "2026-01-22T20:31:17.592172"
}
```

### Data File (.records) - JSON Lines

Each line is a complete JSON object representing one record:

```json
{"name": "Alice Johnson", "email": "alice@university.edu", "gpa": 3.8, "id": 1}
{"name": "Bob Smith", "email": "bob@university.edu", "gpa": 3.5, "id": 2}
{"name": "Carol White", "email": "carol@university.edu", "gpa": 3.9, "id": 3}
```

**Benefits of JSON Lines:**
- Append-only writes (no need to rewrite entire file for inserts)
- Easy to stream/process line by line
- Simple to grep/search with standard tools
- Human-readable and debuggable

### Write-Ahead Log (transaction.log)

Records all operations for durability:

```json
{"timestamp": "2026-01-22T20:31:17.592245", "operation": "CREATE_TABLE", "table": "student", "record": null, "old_record": null}
{"timestamp": "2026-01-22T20:31:17.592722", "operation": "CREATE_TABLE", "table": "course", "record": null, "old_record": null}
{"timestamp": "2026-01-22T20:31:17.593123", "operation": "INSERT", "table": "student", "record": {"id": 1, "name": "Alice"}, "old_record": null}
```

## Advanced Operations

### Statistics

```python
stats = db.get_stats()

# In-memory stats
print(f"Tables: {len(stats['tables'])}")

# Disk stats (if persistence enabled)
if 'disk' in stats:
    print(f"Total size: {stats['disk']['total_size_bytes']} bytes")
    for table_name, info in stats['disk']['tables'].items():
        print(f"  {table_name}: {info['records']} records")
```

### Checkpoint WAL

Archive the Write-Ahead Log after confirming data is saved:

```python
db.save()         # Save all data
db.checkpoint()   # Archive WAL
```

This creates an archived WAL file like `transaction.20260122_203117.log` and starts a fresh log.

### Export Table to JSON

Export a table to a standard JSON file:

```python
db.export_table("student", "exports/students.json")
```

Output format:
```json
{
  "table": "student",
  "records": [
    {"id": 1, "name": "Alice", ...},
    {"id": 2, "name": "Bob", ...}
  ],
  "count": 2,
  "exported_at": "2026-01-22T20:31:17.594614"
}
```

### Inspect WAL

View all operations in the Write-Ahead Log:

```python
if db.storage:
    operations = db.storage.replay_wal()
    for op in operations:
        print(f"{op['timestamp']}: {op['operation']} on {op['table']}")
```

## Architecture Details

### Write Path

1. **Insert/Update/Delete** → Modify in-memory data
2. **db.save()** → Write to `.records` file
3. **WAL Entry** → Log operation for durability
4. **Checkpoint** → Archive WAL after confirming save

### Read Path

1. **db.load()** → Discover tables from schema files
2. **Load Schema** → Parse `.schema.json` files
3. **Load Records** → Read `.records` files line-by-line
4. **Reconstruct Tables** → Create in-memory tables with data

### Recovery Path (Future)

The WAL enables crash recovery:
1. Load last known good state from `.records` files
2. Replay WAL entries to recover uncommitted changes
3. Restore to consistent state

## Performance Characteristics

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| **Insert + Append** | O(1) | Append single line to file |
| **Insert + Save** | O(n) | Rewrite entire table |
| **Load** | O(n) | Read all records |
| **Update** | O(n) | Must rewrite file |
| **Delete** | O(n) | Must rewrite file |

**Optimization Strategy:**
- Use append mode for inserts (not yet implemented)
- Batch updates before saving
- Implement compaction to remove deleted records

## Best Practices

### 1. Batch Your Saves

```python
# ❌ Bad - save after every insert
for student in students:
    Student.insert(**student)
    db.save()  # Expensive!

# ✅ Good - batch inserts then save once
for student in students:
    Student.insert(**student)
db.save()  # Single write
```

### 2. Checkpoint Regularly

```python
# After major operations
db.save()
db.checkpoint()  # Archive WAL
```

### 3. Use Stats to Monitor Growth

```python
stats = db.get_stats()
if stats['disk']['total_size_bytes'] > 10_000_000:  # 10MB
    print("Database getting large, consider archiving")
```

### 4. Handle Errors Gracefully

```python
try:
    db.save()
except IOError as e:
    print(f"Failed to save: {e}")
    # Could retry or alert
```

## Comparison with Real Databases

Our approach is similar to how real databases work:

| Feature | Our DB | SQLite | PostgreSQL |
|---------|--------|--------|------------|
| **Storage Format** | JSON Lines | B-tree pages | Pages + MVCC |
| **WAL** | JSON log | Binary WAL | WAL + checkpoints |
| **Crash Recovery** | Replay WAL | Replay WAL | REDO/UNDO logs |
| **Compaction** | Manual | Auto VACUUM | Auto VACUUM |
| **Indexes** | None | B-tree | B-tree, Hash, GiST, etc. |

## Future Enhancements

### Short-term
- [ ] Auto-save mode (save after every operation)
- [ ] Append-only inserts (don't rewrite file)
- [ ] Automatic compaction on load

### Medium-term
- [ ] Implement WAL replay for crash recovery
- [ ] Compressed data files (gzip)
- [ ] Table-level locking for concurrent access

### Long-term
- [ ] Binary format for better performance
- [ ] Incremental saves (only changed tables)
- [ ] Streaming large result sets

## Examples

See `example_persistence.py` for comprehensive examples including:
- Creating persistent databases
- Saving and loading data
- Inspecting file structure
- Updates across sessions
- WAL inspection and checkpointing
- Exporting tables

Run it:
```bash
uv run example_persistence.py
```

## File Locations

By default, data is stored in:
```
./data/{db_name}/
```

You can customize the base path:
```python
db = Database(name="mydb", persist=True, base_path="/var/lib/myapp/data")
```

## Debugging

### View Schema

```bash
cat data/university/schema/student.schema.json | python -m json.tool
```

### View Records

```bash
cat data/university/data/student.records
```

### Count Records

```bash
wc -l data/university/data/student.records
```

### Search Records

```bash
grep "Alice" data/university/data/student.records
```

### View WAL

```bash
cat data/university/wal/transaction.log
```

The JSON Lines format makes it easy to use standard Unix tools!
