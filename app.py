from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from models.student import Student
from models.course import Course
from models.user import User
from services.studentservice import StudentService
from schemas.student_schema import StudentQuery, StudentCreate, StudentUpdate, StudentResponse, CourseCreate, CourseResponse, UserCreate, UserLogin
from services.courseservice import CourseService
from utils.security import hash_password, verify_password
from utils.jwt import create_access_token
from db.database import Base, engine
from db.deps import get_db

app = FastAPI()
Base.metadata.create_all(engine)
service = StudentService()

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/signup")
def signup(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user = User(username=data.username, password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully!"}

@app.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})

    return {"access_token": token}

@app.post("/students", status_code=201, response_model=StudentResponse)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    try:
        student = Student(**data.model_dump())
        return service.add_student(db, student)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db), query: StudentQuery = Depends()):
    return service.get_all_students(db, query)

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