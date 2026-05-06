from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.user import User
from db.deps import get_db
from utils.exceptions import AppException
from auth.deps import get_current_user
from auth.permissions import require_permission
from schemas.student_schema import RoleUpdate

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    return user

@router.get("")
def get_all_users(
    user: dict = Depends(require_permission("admin_only")),
    db: Session = Depends(get_db)
):
    return db.query(User).all()

@router.put("/{username}/role")
def update_role(
    username: str,
    data: RoleUpdate,
    user: dict = Depends(require_permission("admin_only")),
    db: Session = Depends(get_db)
):
    target_user = db.query(User).filter(User.username == username).first()

    if not target_user:
        raise AppException("User not found!", 404)

    target_user.role = data.role
    db.commit()

    return {"message": f"{username} role updated to {data.role}!"}