from services.studentservice import StudentService
from services.courseservice import CourseService

def get_student_service():
    return StudentService()

def get_course_service():
    return CourseService()