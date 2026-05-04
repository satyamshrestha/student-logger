from fastapi.security import HTTPBearer
from fastapi import Depends
from utils.jwt import SECRET_KEY
from jose import jwt

security = HTTPBearer()

def get_current_user(token = Depends(security)):
    payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
    return payload["sub"]