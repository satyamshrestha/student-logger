import json

from db.redis import redis_client
from models.student import Student
from utils.exceptions import AppException

class StudentService():

    def add_student(self, db, data):
        existing_student = db.query(Student).filter(Student.student_id == data.student_id).first()
        if existing_student:
            raise AppException(f"Student with ID {data.student_id} already exists", 400)
        
        student = Student(**data.model_dump())        
        
        db.add(student)
        db.commit()
        db.refresh(student)
        redis_client.delete("all_students")  
        return student 

    def find_student(self, db, student_id: str) -> Student | None:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            raise AppException(f"Student with the id {student_id} not found!", 404)
        return student    

    def update_student(self, db, student_id: str, name=None, age=None):
        if name is None and age is None:
            raise AppException("No update data provided", 400)
        
        student = self.find_student(db, student_id)

        if not student:
            raise AppException(f"Student with ID {student_id} not found", 404)
        
        if name is not None:
            student.name = name
        
        if age is not None:
            student.age = age
        
        db.commit()
        db.refresh(student)
        redis_client.delete("all_students")
        return student
    
    def count_students(self, db):
        return db.query(Student).count()

    def delete_student(self, db, student_id: str):
        student = self.find_student(db, student_id)
        if not student:
            raise AppException(f"Student with ID {student_id} not found!", 404)
        
        db.delete(student)
        db.commit()
        redis_client.delete("all_students")
        return True

    def get_all_students(self, db, query):
        cached_students = redis_client.get("all_students")

        if cached_students:
            return json.loads(cached_students)
        q = db.query(Student)
        # Filtering
        if query.age is not None:
            q = q.filter(Student.age == query.age)
        else:
            if query.min_age is not None:
                q = q.filter(Student.age >= query.min_age)
            if query.max_age is not None:
                q = q.filter(Student.age <= query.max_age)
        if query.name is not None:
            q = q.filter(Student.name.ilike(f"%{query.name}%"))
        
        # Sorting
        if query.sort == "age":
            if query.order == "desc":
                q = q.order_by(Student.age.desc())
            else: 
                q = q.order_by(Student.age)
    
        # Pagination
        students = q.offset(query.offset).limit(query.limit).all()

        redis_client.set(
            "all_students",
            json.dumps([student.to_dict() for student in students])
        )

        return students