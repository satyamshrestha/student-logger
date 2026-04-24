from models.student import Student
from services.studentmanager import StudentManager

def main():
    print("Starting Student Management System...")
    manager = StudentManager()
    try:
        manager.load_from_file()
        print("Started Student Management System!")
    except ValueError as e:
        print(f"Warning: {e}")
        print("Starting with empty data...")

    while True:
        show_menu()
        choice = input("Enter choice: ").strip().lower()
        should_continue = handle_choice(choice, manager)

        if should_continue is False:
            break

def show_menu():
    print("\n--- Student Management System ---")
    print("1. Add Student")
    print("2. View Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Exit")

def handle_choice(choice, manager):
    if choice == "1":
        handle_add(manager)

    elif choice == "2":
        handle_view(manager)

    elif choice == "3":
        handle_update(manager)

    elif choice == "4":
        handle_delete(manager)

    elif choice == "5":
        manager.save_to_file()
        print("Exiting...")
        return False
    else:
        print("Invalid choice! *Choose (1, 2, 3, 4 or 5)*")

def handle_add(manager):
    try:
        student_id = input("Enter the student id: ").strip()
        name = get_valid_name("Enter the student's name:\n")        
        age = get_valid_age("Enter the student's age:\n")
        manager.add_student(Student(student_id, name, age))
        manager.save_to_file()
        print("Student added!")
    
    except ValueError as e:
        print(f"Error: {e}")
    

def handle_view(manager):
    students = manager.get_all_students()

    if not students:
        print("No students found")
        return

    for s in students:
        print(f"ID: {s.student_id} | Name: {s.name} | Age: {s.age}")

def handle_update(manager):
    student_id = input("Enter the ID of student you want to update: ").strip()
    while True:
        choice = input("What do you want to update?\n1. Name\n2. Age\n3. Both\n4. Abort\n").strip().lower()
        if choice in ("1", "name"):
            name = get_valid_name("Enter the new name:\n")
            try:
                student = manager.update_student(student_id, name=name)
                print(f"Name Updated Successfully!\nID={student.student_id}, Name={student.name}, Age={student.age}")
                manager.save_to_file()
                break
            except ValueError as e:
                print(f"Error: {e}")

        elif choice in ("2", "age"):
            try:
                age = get_valid_age("Enter the new age:\n")
                student = manager.update_student(student_id, age=age)
                print(f"Age Updated Successfully!\nID={student.student_id}, Name={student.name}, Age={student.age}")
                manager.save_to_file()
                break
            except ValueError as e:
                print(f"Error: {e}")

        elif choice in ("3", "both"):
            name = get_valid_name("Enter the new name:\n")
            age = get_valid_age("Enter the new age:\n")
            try:
                student = manager.update_student(student_id, name=name, age=age)
                print(f"Name and Age Updated Successfully!\nID={student.student_id}, Name={student.name}, Age={student.age}")
                manager.save_to_file()
                break
            except ValueError as e:
                print(f"Error: {e}")

        elif choice in ("4", "abort"):
            print("Aborting...")
            break

        else:
            print("Invalid choice!")

def handle_delete(manager):
    student_id = input("Enter the ID of the student you want to delete: ").strip()
    while True:
        confirm = input("Are you sure you want to delete? (Y/n):\n")
        if confirm.strip().lower() == "y":
            try:
                manager.delete_student(student_id)
                manager.save_to_file()
                print(f"Student with ID {student_id} deleted successfully!")
            except ValueError as e:
                print(f"Error: {e}")
            break

        elif confirm.strip().lower() == "n":
            print("Operation Cancelled!")
            break
        
        else:
            print("Enter Y/n.")

def get_valid_age(prompt):
    while True:
        try:    
            return int(input(prompt))
        except ValueError:
            print("Age must be an integer!")

def get_valid_name(prompt):
    while True:
        name = input(prompt).strip()
        if name:
            return name
        print("Name cannot be empty!")

if __name__ == "__main__":
    main()