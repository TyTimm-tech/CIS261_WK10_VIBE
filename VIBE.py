"""
Student Grade Calculator
Manages student records including test scores and calculates grades.
"""

import os
import sys
from datetime import datetime


class Student:
    """Represents a student with test scores and calculated grades."""
    
    def __init__(self, name, student_id, test1, test2, test3):
        """Initialize a student with name, ID, and three test scores."""
        self.name = name
        self.id = student_id
        self.test1 = float(test1)
        self.test2 = float(test2)
        self.test3 = float(test3)
        self.average = self.calculate_average()
        self.grade = self.calculate_grade()
    
    def calculate_average(self):
        """Calculate the average of three test scores."""
        return (self.test1 + self.test2 + self.test3) / 3
    
    def calculate_grade(self):
        """Calculate letter grade based on average score."""
        avg = self.average
        if avg >= 90:
            return 'A'
        elif avg >= 80:
            return 'B'
        elif avg >= 70:
            return 'C'
        elif avg >= 60:
            return 'D'
        else:
            return 'F'
    
    def to_string(self):
        """Return student data as pipe-delimited string."""
        return f"{self.name}|{self.id}|{self.test1:.2f}|{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}"
    
    @staticmethod
    def from_string(data_string):
        """Create a Student object from pipe-delimited string."""
        parts = data_string.strip().split('|')
        if len(parts) >= 5:
            return Student(parts[0], parts[1], parts[2], parts[3], parts[4])
        return None


def load_students(filename='student_grades.txt'):
    """Load student records from file."""
    students = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    student = Student.from_string(line)
                    if student:
                        students.append(student)
            print(f"✓ Loaded {len(students)} student records from {filename}")
        except IOError as e:
            print(f"✗ Error reading file: {e}")
    else:
        print(f"No existing records found. Starting with empty list.")
    
    return students


def save_students(students, filename='student_grades.txt'):
    """Save student records to file."""
    try:
        with open(filename, 'w') as file:
            for student in students:
                file.write(student.to_string() + '\n')
        print(f"✓ Saved {len(students)} student records to {filename}")
        return True
    except IOError as e:
        print(f"✗ Error saving file: {e}")
        return False


def add_student(students):
    """Prompt user to add a new student record."""
    print("\n" + "="*50)
    print("ADD NEW STUDENT")
    print("="*50)
    
    try:
        name = input("Enter student name: ").strip()
        if not name:
            print("✗ Student name cannot be empty.")
            return
        
        student_id = input("Enter student ID: ").strip()
        if not student_id:
            print("✗ Student ID cannot be empty.")
            return
        
        # Get test scores with validation
        test_scores = []
        for i in range(1, 4):
            while True:
                try:
                    score = float(input(f"Enter Test {i} score (0-100): "))
                    if 0 <= score <= 100:
                        test_scores.append(score)
                        break
                    else:
                        print("✗ Score must be between 0 and 100.")
                except ValueError:
                    print("✗ Please enter a valid number.")
        
        # Create and add student
        student = Student(name, student_id, test_scores[0], test_scores[1], test_scores[2])
        students.append(student)
        print(f"\n✓ Student '{student.name}' added successfully!")
        print(f"  Average: {student.average:.2f}, Grade: {student.grade}")
        
    except KeyboardInterrupt:
        print("\n✗ Operation cancelled.")


def display_all_students(students):
    """Display all students in a formatted table."""
    if not students:
        print("\n✗ No student records to display.")
        return
    
    print("\n" + "="*100)
    print("ALL STUDENT RECORDS")
    print("="*100)
    print(f"{'Name':<20} {'Student ID':<12} {'Test 1':<10} {'Test 2':<10} {'Test 3':<10} {'Average':<10} {'Grade':<8}")
    print("-"*100)
    
    for student in students:
        print(f"{student.name:<20} {student.id:<12} {student.test1:<10.2f} {student.test2:<10.2f} {student.test3:<10.2f} {student.average:<10.2f} {student.grade:<8}")
    
    print("="*100)


def search_student(students):
    """Search for a student by name (case-insensitive)."""
    print("\n" + "="*50)
    print("SEARCH STUDENT")
    print("="*50)
    
    search_name = input("Enter student name to search: ").strip().lower()
    
    if not search_name:
        print("✗ Search term cannot be empty.")
        return
    
    found = [s for s in students if s.name.lower() == search_name]
    
    if found:
        print(f"\n✓ Found {len(found)} match(es):")
        print(f"{'Name':<20} {'Student ID':<12} {'Test 1':<10} {'Test 2':<10} {'Test 3':<10} {'Average':<10} {'Grade':<8}")
        print("-"*90)
        for student in found:
            print(f"{student.name:<20} {student.id:<12} {student.test1:<10.2f} {student.test2:<10.2f} {student.test3:<10.2f} {student.average:<10.2f} {student.grade:<8}")
    else:
        print(f"✗ No student found with name '{search_name}'.")


def calculate_statistics(students):
    """Calculate and display class statistics."""
    if not students:
        print("\n✗ No student records available for statistics.")
        return
    
    averages = [s.average for s in students]
    
    highest = max(students, key=lambda s: s.average)
    lowest = min(students, key=lambda s: s.average)
    class_avg = sum(averages) / len(averages)
    
    print("\n" + "="*50)
    print("CLASS STATISTICS")
    print("="*50)
    print(f"Total Students: {len(students)}")
    print(f"Class Average: {class_avg:.2f}")
    print(f"\nHighest Average: {highest.average:.2f}")
    print(f"  Student: {highest.name} (ID: {highest.id})")
    print(f"\nLowest Average: {lowest.average:.2f}")
    print(f"  Student: {lowest.name} (ID: {lowest.id})")
    print("="*50)


def display_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("STUDENT GRADE CALCULATOR")
    print("="*50)
    print("1. Add new student")
    print("2. Display all students")
    print("3. Search for student")
    print("4. View class statistics")
    print("5. Save and exit (or press ESC)")
    print("="*50)
    print("Enter choice (1-5) or press ESC to exit: ", end="")


def main():
    """Main program loop."""
    print("Starting Student Grade Calculator...")
    students = load_students()
    
    while True:
        try:
            display_menu()
            choice = input().strip().upper()
            
            # Check for ESC key (Ctrl+C will be caught by except)
            if choice == '':
                continue
            
            if choice == '1':
                add_student(students)
            elif choice == '2':
                display_all_students(students)
            elif choice == '3':
                search_student(students)
            elif choice == '4':
                calculate_statistics(students)
            elif choice == '5':
                print("\nSaving records...")
                save_students(students)
                print("✓ Goodbye!")
                break
            else:
                print("✗ Invalid choice. Please enter 1-5.")
        
        except KeyboardInterrupt:
            print("\n\nSaving records before exit...")
            save_students(students)
            print("✓ Goodbye!")
            break
        except Exception as e:
            print(f"✗ An error occurred: {e}")


if __name__ == "__main__":
    main()