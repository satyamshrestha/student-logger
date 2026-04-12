import json
from student import Student

class StudentManager():
    def __init__(self):
        self.students = {}

    def add_student(self, student: Student):
        if not isinstance(student, Student):
            raise TypeError("Expected Student object!")
        
        if student.student_id in self.students:
            raise ValueError(f"Student with ID {student.student_id} already exists")
        self.students[student.student_id] = student
        return True

    def find_student(self, student_id: int) -> Student | None:
        return self.students.get(student_id)
    

    def update_student(self, student_id: int, name=None, age=None):
        if name is None and age is None:
            raise ValueError("No update data provided")
        
        student = self.students.get(student_id)

        if not student:
            raise ValueError(f"Student with ID {student_id} not found")
        
        if name is not None:
            student.update_name(name)
        
        if age is not None:
            student.update_age(age)
        
        return student


    def delete_student(self, student_id):
        if student_id not in self.students:
            raise ValueError(f"Student with ID {student_id} not found")
        del self.students[student_id]
        return True
    

    def get_all_students(self):
        return list(self.students.values())
    

    def save_to_file(self, filename):
        data = [s.to_dict() for s in self.students.values()]
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
    

    def load_from_file(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.students = {d["student_id"]: Student.from_dict(d) for d in data}

        except (FileNotFoundError, json.JSONDecodeError):
            self.students = {}