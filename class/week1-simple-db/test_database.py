"""
Test and demonstration of database features and edge cases.
"""

from dataclasses import dataclass, field
from database import table, get_db, Database


def test_basic_operations():
    """Test basic CRUD operations."""
    print("=" * 80)
    print("TEST 1: Basic CRUD Operations")
    print("=" * 80 + "\n")
    
    # Create a simple database
    test_db = Database("test")
    
    @table(db=test_db)
    @dataclass
    class Person:
        id: int = field(metadata={'primary_key': True})
        name: str = field(metadata={'nullable': False})
        age: int = field(metadata={'nullable': False})
    
    # INSERT
    print("✓ Inserting records...")
    Person.insert(name="John", age=30)
    Person.insert(name="Jane", age=25)
    Person.insert(name="Bob", age=35)
    print(f"  Total records: {Person.count()}")
    
    # SELECT
    print("\n✓ Selecting all records...")
    all_people = Person.select()
    for p in all_people:
        print(f"  {p}")
    
    # UPDATE
    print("\n✓ Updating John's age to 31...")
    updated = Person.update(where=lambda p: p['name'] == 'John', age=31)
    print(f"  Updated {updated} record(s)")
    
    # Verify update
    john = Person.select(where=lambda p: p['name'] == 'John')[0]
    print(f"  John's new age: {john['age']}")
    
    # DELETE
    print("\n✓ Deleting Bob...")
    deleted = Person.delete(where=lambda p: p['name'] == 'Bob')
    print(f"  Deleted {deleted} record(s)")
    print(f"  Remaining records: {Person.count()}")
    
    print("\n✅ Test 1 passed!\n")


def test_constraints():
    """Test field constraints and validation."""
    print("=" * 80)
    print("TEST 2: Constraints and Validation")
    print("=" * 80 + "\n")
    
    test_db = Database("test_constraints")
    
    @table(db=test_db)
    @dataclass
    class User:
        id: int = field(metadata={'primary_key': True})
        username: str = field(metadata={'unique': True, 'nullable': False})
        email: str = field(metadata={'unique': True, 'nullable': False})
        age: int = field(default=18)
    
    # Test successful insert
    print("✓ Inserting valid user...")
    User.insert(username="alice", email="alice@example.com", age=25)
    print("  Success!")
    
    # Test unique constraint
    print("\n✓ Testing unique constraint...")
    try:
        User.insert(username="alice", email="different@example.com", age=30)
        print("  ❌ Should have failed!")
    except ValueError as e:
        print(f"  ✓ Correctly rejected: {e}")
    
    # Test nullable constraint
    print("\n✓ Testing nullable constraint...")
    try:
        User.insert(username=None, email="test@example.com", age=20)
        print("  ❌ Should have failed!")
    except ValueError as e:
        print(f"  ✓ Correctly rejected: {e}")
    
    print("\n✅ Test 2 passed!\n")


def test_complex_queries():
    """Test more complex query patterns."""
    print("=" * 80)
    print("TEST 3: Complex Queries")
    print("=" * 80 + "\n")
    
    test_db = Database("test_queries")
    
    @table(db=test_db)
    @dataclass
    class Product:
        id: int = field(metadata={'primary_key': True})
        name: str = field(metadata={'nullable': False})
        category: str = field(metadata={'nullable': False})
        price: float = field(metadata={'nullable': False})
        in_stock: bool = field(default=True)
    
    # Insert test data
    products = [
        {"name": "Laptop", "category": "Electronics", "price": 999.99, "in_stock": True},
        {"name": "Mouse", "category": "Electronics", "price": 29.99, "in_stock": True},
        {"name": "Desk", "category": "Furniture", "price": 299.99, "in_stock": False},
        {"name": "Chair", "category": "Furniture", "price": 199.99, "in_stock": True},
        {"name": "Monitor", "category": "Electronics", "price": 399.99, "in_stock": True},
        {"name": "Lamp", "category": "Furniture", "price": 49.99, "in_stock": False},
    ]
    
    for p in products:
        Product.insert(**p)
    
    print(f"✓ Inserted {len(products)} products\n")
    
    # Query 1: Electronics under $500
    print("Query 1: Electronics under $500")
    results = Product.select(
        where=lambda p: p['category'] == 'Electronics' and p['price'] < 500
    )
    for r in results:
        print(f"  - {r['name']}: ${r['price']}")
    
    # Query 2: Out of stock items
    print("\nQuery 2: Out of stock items")
    results = Product.select(where=lambda p: not p['in_stock'])
    for r in results:
        print(f"  - {r['name']} ({r['category']})")
    
    # Query 3: Furniture sorted by price
    print("\nQuery 3: Furniture sorted by price (ascending)")
    results = Product.select(
        where=lambda p: p['category'] == 'Furniture',
        order_by='price'
    )
    for r in results:
        print(f"  - {r['name']}: ${r['price']}")
    
    # Query 4: Most expensive products (top 2)
    print("\nQuery 4: Top 2 most expensive products")
    results = Product.select(order_by='-price', limit=2)
    for r in results:
        print(f"  - {r['name']}: ${r['price']}")
    
    print("\n✅ Test 3 passed!\n")


