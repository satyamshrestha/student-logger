from student import Student
from studentmanager import StudentManager

# Loading before adding
manager = StudentManager()

manager.load_from_file("student.json")

manager.add_student(Student(1, "A", 20))
manager.add_student(Student(2, "B", 22))

manager.update_student(1, age=25)
manager.delete_student(2)

manager.save_to_file("student.json")

result = manager.update_student(1, age=30)

if result:
    print(result.to_dict())