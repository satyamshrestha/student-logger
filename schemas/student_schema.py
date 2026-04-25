from pydantic import BaseModel

class StudentCreate(BaseModel):
    student_id: str
    name: str
    age: int

class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None