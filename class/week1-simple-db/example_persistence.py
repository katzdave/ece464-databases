"""
Example demonstrating database persistence to disk.
Shows how to save/load data and inspect the file structure.
"""

from dataclasses import dataclass, field
from database import Database, table, Field
import json
from pathlib import Path


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"📝 {title}")
    print("=" * 80 + "\n")


def demonstrate_basic_persistence():
    """Show basic save/load operations."""
    print_header("PART 1: Creating Database with Persistence")
    
    # Create a persistent database
    db = Database(name="university", persist=True, base_path="./data")
    
    # Define tables with this database
    @table(db=db)
    @dataclass
    class Student:
        id: int = field(metadata={'primary_key': True})
        name: str = field(metadata={'nullable': False})
        email: str = field(metadata={'unique': True})
        gpa: float = field(default=0.0)
    
    @table(db=db)
    @dataclass
    class Course:
        id: int = field(metadata={'primary_key': True})
        code: str = field(metadata={'unique': True})
        name: str = field(metadata={'nullable': False})
        credits: int = field(metadata={'nullable': False})
    
    # Insert some data
    print("✓ Inserting students...")
    Student.insert(name="Alice Johnson", email="alice@university.edu", gpa=3.8)
    Student.insert(name="Bob Smith", email="bob@university.edu", gpa=3.5)
    Student.insert(name="Carol White", email="carol@university.edu", gpa=3.9)
    print(f"  Inserted {Student.count()} students")
    
    print("\n✓ Inserting courses...")
    Course.insert(code="CS101", name="Intro to Programming", credits=4)
    Course.insert(code="CS201", name="Data Structures", credits=4)
    Course.insert(code="MATH101", name="Calculus I", credits=3)
    print(f"  Inserted {Course.count()} courses")
    
    # Save to disk
    print_header("PART 2: Saving to Disk")
    print("✓ Saving database to disk...")
    tables_saved = db.save()
    print(f"  Saved {tables_saved} tables")
    
    # Show stats
    stats = db.get_stats()
    print("\n📊 Database Statistics:")
    print(f"  Database name: {stats['name']}")
    print(f"  Persistence: {stats['persist']}")
    print(f"  Tables in memory: {len(stats['tables'])}")
    
    if 'disk' in stats:
        disk = stats['disk']
        print(f"\n💾 Disk Storage:")
        print(f"  Location: {disk['db_path']}")
        print(f"  Total size: {disk['total_size_bytes']} bytes")
        print(f"  WAL entries: {disk.get('wal_entries', 0)}")
        
        for table_name, table_info in disk['tables'].items():
            print(f"\n  Table: {table_name}")
            print(f"    Records: {table_info['records']}")
            print(f"    Size: {table_info['size_bytes']} bytes")
    
    return db


def demonstrate_file_structure():
    """Show the file structure on disk."""
    print_header("PART 3: Inspecting File Structure")
    
    db_path = Path("./data/university")
    
    print("📁 Directory Structure:")
    print(f"  {db_path}/")
    
    # Show schema files
    schema_path = db_path / "schema"
    if schema_path.exists():
        print(f"    schema/")
        for schema_file in sorted(schema_path.glob("*.schema.json")):
            size = schema_file.stat().st_size
            print(f"      {schema_file.name} ({size} bytes)")
            
            # Show schema content
            with open(schema_file, 'r') as f:
                schema_data = json.load(f)
                print(f"        Fields: {', '.join(schema_data['schema'].keys())}")
    
    # Show data files
    data_path = db_path / "data"
    if data_path.exists():
        print(f"    data/")
        for data_file in sorted(data_path.glob("*.records")):
            size = data_file.stat().st_size
            record_count = sum(1 for _ in open(data_file))
            print(f"      {data_file.name} ({size} bytes, {record_count} records)")
            
            # Show first record as example
            with open(data_file, 'r') as f:
                first_line = f.readline().strip()
                if first_line:
                    record = json.loads(first_line)
                    print(f"        Example: {record}")
    
    # Show WAL
    wal_path = db_path / "wal"
    if wal_path.exists():
        print(f"    wal/")
        for wal_file in sorted(wal_path.glob("*.log")):
            size = wal_file.stat().st_size
            entry_count = sum(1 for _ in open(wal_file))
            print(f"      {wal_file.name} ({size} bytes, {entry_count} entries)")


def demonstrate_loading():
    """Show loading data from disk."""
    print_header("PART 4: Loading from Disk (Fresh Instance)")
    
    # Create a NEW database instance (simulating app restart)
    print("✓ Creating new database instance...")
    db_new = Database(name="university", persist=True, base_path="./data")
    
    print(f"  Tables before load: {len(db_new.list_tables())}")
    
    # Load from disk
    print("\n✓ Loading from disk...")
    tables_loaded = db_new.load()
    print(f"  Loaded {tables_loaded} tables")
    
    # Access the data
    student_table = db_new.get_table("student")
    course_table = db_new.get_table("course")
    
    print(f"\n📚 Loaded Data:")
    print(f"  Students: {len(student_table.data)} records")
    for student in student_table.data:
        print(f"    - {student['name']} (GPA: {student['gpa']})")
    
    print(f"\n  Courses: {len(course_table.data)} records")
    for course in course_table.data:
        print(f"    - {course['code']}: {course['name']}")
    
    return db_new


