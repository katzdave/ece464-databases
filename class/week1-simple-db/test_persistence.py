"""
Test suite for database persistence layer.
"""

from dataclasses import dataclass, field
from database import Database, table
from pathlib import Path
import shutil
import json


def setup_clean_db(db_name="test_persist"):
    """Create a clean test database."""
    db_path = Path(f"./data/{db_name}")
    if db_path.exists():
        shutil.rmtree(db_path)
    return Database(name=db_name, persist=True, base_path="./data")


def test_basic_save_load():
    """Test basic save and load operations."""
    print("=" * 80)
    print("TEST 1: Basic Save and Load")
    print("=" * 80 + "\n")
    
    # Create and populate database
    db = setup_clean_db("test_basic")
    
    @table(db=db)
    @dataclass
    class Person:
        id: int = field(metadata={'primary_key': True})
        name: str = field(metadata={'nullable': False})
        age: int = field(default=0)
    
    print("✓ Inserting data...")
    Person.insert(name="Alice", age=30)
    Person.insert(name="Bob", age=25)
    Person.insert(name="Carol", age=35)
    
    initial_count = Person.count()
    print(f"  Inserted {initial_count} records")
    
    # Save to disk
    print("\n✓ Saving to disk...")
    db.save()
    
    # Create new instance and load
    print("\n✓ Creating new database instance...")
    db_new = Database(name="test_basic", persist=True, base_path="./data")
    
    print("✓ Loading from disk...")
    tables_loaded = db_new.load()
    
    assert tables_loaded == 1, f"Expected 1 table, got {tables_loaded}"
    
    person_table = db_new.get_table("person")
    loaded_count = len(person_table.data)
    
    print(f"  Loaded {loaded_count} records")
    assert loaded_count == initial_count, f"Expected {initial_count} records, got {loaded_count}"
    
    # Verify data
    print("\n✓ Verifying data integrity...")
    alice = [p for p in person_table.data if p['name'] == 'Alice'][0]
    assert alice['age'] == 30, f"Alice's age should be 30, got {alice['age']}"
    
    print("  All data verified!")
    print("\n✅ Test 1 passed!\n")


def test_schema_persistence():
    """Test that schema is correctly saved and loaded."""
    print("=" * 80)
    print("TEST 2: Schema Persistence")
    print("=" * 80 + "\n")
    
    db = setup_clean_db("test_schema")
    
    @table(db=db)
    @dataclass
    class Product:
        id: int = field(metadata={'primary_key': True})
        name: str = field(metadata={'nullable': False, 'unique': True})
        price: float = field(default=0.0)
        in_stock: bool = field(default=True)
    
    print("✓ Schema created for Product table")
    
    # Check schema file exists
    schema_file = Path("./data/test_schema/schema/product.schema.json")
    assert schema_file.exists(), "Schema file should exist"
    
    print("✓ Schema file exists")
    
    # Read and verify schema
    with open(schema_file, 'r') as f:
        schema_data = json.load(f)
    
    print("\n✓ Schema file contents:")
    print(f"  Table: {schema_data['table_name']}")
    print(f"  Fields: {', '.join(schema_data['schema'].keys())}")
    
    # Verify unique constraint
    assert schema_data['schema']['name']['unique'] == True
    print("  ✓ Unique constraint on 'name' preserved")
    
    # Verify nullable constraint
    assert schema_data['schema']['name']['nullable'] == False
    print("  ✓ Nullable constraint on 'name' preserved")
    
    print("\n✅ Test 2 passed!\n")


