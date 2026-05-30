from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from db.deps import get_db
from models.user import User
from schemas.student_schema import UserCreate, UserLogin, RefreshTokenRequest
from utils.exceptions import AppException
from utils.security import hash_password, verify_password
from utils.jwt import create_access_token, create_refresh_token
from utils.logger import logger
from utils.rate_limiter import limiter
from utils.config import settings
from tasks import send_welcome_email

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        (User.username == data.username) |
        (User.email == data.email)
    ).first()
    if existing_user:
        raise AppException(f"User already exists!", 409)
    user = User(
        username=data.username,
        email=data.email,
        password=hash_password(data.password),
        role="student"
    )
    send_welcome_email.delay(data.username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully!"}

@router.post("/login")
@limiter.limit("3/minute")
def login(
    request: Request,
    data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == data.username).first()
    logger.info(f"Login attempt for user: {data.username}.")

    if not user or not verify_password(data.password, user.password):
        logger.warning(f"Failed login attempt for user: {data.username}.")
        raise AppException("Invalid credentials!", 401)
    
    logger.info(f"User {user.username} logged in successfully.")

    access_token = create_access_token(
        {
            "sub": user.username,
            "role": user.role
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": user.username,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh_token(
    data: RefreshTokenRequest
):
    try:
        payload = jwt.decode(
            data.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token!"
        )
    if payload.get("token_type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token!"
        )
    
    username = payload.get("sub")
    role = payload.get("role")
    if not username or not role:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token payload!"
        )
    access_token = create_access_token(
        {
            "sub": username,
            "role": role
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }