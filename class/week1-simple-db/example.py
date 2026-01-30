"""
Example usage of the in-memory database system.
Demonstrates a student course registration system.
"""

from dataclasses import dataclass, field
from database import table, get_db, Field
from typing import Optional


# Define the schema using dataclasses and decorators
@table()
@dataclass
class Student:
    """Student table with basic information."""
    id: int = field(metadata={'primary_key': True})
    name: str = field(metadata={'nullable': False})
    email: str = field(metadata={'unique': True, 'nullable': False})
    age: int = field(metadata={'nullable': False})
    gpa: float = field(default=0.0, metadata={'nullable': True})
    major: str = field(default="Undeclared", metadata={'nullable': True})


@table()
@dataclass
class Course:
    """Course table with course details."""
    id: int = field(metadata={'primary_key': True})
    code: str = field(metadata={'unique': True, 'nullable': False})
    name: str = field(metadata={'nullable': False})
    credits: int = field(metadata={'nullable': False})
    instructor: str = field(metadata={'nullable': True})


@table()
@dataclass
class Registration:
    """Registration table linking students to courses."""
    id: int = field(metadata={'primary_key': True})
    student_id: int = field(metadata={'nullable': False})
    course_id: int = field(metadata={'nullable': False})
    semester: str = field(metadata={'nullable': False})
    grade: str = field(default=None, metadata={'nullable': True})


def seed_data():
    """Populate the database with sample data."""
    print("🌱 Seeding database with sample data...\n")
    
    # Insert students
    students_data = [
        {"name": "Alice Johnson", "email": "alice@university.edu", "age": 20, "gpa": 3.8, "major": "Computer Science"},
        {"name": "Bob Smith", "email": "bob@university.edu", "age": 22, "gpa": 3.5, "major": "Mathematics"},
        {"name": "Carol White", "email": "carol@university.edu", "age": 19, "gpa": 3.9, "major": "Computer Science"},
        {"name": "David Brown", "email": "david@university.edu", "age": 21, "gpa": 3.2, "major": "Physics"},
        {"name": "Eve Davis", "email": "eve@university.edu", "age": 20, "gpa": 3.7, "major": "Mathematics"},
        {"name": "Frank Miller", "email": "frank@university.edu", "age": 23, "gpa": 2.9, "major": "Computer Science"},
    ]
    
    for student in students_data:
        Student.insert(**student)
    
    print(f"✓ Inserted {len(students_data)} students")
    
    # Insert courses
    courses_data = [
        {"code": "CS101", "name": "Introduction to Programming", "credits": 4, "instructor": "Dr. Smith"},
        {"code": "CS201", "name": "Data Structures", "credits": 4, "instructor": "Dr. Johnson"},
        {"code": "CS301", "name": "Algorithms", "credits": 3, "instructor": "Dr. Williams"},
        {"code": "MATH201", "name": "Calculus II", "credits": 4, "instructor": "Dr. Brown"},
        {"code": "MATH301", "name": "Linear Algebra", "credits": 3, "instructor": "Dr. Davis"},
        {"code": "PHYS101", "name": "Physics I", "credits": 4, "instructor": "Dr. Wilson"},
    ]
    
    for course in courses_data:
        Course.insert(**course)
    
    print(f"✓ Inserted {len(courses_data)} courses")
    
    # Insert registrations
    registrations_data = [
        # Alice's courses (student_id=1)
        {"student_id": 1, "course_id": 1, "semester": "Fall 2025", "grade": "A"},
        {"student_id": 1, "course_id": 2, "semester": "Fall 2025", "grade": "A-"},
        {"student_id": 1, "course_id": 4, "semester": "Spring 2026", "grade": None},
        
        # Bob's courses (student_id=2)
        {"student_id": 2, "course_id": 4, "semester": "Fall 2025", "grade": "B+"},
        {"student_id": 2, "course_id": 5, "semester": "Fall 2025", "grade": "A"},
        {"student_id": 2, "course_id": 3, "semester": "Spring 2026", "grade": None},
        
        # Carol's courses (student_id=3)
        {"student_id": 3, "course_id": 1, "semester": "Fall 2025", "grade": "A"},
        {"student_id": 3, "course_id": 2, "semester": "Spring 2026", "grade": None},
        {"student_id": 3, "course_id": 5, "semester": "Spring 2026", "grade": None},
        
        # David's courses (student_id=4)
        {"student_id": 4, "course_id": 6, "semester": "Fall 2025", "grade": "B"},
        {"student_id": 4, "course_id": 4, "semester": "Fall 2025", "grade": "B-"},
        
        # Eve's courses (student_id=5)
        {"student_id": 5, "course_id": 4, "semester": "Fall 2025", "grade": "A"},
        {"student_id": 5, "course_id": 5, "semester": "Spring 2026", "grade": None},
        
        # Frank's courses (student_id=6)
        {"student_id": 6, "course_id": 1, "semester": "Fall 2025", "grade": "B-"},
        {"student_id": 6, "course_id": 2, "semester": "Spring 2026", "grade": None},
    ]
    
    for registration in registrations_data:
        Registration.insert(**registration)
    
    print(f"✓ Inserted {len(registrations_data)} registrations\n")


def print_results(title: str, results: list):
    """Pretty print query results."""
    print(f"{'=' * 80}")
    print(f"📊 {title}")
    print(f"{'=' * 80}")
    
    if not results:
        print("  (No results)\n")
        return
    
    for i, record in enumerate(results, 1):
        print(f"\n  {i}. {record}")
    
    print(f"\n  Total: {len(results)} record(s)\n")


def run_sample_queries():
    """Execute sample queries to demonstrate database functionality."""
    print("\n" + "=" * 80)
    print("🔍 RUNNING SAMPLE QUERIES")
    print("=" * 80 + "\n")
    
    # Query 1: All students
    print_results(
        "Query 1: All Students",
        Student.select()
    )
    
    # Query 2: Students with GPA > 3.5
    print_results(
        "Query 2: Students with GPA > 3.5",
        Student.select(where=lambda s: s['gpa'] > 3.5)
    )
    
    # Query 3: Computer Science majors
    print_results(
        "Query 3: Computer Science Majors",
        Student.select(where=lambda s: s['major'] == "Computer Science")
    )
    
    # Query 4: All courses sorted by credits (descending)
    print_results(
        "Query 4: Courses Ordered by Credits (Descending)",
        Course.select(order_by='-credits')
    )
    
    # Query 5: Courses with 4 credits
    print_results(
        "Query 5: 4-Credit Courses",
        Course.select(where=lambda c: c['credits'] == 4)
    )
    
    # Query 6: Spring 2026 registrations (current semester)
    print_results(
        "Query 6: Spring 2026 Registrations (Current Semester)",
        Registration.select(where=lambda r: r['semester'] == "Spring 2026")
    )
    
    # Query 7: Completed registrations with grades
    print_results(
        "Query 7: Completed Registrations (With Grades)",
        Registration.select(where=lambda r: r['grade'] is not None)
    )
    
    # Query 8: Top 3 students by GPA
    print_results(
        "Query 8: Top 3 Students by GPA",
        Student.select(order_by='-gpa', limit=3)
    )
    
    # Query 9: Young students (age <= 20)
    print_results(
        "Query 9: Students Age 20 or Younger",
        Student.select(where=lambda s: s['age'] <= 20, order_by='age')
    )
    
    # Query 10: CS courses (course codes starting with 'CS')
    print_results(
        "Query 10: Computer Science Courses",
        Course.select(where=lambda c: c['code'].startswith('CS'))
    )


def run_update_operations():
    """Demonstrate UPDATE operations."""
    print("\n" + "=" * 80)
    print("✏️  RUNNING UPDATE OPERATIONS")
    print("=" * 80 + "\n")
    
    # Update 1: Assign grade to a registration
    print("Update 1: Assigning grade to Alice's Calculus II course...")
    count = Registration.update(
        where=lambda r: r['student_id'] == 1 and r['course_id'] == 4,
        grade='A'
    )
    print(f"  ✓ Updated {count} record(s)\n")
    
    # Update 2: Update a student's major
    print("Update 2: Changing Frank's major to Data Science...")
    count = Student.update(
        where=lambda s: s['name'] == "Frank Miller",
        major="Data Science"
    )
    print(f"  ✓ Updated {count} record(s)\n")
    
    # Update 3: Increase credits for a course
    print("Update 3: Increasing credits for CS301 (Algorithms) from 3 to 4...")
    count = Course.update(
        where=lambda c: c['code'] == 'CS301',
        credits=4
    )
    print(f"  ✓ Updated {count} record(s)\n")
    
    # Verify updates
    print_results(
        "Verification: Alice's Updated Registrations",
        Registration.select(where=lambda r: r['student_id'] == 1)
    )
    
    print_results(
        "Verification: Frank's Updated Profile",
        Student.select(where=lambda s: s['name'] == "Frank Miller")
    )
    
    print_results(
        "Verification: Updated CS301 Course",
        Course.select(where=lambda c: c['code'] == 'CS301')
    )


def show_statistics():
    """Display database statistics."""
    print("\n" + "=" * 80)
    print("📈 DATABASE STATISTICS")
    print("=" * 80 + "\n")
    
    print(f"  Total Students:      {Student.count()}")
    print(f"  Total Courses:       {Course.count()}")
    print(f"  Total Registrations: {Registration.count()}")
    
    # Calculate some interesting stats
    cs_majors = len(Student.select(where=lambda s: s['major'] == "Computer Science"))
    print(f"  CS Majors:           {cs_majors}")
    
    completed = len(Registration.select(where=lambda r: r['grade'] is not None))
    print(f"  Completed Courses:   {completed}")
    
    spring_2026 = len(Registration.select(where=lambda r: r['semester'] == "Spring 2026"))
    print(f"  Spring 2026 Enrollments: {spring_2026}")
    
    print()


def main():
    """Main function to run the example."""
    print("\n" + "=" * 80)
    print("🎓 STUDENT COURSE REGISTRATION SYSTEM")
    print("     In-Memory Database Example")
    print("=" * 80 + "\n")
    
    # Initialize with sample data
    seed_data()
    
    # Show initial statistics
    show_statistics()
    
    # Run sample queries
    run_sample_queries()
    
    # Demonstrate updates
    run_update_operations()
    
    # Show final statistics
    show_statistics()
    
    print("=" * 80)
    print("✅ Example completed successfully!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
