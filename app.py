from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models.student import Student
from models.course import Course
from services.studentservice import StudentService
from schemas.student_schema import StudentCreate, StudentUpdate, StudentResponse, CourseCreate, CourseResponse
from services.courseservice import CourseService
from db.database import Base, engine
from db.deps import get_db

app = FastAPI()
Base.metadata.create_all(engine)
service = StudentService()

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/students", status_code=201, response_model=StudentResponse)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    try:
        student = Student(**data.model_dump())
        return service.add_student(db, student)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return service.get_all_students(db)

@app.get("/students/count")
def get_student_count(db: Session = Depends(get_db)):
    return {"count": service.count_students(db)}

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, db: Session = Depends(get_db)):
    try:
        student = service.find_student(db, student_id)
        if not student:
            raise ValueError("Student not found")
        return student
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/students/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    try:
        service.delete_student(db, student_id)
        return {"message": "Deleted student successfully!"}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.put("/students/{student_id}", status_code=200, response_model=StudentResponse)
def update_student(student_id: str, data: StudentUpdate, db: Session = Depends(get_db)):
    try:
        return service.update_student(
            db,
            student_id, 
            name=data.name, 
            age=data.age
        )
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@app.post("/courses", response_model=CourseResponse)
def create_course(data: CourseCreate, db: Session = Depends(get_db)):
    try:
        course = Course(**data.model_dump())
        return CourseService().add_course(db, course)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))