# Quick Start Guide

## Overview

This is a simple, extensible in-memory database system built in Python with a clean decorator-based API. Perfect for learning database concepts, prototyping, or small applications that don't need persistence.

## Installation & Running

No installation needed! Just use `uv`:

```bash
# Run the example application (recommended first step)
uv run example.py

# Run the test suite
uv run test_database.py
```

## 5-Minute Tutorial

### Step 1: Define Your Tables

```python
from dataclasses import dataclass, field
from database import table

@table()
@dataclass
class Student:
    id: int = field(metadata={'primary_key': True})
    name: str = field(metadata={'nullable': False})
    email: str = field(metadata={'unique': True})
    gpa: float = field(default=0.0)
```

### Step 2: Insert Data

```python
# Auto-generates ID
Student.insert(name="Alice Johnson", email="alice@uni.edu", gpa=3.8)
Student.insert(name="Bob Smith", email="bob@uni.edu", gpa=3.5)
```

### Step 3: Query Data

```python
# Get all students
all_students = Student.select()

# Filter with conditions
top_students = Student.select(where=lambda s: s['gpa'] > 3.5)

# Sort and limit
best_students = Student.select(order_by='-gpa', limit=3)
```

### Step 4: Update & Delete

```python
# Update records
Student.update(
    where=lambda s: s['name'] == 'Alice Johnson',
    gpa=3.9
)

# Delete records
Student.delete(where=lambda s: s['gpa'] < 2.0)
```

## What's Included

### Files

- **`database.py`** - Core database engine (Field, Table, Database classes)
- **`example.py`** - Complete student registration system example
- **`test_database.py`** - Comprehensive test suite
- **`README.md`** - Full documentation
- **`USAGE.md`** - Detailed API reference
- **`QUICKSTART.md`** - This file!

### Features

✅ Decorator-based table definitions  
✅ Auto-incrementing primary keys  
✅ Unique & nullable constraints  
✅ Type validation  
✅ Lambda-based filtering  
✅ Sorting & limiting results  
✅ Full CRUD operations  
✅ Multiple table support  
✅ Clean, extensible architecture  

## Example Output

```
🌱 Seeding database with sample data...

✓ Inserted 6 students
✓ Inserted 6 courses
✓ Inserted 15 registrations

📈 DATABASE STATISTICS
  Total Students:      6
  Total Courses:       6
  Total Registrations: 15
```

## Next Steps

1. **Run the examples**: `uv run example.py`
2. **Read the code**: Start with `example.py` to see real usage
3. **Experiment**: Try modifying the example or creating your own tables
4. **Read the docs**: Check `USAGE.md` for complete API reference
5. **Extend it**: Add features like indexes, joins, or persistence!

## Architecture Highlights

The system is built with extensibility in mind:

- **Modular design**: Field, Table, and Database classes are separate
- **Decorator pattern**: Clean syntax for table definitions
- **Functional queries**: Lambda-based filtering is flexible and readable
- **Type safety**: Runtime validation of types and constraints
- **Isolated databases**: Support for multiple database instances

## Common Use Cases

- **Learning**: Great for understanding database concepts
- **Prototyping**: Quick data structures without setup
- **Testing**: In-memory databases are perfect for unit tests
- **Small tools**: CLI tools or scripts that don't need persistence
- **Proof of concepts**: Validate ideas before moving to production DB

## Limitations

- No persistence (data lost when program ends)
- No JOIN operations (must be done manually)
- No indexes (all queries scan full table)
- No transactions
- Single-threaded only

See the Future Enhancements section in README.md for expansion ideas!

## Getting Help

- Check `USAGE.md` for detailed API documentation
- Look at `example.py` for practical examples
- Review `test_database.py` for edge cases and patterns
- Read `database.py` source code (well-commented!)

## Quick Reference

```python
# Define table
@table()
@dataclass
class MyTable:
    id: int = field(metadata={'primary_key': True})
    field: str = field(metadata={'nullable': False, 'unique': True})

# CRUD operations
MyTable.insert(field="value")                              # Create
MyTable.select(where=lambda r: r['field'] == "value")      # Read
MyTable.update(where=lambda r: r['id'] == 1, field="new")  # Update
MyTable.delete(where=lambda r: r['id'] == 1)               # Delete
MyTable.count()                                            # Count
```

Happy coding! 🚀
