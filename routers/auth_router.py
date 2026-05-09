from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.deps import get_db
from models.user import User
from schemas.student_schema import UserCreate, UserLogin
from utils.exceptions import AppException
from utils.security import hash_password, verify_password
from utils.jwt import create_access_token
from utils.logger import logger


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
    db.refresh(user)
    return {"message": "User created successfully!"}

@router.post("/login")
def login(
    data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == data.username).first()
    logger.info(f"Login attempt for user: {data.username}.")

    if not user or not verify_password(data.password, user.password):
        logger.warning(f"Failed login attempt for user: {data.username}.")
        raise AppException("Invalid credentials!", 401)
    
    logger.info(f"User {user.username} logged in successfully.")

    token = create_access_token({"sub": user.username, "role": user.role})

    return {"access_token": token}