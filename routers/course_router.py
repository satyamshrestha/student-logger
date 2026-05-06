from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.student_schema import CourseCreate, CourseResponse
from db.deps import get_db
from services.courseservice import CourseService
from services.deps import get_course_service
from auth.permissions import require_permission

router = APIRouter(prefix="/courses", tags=["Course"])

@router.post("", response_model=CourseResponse)
def create_course(
    data: CourseCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_permission("create")),
    service: CourseService = Depends(get_course_service)
):
    return service.add_course(db, data)

# MORE TO COME JUST LIKE STUDENT SERVICES.