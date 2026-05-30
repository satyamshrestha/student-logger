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

class CourseResponse(BaseModel):
    course_id: str
    title: str

    class Config:
        from_attributes = True

class StudentResponse(BaseModel):
    student_id: str
    name: str
    age: int
    courses: list[CourseResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    course_id: str
    title: str
    student_id: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class RoleUpdate(BaseModel):
    role: Literal["admin", "teacher", "student"]

class RefreshTokenRequest(BaseModel):
    refresh_token: str