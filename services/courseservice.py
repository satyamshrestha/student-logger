from models.student import Student
from models.course import Course
from utils.exceptions import AppException
from db.redis import redis_client

class CourseService:
    def add_course(self, db, data):
        student = db.query(Student).filter(Student.student_id == data.student_id).first()
        if not student:
            raise AppException("Student with the given ID does not exist", 404)
        course = Course(**data.model_dump())
        
        db.add(course)
        db.commit()
        db.refresh(course)
        redis_client.flushdb()
        return course