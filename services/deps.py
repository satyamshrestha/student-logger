from services.studentservice import StudentService
from services.courseservice import CourseService
from services.userservice import UserService

def get_student_service():
    return StudentService()

def get_course_service():
    return CourseService()

def get_user_service():
    return UserService()