# Usage Guide

## Quick Start

Run the example application:
```bash
uv run example.py
```

Run the test suite:
```bash
uv run test_database.py
```

## API Reference

### Defining Tables

Use the `@table()` decorator with Python dataclasses:

```python
from dataclasses import dataclass, field
from database import table

@table()
@dataclass
class YourTable:
    id: int = field(metadata={'primary_key': True})
    required_field: str = field(metadata={'nullable': False})
    unique_field: str = field(metadata={'unique': True})
    optional_field: int = field(default=0)
```

### Field Metadata

- **`primary_key: bool`** - Marks field as primary key (auto-incrementing if not provided)
- **`nullable: bool`** - Allows NULL/None values (default: True if field has default, False otherwise)
- **`unique: bool`** - Enforces uniqueness constraint

### CRUD Operations

#### INSERT

```python
# Basic insert
Student.insert(name="Alice", email="alice@example.com", age=20)

# Returns the inserted record with auto-generated ID
record = Student.insert(name="Bob", email="bob@example.com")
print(record)  # {'id': 1, 'name': 'Bob', 'email': 'bob@example.com', ...}
```

#### SELECT (Query)

```python
# Select all records
all_students = Student.select()

# Filter with lambda function
cs_students = Student.select(where=lambda s: s['major'] == 'Computer Science')

# Multiple conditions
top_students = Student.select(
    where=lambda s: s['gpa'] > 3.5 and s['age'] < 22
)

# Ordering (ascending)
by_name = Student.select(order_by='name')

# Ordering (descending - use '-' prefix)
by_gpa = Student.select(order_by='-gpa')

# Limiting results
top_3 = Student.select(order_by='-gpa', limit=3)

# Combining all options
results = Student.select(
    where=lambda s: s['gpa'] > 3.0,
    order_by='-gpa',
    limit=10
)
```

#### UPDATE

```python
# Update matching records
count = Student.update(
    where=lambda s: s['name'] == 'Alice',
    gpa=3.9,
    major='Data Science'
)
print(f"Updated {count} records")

# Update multiple records
Student.update(
    where=lambda s: s['age'] < 20,
    status='Undergraduate'
)
```

#### DELETE

```python
# Delete matching records
count = Student.delete(where=lambda s: s['gpa'] < 2.0)
print(f"Deleted {count} records")

# Delete single record
Student.delete(where=lambda s: s['id'] == 5)
```

#### COUNT

```python
# Total count
total = Student.count()

# Use select + len for conditional count
active_count = len(Student.select(where=lambda s: s['status'] == 'Active'))
```

### Working with Multiple Databases

By default, tables are created in a global database. You can create separate databases:

```python
from database import Database, table

# Create a new database
my_db = Database("my_database")

# Use it with tables
@table(db=my_db)
@dataclass
class MyTable:
    id: int = field(metadata={'primary_key': True})
    data: str
```

### Manual Joins

Since JOIN operations aren't built-in yet, you can manually join data:

```python
# Find all books by a specific author
author = Author.select(where=lambda a: a['name'] == 'George Orwell')[0]
books = Book.select(where=lambda b: b['author_id'] == author['id'])

# Or create a helper function
def get_books_by_author(author_name):
    authors = Author.select(where=lambda a: a['name'] == author_name)
    if not authors:
        return []
    
    author_id = authors[0]['id']
    return Book.select(where=lambda b: b['author_id'] == author_id)
```

## Common Patterns

### Checking if record exists

```python
results = Student.select(where=lambda s: s['email'] == 'test@example.com')
if results:
    print("Student exists:", results[0])
else:
    print("Student not found")
```

### Updating or inserting (upsert)

```python
email = 'alice@example.com'
existing = Student.select(where=lambda s: s['email'] == email)

if existing:
    Student.update(
        where=lambda s: s['email'] == email,
        gpa=3.9
    )
else:
    Student.insert(name='Alice', email=email, gpa=3.9)
```

### Batch operations

```python
# Batch insert
students = [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"},
    {"name": "Carol", "email": "carol@example.com"},
]

for student in students:
    Student.insert(**student)
```

### Aggregations (manual)

```python
# Average GPA
students = Student.select()
avg_gpa = sum(s['gpa'] for s in students) / len(students)

# Max/Min
max_gpa = max(s['gpa'] for s in students)
min_age = min(s['age'] for s in students)

# Group by (manual)
from collections import defaultdict

by_major = defaultdict(list)
for student in Student.select():
    by_major[student['major']].append(student)

for major, students in by_major.items():
    print(f"{major}: {len(students)} students")
```

## Type Support

Supported primitive types:
- `int`
- `str`
- `float`
- `bool`
- Any Python type (though complex types aren't validated)

## Error Handling

```python
try:
    Student.insert(name="Alice", email="alice@example.com")
    Student.insert(name="Bob", email="alice@example.com")  # Duplicate email
except ValueError as e:
    print(f"Error: {e}")  # Invalid record: Duplicate value for unique field email
```

## Best Practices

1. **Use primary keys**: Always define a primary key field for easier record management
2. **Validate before batch operations**: Check data validity before large inserts
3. **Use meaningful table names**: The decorator uses `ClassName.lower()` as table name
4. **Leverage lambdas**: Write clear, readable filter conditions
5. **Check return values**: Update and delete return counts - use them for verification
6. **Deep copies**: All returned data is deep-copied, so you can modify it safely

## Limitations

Current limitations (future enhancements):
- No built-in JOIN operations (must be done manually)
- No indexes (all queries are O(n))
- No transactions or rollback
- No persistence (data is lost when program exits)
- No concurrent access control
- Limited aggregation functions
