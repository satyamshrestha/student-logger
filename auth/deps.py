from fastapi.security import HTTPBearer
from jose import JWTError
from fastapi import Depends, HTTPException
from utils.jwt import settings
from jose import jwt

security = HTTPBearer()

def get_current_user(token = Depends(security)):
    try:
        payload = jwt.decode(
            token.credentials, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        if not payload.get("sub"):
            raise HTTPException(status_code=401, detail="Invalid token payload!")

        if payload.get("token_type") != "access":
            raise HTTPException(
                status_code=401,
                detail="Invalid access token"
            )

        if not payload.get("role"):
            raise HTTPException(
                status_code=401,
                detail="Role missing in token!"
            )
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token!")
    
    return {
        "username": payload.get("sub"),
        "role": payload.get("role")
    }