def demonstrate_updates_and_persistence():
    """Show that updates persist correctly."""
    print_header("PART 5: Updates and Persistence")
    
    # Load existing database
    db = Database(name="university", persist=True, base_path="./data")
    db.load()
    
    student_table = db.get_table("student")
    
    print("✓ Current students:")
    for s in student_table.data:
        print(f"  - {s['name']}: GPA {s['gpa']}")
    
    # Update Alice's GPA
    print("\n✓ Updating Alice's GPA to 4.0...")
    student_table.update(
        where=lambda s: s['name'] == 'Alice Johnson',
        updates={'gpa': 4.0}
    )
    
    # Add a new student
    print("✓ Adding new student...")
    student_table.insert({
        'name': 'David Brown',
        'email': 'david@university.edu',
        'gpa': 3.6
    })
    
    print(f"\n  Total students now: {len(student_table.data)}")
    
    # Save changes
    print("\n✓ Saving changes to disk...")
    db.save()
    
    print("\n✓ Updated students:")
    for s in student_table.data:
        print(f"  - {s['name']}: GPA {s['gpa']}")


def demonstrate_wal_inspection():
    """Show Write-Ahead Log contents."""
    print_header("PART 6: Write-Ahead Log Inspection")
    
    db = Database(name="university", persist=True, base_path="./data")
    
    if db.storage:
        wal_entries = db.storage.replay_wal()
        
        print(f"📝 WAL contains {len(wal_entries)} entries:")
        
        # Show last 10 entries
        recent_entries = wal_entries[-10:] if len(wal_entries) > 10 else wal_entries
        
        for i, entry in enumerate(recent_entries, 1):
            print(f"\n  {i}. Operation: {entry['operation']}")
            print(f"     Table: {entry['table']}")
            print(f"     Time: {entry['timestamp']}")
            
            if entry.get('record'):
                print(f"     Record: {entry['record']}")


def demonstrate_export():
    """Show exporting tables to JSON."""
    print_header("PART 7: Exporting Tables")
    
    db = Database(name="university", persist=True, base_path="./data")
    db.load()
    
    export_file = "./exports/students.json"
    Path("./exports").mkdir(exist_ok=True)
    
    print(f"✓ Exporting student table to {export_file}...")
    db.export_table("student", export_file)
    
    # Show the exported file
    with open(export_file, 'r') as f:
        export_data = json.load(f)
    
    print(f"\n📄 Exported file contents:")
    print(f"  Table: {export_data['table']}")
    print(f"  Count: {export_data['count']}")
    print(f"  Exported at: {export_data['exported_at']}")
    print(f"\n  Sample records:")
    for record in export_data['records'][:3]:
        print(f"    {record}")


def demonstrate_checkpoint():
    """Show WAL checkpointing."""
    print_header("PART 8: WAL Checkpoint")
    
    db = Database(name="university", persist=True, base_path="./data")
    
    if db.storage:
        wal_before = len(db.storage.replay_wal())
        print(f"✓ WAL entries before checkpoint: {wal_before}")
        
        print("\n✓ Performing checkpoint (archiving WAL)...")
        db.checkpoint()
        
        wal_after = len(db.storage.replay_wal())
        print(f"  WAL entries after checkpoint: {wal_after}")
        
        # Show archived WAL files
        wal_path = Path("./data/university/wal")
        archived = list(wal_path.glob("transaction.*.log"))
        if archived:
            print(f"\n📦 Archived WAL files:")
            for archive in archived:
                size = archive.stat().st_size
                print(f"  - {archive.name} ({size} bytes)")


def main():
    """Run all persistence demonstrations."""
    print("\n" + "=" * 80)
    print("💾 DATABASE PERSISTENCE DEMONSTRATION")
    print("=" * 80)
    
    # Clean start - remove old data
    import shutil
    if Path("./data/university").exists():
        print("\n🗑️  Cleaning old data...")
        shutil.rmtree("./data/university")
    if Path("./exports").exists():
        shutil.rmtree("./exports")
    
    # Run demonstrations
    db = demonstrate_basic_persistence()
    demonstrate_file_structure()
    demonstrate_loading()
    demonstrate_updates_and_persistence()
    demonstrate_wal_inspection()
    demonstrate_export()
    demonstrate_checkpoint()
    
    # Final stats
    print_header("FINAL STATISTICS")
    stats = db.get_stats()
    
    if 'disk' in stats:
        disk = stats['disk']
        print("💾 Final Disk Usage:")
        print(f"  Total size: {disk['total_size_bytes']} bytes")
        print(f"  Tables: {len(disk['tables'])}")
        
        for table_name, info in disk['tables'].items():
            print(f"    {table_name}: {info['records']} records, {info['size_bytes']} bytes")
    
    print("\n" + "=" * 80)
    print("✅ Persistence demonstration complete!")
    print("=" * 80)
    print(f"\n💡 Data persisted to: ./data/university/")
    print(f"   You can inspect the files to see the structure!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
