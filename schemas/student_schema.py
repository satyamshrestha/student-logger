from pydantic import BaseModel

class StudentCreate(BaseModel):
    student_id: str
    name: str
    age: int

class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None

class StudentResponse(BaseModel):
    student_id: str
    name: str
    age: int
    courses: list[CourseResponse] = []

    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    course_id: str
    title: str
    student_id: str

class CourseResponse(BaseModel):
    course_id: str
    title: str

    class Config:
        from_attributes = True