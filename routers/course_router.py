from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from schemas.student_schema import CourseCreate, CourseResponse
from db.deps import get_db
from services.courseservice import CourseService
from services.deps import get_course_service
from auth.permissions import require_permission
from utils.rate_limiter import limiter

router = APIRouter(prefix="/courses", tags=["Course"])

@router.post("", response_model=CourseResponse)
@limiter.limit("30/minute")
def create_course(
    request: Request,
    data: CourseCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_permission("create")),
    service: CourseService = Depends(get_course_service)
):
    return service.add_course(db, data)

@router.get("", response_model=list[CourseResponse])
@limiter.limit("100/minute")
def view_all_courses(
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Depends(require_permission("read")),
    service: CourseService = Depends(get_course_service)
):
    return service.get_all_courses(db)
# MORE CRUD FEATURES TO COME