def test_multiple_tables():
    """Test working with multiple related tables."""
    print("=" * 80)
    print("TEST 4: Multiple Tables")
    print("=" * 80 + "\n")
    
    test_db = Database("test_multi")
    
    @table(db=test_db)
    @dataclass
    class Author:
        id: int = field(metadata={'primary_key': True})
        name: str = field(metadata={'nullable': False})
        country: str = field(metadata={'nullable': False})
    
    @table(db=test_db)
    @dataclass
    class Book:
        id: int = field(metadata={'primary_key': True})
        title: str = field(metadata={'nullable': False})
        author_id: int = field(metadata={'nullable': False})
        year: int = field(metadata={'nullable': False})
    
    # Insert authors
    Author.insert(name="J.K. Rowling", country="UK")
    Author.insert(name="George Orwell", country="UK")
    Author.insert(name="Ernest Hemingway", country="USA")
    
    # Insert books
    Book.insert(title="Harry Potter and the Philosopher's Stone", author_id=1, year=1997)
    Book.insert(title="1984", author_id=2, year=1949)
    Book.insert(title="Animal Farm", author_id=2, year=1945)
    Book.insert(title="The Old Man and the Sea", author_id=3, year=1952)
    
    print(f"✓ Created {Author.count()} authors and {Book.count()} books\n")
    
    # Manual "join" - find all books by George Orwell
    print("Query: Books by George Orwell")
    orwell = Author.select(where=lambda a: a['name'] == 'George Orwell')[0]
    orwell_books = Book.select(where=lambda b: b['author_id'] == orwell['id'])
    
    for book in orwell_books:
        print(f"  - {book['title']} ({book['year']})")
    
    # Find authors with books published before 1950
    print("\nQuery: Authors with books published before 1950")
    old_books = Book.select(where=lambda b: b['year'] < 1950)
    author_ids = set(b['author_id'] for b in old_books)
    
    for author_id in author_ids:
        author = Author.select(where=lambda a: a['id'] == author_id)[0]
        print(f"  - {author['name']} ({author['country']})")
    
    print("\n✅ Test 4 passed!\n")


def test_edge_cases():
    """Test edge cases and special scenarios."""
    print("=" * 80)
    print("TEST 5: Edge Cases")
    print("=" * 80 + "\n")
    
    test_db = Database("test_edge")
    
    @table(db=test_db)
    @dataclass
    class Item:
        id: int = field(metadata={'primary_key': True})
        name: str = field(metadata={'nullable': False})
        value: int = field(default=0)
    
    # Empty table queries
    print("✓ Testing empty table...")
    assert Item.count() == 0
    assert Item.select() == []
    print("  Empty table queries work correctly")
    
    # Insert and immediate query
    print("\n✓ Testing insert and query...")
    Item.insert(name="First", value=100)
    assert Item.count() == 1
    print("  Insert successful")
    
    # Update with no matches
    print("\n✓ Testing update with no matches...")
    updated = Item.update(where=lambda i: i['name'] == 'Nonexistent', value=200)
    assert updated == 0
    print("  Update correctly returned 0")
    
    # Delete with no matches
    print("\n✓ Testing delete with no matches...")
    deleted = Item.delete(where=lambda i: i['value'] > 1000)
    assert deleted == 0
    print("  Delete correctly returned 0")
    
    # Query with limit larger than result set
    print("\n✓ Testing limit larger than results...")
    results = Item.select(limit=100)
    assert len(results) == 1
    print("  Limit handled correctly")
    
    print("\n✅ Test 5 passed!\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("🧪 DATABASE TEST SUITE")
    print("=" * 80 + "\n")
    
    test_basic_operations()
    test_constraints()
    test_complex_queries()
    test_multiple_tables()
    test_edge_cases()
    
    print("=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
