from fastapi import APIRouter, Depends, Request, BackgroundTasks
from sqlalchemy.orm import Session

from models.user import User
from db.deps import get_db
from utils.exceptions import AppException
from auth.deps import get_current_user
from auth.permissions import require_permission
from schemas.student_schema import RoleUpdate
from services.userservice import UserService
from services.deps import get_user_service
from utils.rate_limiter import limiter
from utils.audit import log_action

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
@limiter.limit("100/minute")
def get_me(request: Request, user: dict = Depends(get_current_user)):
    return user

@router.get("")
@limiter.limit("100/minute")
def get_all_users(
    request: Request,
    user: dict = Depends(require_permission("admin_only")),
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    return service.get_all_users(db)

@router.put("/{username}/role")
@limiter.limit("30/minute")
def update_role(
    request: Request,
    username: str,
    data: RoleUpdate,
    background_tasks: BackgroundTasks,
    user: dict = Depends(require_permission("admin_only")),
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    background_tasks.add_task(
        log_action,
        f"Admin updated the role of {user} to {user.role}."
    )
    return service.update_role(db, username, data)