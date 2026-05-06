from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.deps import get_db
from models.user import User
from schemas.student_schema import UserCreate, UserLogin
from utils.exceptions import AppException
from utils.security import hash_password, verify_password
from utils.jwt import create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.username == data.username).first():
        raise AppException(f"User {data.username} already exists!", 400)
    user = User(
        username=data.username,
        password=hash_password(data.password),
        role="student"
    )
    db.add(user)
    db.commit()
    db.refresh()
    return {"message": "User created successfully!"}

@router.post("/login")
def login(
    data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password):
        raise AppException("Invalid credentials", 401)

    token = create_access_token({"sub": user.username, "role": user.role})

    return {"access_token": token}