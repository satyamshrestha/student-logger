from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "max-emilian-verstappen-1997" # In production, use a secure method to store this key i.e. dotenv files
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)