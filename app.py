from fastapi import FastAPI, HTTPException
from models.student import Student
from services.studentmanager import StudentManager
from schemas.student_schema import StudentCreate, StudentUpdate

app = FastAPI()
manager = StudentManager()
try:    
    print("Started Student Management System!")
    manager.load_from_file()
except ValueError:
    print("Starting with an empty JSON file!")

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/students", status_code=201)
def create_student(data: StudentCreate):
    try:
        manager.add_student(Student(data.student_id, data.name, data.age))
        manager.save_to_file()
        return {
            "message": "Student created successfully!",
            "student": data
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/students")
def get_students():
    students = manager.get_all_students()
    return [s.to_dict() for s in students]

@app.get("/students/{student_id}")
def get_student(student_id: str):
    try:
        student = manager.find_student(student_id)
        if not student:
            raise ValueError("Student not found")
        return student.to_dict()
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/students/count")
def get_student_count():
    return {"count": len(manager.get_all_students())}

@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    try:
        manager.delete_student(student_id)
        manager.save_to_file()
        return {"message": "Deleted student successfully!"}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.put("/students/{student_id}", status_code=200)
def update_student(student_id: str, data: StudentUpdate):
    try:
        student = manager.update_student(
            student_id, 
            name=data.name, 
            age=data.age
        )
        manager.save_to_file()
        return {"message": "Student Updated Successfully",
                "student": student.to_dict()
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))