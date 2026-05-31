from models.student import Student
from models.course import Course
from utils.exceptions import AppException
from utils.cache import invalidate_student_cache

class CourseService:
    def add_course(self, db, data):
        student = db.query(Student).filter(Student.student_id == data.student_id).first()
        if not student:
            raise AppException("Student with the given ID does not exist", 404)
        course = Course(**data.model_dump())
        
        db.add(course)
        db.commit()
        db.refresh(course)
        invalidate_student_cache()
        return course
    
    def get_all_courses(self, db):
        return db.query(Course).all()