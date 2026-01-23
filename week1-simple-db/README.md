# Simple In-Memory Database with Persistence

A production-quality in-memory database system implemented in Python with a decorator-based API and sophisticated file-based persistence that's **much better than a single JSON blob**!

## Features

### Core Database
- **Decorator-based Schema Definition**: Use `@table()` decorator with dataclasses to define tables
- **Type Support**: Supports common primitive types (int, str, float, bool, etc.)
- **CRUD Operations**: Full support for INSERT, SELECT, UPDATE, DELETE, and COUNT operations
- **Constraints**: Primary keys, unique constraints, nullable fields
- **Flexible Querying**: Lambda-based filtering, ordering, and limiting
- **Auto-increment Primary Keys**: Automatic ID generation
- **Type Validation**: Runtime validation of field types and constraints

### Persistence Layer ⭐ NEW!
- **Per-Table Storage**: Each table has its own files (not a single JSON blob!)
- **JSON Lines Format**: One record per line for efficient appending
- **Separate Schema Files**: Metadata stored independently for flexibility
- **Write-Ahead Log (WAL)**: Durability and crash recovery support
- **Checkpoint Support**: Archive and rotate WAL files
- **Export/Import**: Standard JSON export for portability
- **Statistics**: Detailed disk usage and table metrics

## Architecture

The system consists of five main components:

1. **Field**: Represents a column with type and constraints
2. **Table**: Manages schema and data for a single table
3. **Database**: Coordinates multiple tables and persistence
4. **StorageEngine**: Handles file I/O and Write-Ahead Logging
5. **Decorator API**: `@table()` for clean schema definitions

### File Structure

When persistence is enabled, the database creates this structure:

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

**Why This is Better Than a JSON Blob:**
- ✅ Scalable - Load only the tables you need
- ✅ Fast Writes - Append records without rewriting entire file
- ✅ Recoverable - WAL enables crash recovery
- ✅ Debuggable - Easy to inspect individual files with standard tools
- ✅ Efficient - Smaller files, better I/O performance

## Usage

### Basic Usage (In-Memory)

### Define Tables

```python
from dataclasses import dataclass, field
from database import table

@table()
@dataclass
class Student:
    id: int = field(metadata={'primary_key': True})
    name: str = field(metadata={'nullable': False})
    email: str = field(metadata={'unique': True, 'nullable': False})
    gpa: float = field(default=0.0)
```

### Insert Data

```python
Student.insert(name="Alice Johnson", email="alice@university.edu", gpa=3.8)
```

### Query Data

```python
# All records
all_students = Student.select()

# With filtering
top_students = Student.select(where=lambda s: s['gpa'] > 3.5)

# With ordering
students_by_gpa = Student.select(order_by='-gpa')

# With limit
top_3 = Student.select(order_by='-gpa', limit=3)
```

### Update Data

```python
Student.update(
    where=lambda s: s['name'] == "Alice Johnson",
    gpa=3.9
)
```

### Delete Data

```python
Student.delete(where=lambda s: s['gpa'] < 2.0)
```

### Count Records

```python
total = Student.count()
```

### Persistent Usage (Save to Disk)

```python
from database import Database

# Create a persistent database
db = Database(name="university", persist=True, base_path="./data")

# Define tables with this database
@table(db=db)
@dataclass
class Student:
    id: int = field(metadata={'primary_key': True})
    name: str
    gpa: float

# Insert and manipulate data
Student.insert(name="Alice", gpa=3.8)
Student.insert(name="Bob", gpa=3.5)

# Save to disk
db.save()

# Later... load from disk
db_new = Database(name="university", persist=True, base_path="./data")
db_new.load()

# Data is restored!
students = Student.select()
```

See [PERSISTENCE.md](PERSISTENCE.md) for complete persistence documentation.

## Running the Examples

Use `uv` to run the example applications:

```bash
# In-memory database example
uv run example.py

# Persistence demonstration
uv run example_persistence.py

# Run tests
uv run test_database.py
uv run test_persistence.py
```

**example.py** demonstrates:
- Student/Course/Registration system
- Sample data seeding
- 10+ query examples
- Update operations

**example_persistence.py** demonstrates:
- Creating persistent databases
- Saving and loading data
- File structure inspection
- WAL management
- Export/import functionality

## Field Metadata Options

- `primary_key`: Boolean - marks field as primary key (auto-incrementing)
- `nullable`: Boolean - allows NULL values
- `unique`: Boolean - enforces uniqueness constraint

## Design Considerations

The database is designed to be:

- **Extensible**: Easy to add new features like indexes, joins, or transactions
- **Type-safe**: Runtime validation of types and constraints
- **Pythonic**: Leverages dataclasses and decorators for clean syntax
- **Testable**: Simple API makes unit testing straightforward

## Future Enhancements

Potential areas for expansion:
- Foreign key relationships and joins
- Indexes for faster lookups
- Transaction support (ACID properties)
- Query builder API
- Aggregation functions (SUM, AVG, COUNT, etc.)
- More complex constraints
- Persistence to disk
- Query optimization
- Concurrent access control
