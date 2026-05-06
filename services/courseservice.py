from models.student import Student
from models.course import Course

class CourseService:
    def add_course(self, db, data):
        student = db.query(Student).filter(Student.student_id == course.student_id).first()
        if not student:
            raise ValueError("Student with the given ID does not exist")
        course = Course(**data.model_dump())
        
        db.add(course)
        db.commit()
        db.refresh(course)
        return course