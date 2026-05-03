from pydantic import BaseModel, Field
from typing import Literal

class StudentQuery(BaseModel):
    age: int | None = None
    min_age: int | None = None
    max_age: int | None = None
    name: str | None = None
    sort: Literal["age", "name"] | None = None
    order: Literal["asc", "desc"] = "asc"
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)

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