from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from services.deps import get_student_service
from services.studentservice import StudentService
from schemas.student_schema import StudentCreate, StudentQuery, StudentResponse, StudentUpdate
from db.deps import get_db
from auth.permissions import require_permission

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("", response_model=StudentResponse)
def create_student(
    data: StudentCreate,
    service: StudentService = Depends(get_student_service),
    user: dict = Depends(require_permission("create")),
    db: Session = Depends(get_db)
):
    return service.add_student(db, data)

@router.get("", response_model=list[StudentResponse])
def view_all_students(
    service: StudentService = Depends(get_student_service),
    db: Session = Depends(get_db),
    user: dict = Depends(require_permission("read")),
    query: StudentQuery = Depends()
):
    return service.get_all_students(db, query)

@router.get("/count")
def student_count(
    db: Session = Depends(get_db),
    user: dict = Depends(require_permission("read")),
    service: StudentService = Depends(get_student_service)
):
    return service.count_students(db)

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(require_permission("read")),
    service: StudentService = Depends(get_student_service),
    
):
    return service.find_student(db, student_id)

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: str,
    data: StudentUpdate,
    db: Session = Depends(get_db),
    service: StudentService = Depends(get_student_service),
    user: dict = Depends(require_permission("update"))
):
    return service.update_student(
        db,
        student_id,
        name=data.name,
        age=data.age
    )

@router.delete("/{student_id}")
def delete_student(
    student_id: str,
    user: dict = Depends(require_permission("delete")),
    db: Session = Depends(get_db),
    service: StudentService = Depends(get_student_service)
):
    service.delete_student(db, student_id)
    return {"message": "Deleted successfully"}