def test_updates_persist():
    """Test that updates are correctly persisted."""
    print("=" * 80)
    print("TEST 3: Updates Persist Across Sessions")
    print("=" * 80 + "\n")
    
    # Session 1: Create and update
    db1 = setup_clean_db("test_updates")
    
    @table(db=db1)
    @dataclass
    class User:
        id: int = field(metadata={'primary_key': True})
        username: str = field(metadata={'unique': True})
        score: int = field(default=0)
    
    print("✓ Session 1: Inserting users...")
    User.insert(username="alice", score=100)
    User.insert(username="bob", score=200)
    
    db1.save()
    
    print("✓ Session 1: Updating alice's score...")
    user_table = db1.get_table("user")
    user_table.update(
        where=lambda u: u['username'] == 'alice',
        updates={'score': 150}
    )
    db1.save()
    
    # Session 2: Load and verify
    print("\n✓ Session 2: Loading database...")
    db2 = Database(name="test_updates", persist=True, base_path="./data")
    db2.load()
    
    user_table2 = db2.get_table("user")
    alice = [u for u in user_table2.data if u['username'] == 'alice'][0]
    
    print(f"  Alice's score: {alice['score']}")
    assert alice['score'] == 150, f"Expected 150, got {alice['score']}"
    
    print("\n✅ Test 3 passed!\n")


def test_multiple_tables():
    """Test persistence with multiple tables."""
    print("=" * 80)
    print("TEST 4: Multiple Tables Persistence")
    print("=" * 80 + "\n")
    
    db = setup_clean_db("test_multi")
    
    @table(db=db)
    @dataclass
    class Author:
        id: int = field(metadata={'primary_key': True})
        name: str
    
    @table(db=db)
    @dataclass
    class Book:
        id: int = field(metadata={'primary_key': True})
        title: str
        author_id: int
    
    print("✓ Creating data in two tables...")
    Author.insert(name="George Orwell")
    Author.insert(name="J.K. Rowling")
    
    Book.insert(title="1984", author_id=1)
    Book.insert(title="Animal Farm", author_id=1)
    Book.insert(title="Harry Potter", author_id=2)
    
    db.save()
    
    # Load in new session
    print("\n✓ Loading from disk...")
    db_new = Database(name="test_multi", persist=True, base_path="./data")
    tables_loaded = db_new.load()
    
    assert tables_loaded == 2, f"Expected 2 tables, got {tables_loaded}"
    print(f"  Loaded {tables_loaded} tables")
    
    author_table = db_new.get_table("author")
    book_table = db_new.get_table("book")
    
    assert len(author_table.data) == 2
    assert len(book_table.data) == 3
    
    print(f"  Authors: {len(author_table.data)}")
    print(f"  Books: {len(book_table.data)}")
    
    print("\n✅ Test 4 passed!\n")


def test_wal_operations():
    """Test Write-Ahead Log functionality."""
    print("=" * 80)
    print("TEST 5: Write-Ahead Log")
    print("=" * 80 + "\n")
    
    db = setup_clean_db("test_wal")
    
    @table(db=db)
    @dataclass
    class Event:
        id: int = field(metadata={'primary_key': True})
        name: str
    
    print("✓ Performing operations...")
    Event.insert(name="Event 1")
    Event.insert(name="Event 2")
    db.save()
    
    # Check WAL
    print("\n✓ Checking WAL...")
    operations = db.storage.replay_wal()
    
    print(f"  WAL entries: {len(operations)}")
    assert len(operations) > 0, "WAL should have entries"
    
    # Show operation types
    op_types = [op['operation'] for op in operations]
    print(f"  Operations: {', '.join(op_types)}")
    
    # Checkpoint
    print("\n✓ Checkpointing WAL...")
    db.checkpoint()
    
    operations_after = db.storage.replay_wal()
    print(f"  WAL entries after checkpoint: {len(operations_after)}")
    
    # Check for archived WAL
    wal_path = Path("./data/test_wal/wal")
    archived = list(wal_path.glob("transaction.*.log"))
    assert len(archived) > 0, "Should have archived WAL file"
    print(f"  Archived WAL files: {len(archived)}")
    
    print("\n✅ Test 5 passed!\n")


def test_stats():
    """Test statistics gathering."""
    print("=" * 80)
    print("TEST 6: Database Statistics")
    print("=" * 80 + "\n")
    
    db = setup_clean_db("test_stats")
    
    @table(db=db)
    @dataclass
    class Item:
        id: int = field(metadata={'primary_key': True})
        name: str
        value: int
    
    # Insert some data
    for i in range(10):
        Item.insert(name=f"Item {i}", value=i * 10)
    
    db.save()
    
    # Get stats
    print("✓ Getting statistics...")
    stats = db.get_stats()
    
    print(f"\n  Database: {stats['name']}")
    print(f"  Persistence: {stats['persist']}")
    print(f"  Tables: {len(stats['tables'])}")
    
    if 'disk' in stats:
        print(f"\n  Disk Stats:")
        print(f"    Total size: {stats['disk']['total_size_bytes']} bytes")
        print(f"    WAL entries: {stats['disk'].get('wal_entries', 0)}")
        
        for table_name, info in stats['disk']['tables'].items():
            print(f"\n    Table: {table_name}")
            print(f"      Records: {info['records']}")
            print(f"      Size: {info['size_bytes']} bytes")
            
            assert info['records'] == 10, "Should have 10 records"
    
    print("\n✅ Test 6 passed!\n")


def test_export():
    """Test table export functionality."""
    print("=" * 80)
    print("TEST 7: Table Export")
    print("=" * 80 + "\n")
    
    db = setup_clean_db("test_export")
    
    @table(db=db)
    @dataclass
    class Customer:
        id: int = field(metadata={'primary_key': True})
        name: str
        email: str
    
    print("✓ Creating customer data...")
    Customer.insert(name="Alice", email="alice@example.com")
    Customer.insert(name="Bob", email="bob@example.com")
    
    db.save()
    
    # Export
    export_path = Path("./exports_test")
    export_path.mkdir(exist_ok=True)
    export_file = export_path / "customers.json"
    
    print(f"\n✓ Exporting to {export_file}...")
    db.export_table("customer", str(export_file))
    
    assert export_file.exists(), "Export file should exist"
    
    # Verify export
    with open(export_file, 'r') as f:
        export_data = json.load(f)
    
    print(f"\n  Export contains:")
    print(f"    Table: {export_data['table']}")
    print(f"    Records: {export_data['count']}")
    
    assert export_data['count'] == 2
    assert len(export_data['records']) == 2
    
    # Cleanup
    shutil.rmtree(export_path)
    
    print("\n✅ Test 7 passed!\n")


def test_json_lines_format():
    """Verify JSON Lines format is correct."""
    print("=" * 80)
    print("TEST 8: JSON Lines Format Verification")
    print("=" * 80 + "\n")
    
    db = setup_clean_db("test_jsonl")
    
    @table(db=db)
    @dataclass
    class Record:
        id: int = field(metadata={'primary_key': True})
        data: str
    
    # Insert records
    print("✓ Inserting records...")
    for i in range(5):
        Record.insert(data=f"Record {i}")
    
    db.save()
    
    # Read file directly
    data_file = Path("./data/test_jsonl/data/record.records")
    
    print(f"\n✓ Reading {data_file}...")
    assert data_file.exists(), "Data file should exist"
    
    # Verify each line is valid JSON
    line_count = 0
    with open(data_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                record = json.loads(line)  # Should not raise exception
                assert 'id' in record
                assert 'data' in record
                line_count += 1
                print(f"  Line {line_count}: {record}")
    
    assert line_count == 5, f"Expected 5 lines, got {line_count}"
    
    print("\n✅ Test 8 passed!\n")


def cleanup_test_data():
    """Clean up all test databases."""
    print("🗑️  Cleaning up test data...")
    test_dbs = [
        "test_basic", "test_schema", "test_updates", "test_multi",
        "test_wal", "test_stats", "test_export", "test_jsonl"
    ]
    
    for db_name in test_dbs:
        db_path = Path(f"./data/{db_name}")
        if db_path.exists():
            shutil.rmtree(db_path)
    
    print("  ✓ Cleanup complete\n")


def main():
    """Run all persistence tests."""
    print("\n" + "=" * 80)
    print("🧪 PERSISTENCE TEST SUITE")
    print("=" * 80 + "\n")
    
    try:
        test_basic_save_load()
        test_schema_persistence()
        test_updates_persist()
        test_multiple_tables()
        test_wal_operations()
        test_stats()
        test_export()
        test_json_lines_format()
        
        print("=" * 80)
        print("✅ ALL PERSISTENCE TESTS PASSED!")
        print("=" * 80 + "\n")
        
    finally:
        cleanup_test_data()


if __name__ == "__main__":
    main()
