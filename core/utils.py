import os
import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Union, Any
from jose import jwt, JWTError
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import select
from db.database import get_db

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_ACCESS_SECRET_KEY = os.environ["JWT_ACCESS_SECRET_KEY"]
JWT_REFRESH_SECRET_KEY = os.environ["JWT_REFRESH_SECRET_KEY"]

bearer_scheme = HTTPBearer()


def get_hashed_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed_pass: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_pass.encode())


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    expire = _utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return jwt.encode({"sub": str(subject), "exp": expire}, JWT_ACCESS_SECRET_KEY, ALGORITHM)


def create_refresh_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    expire = _utcnow() + (expires_delta or timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
    return jwt.encode({"sub": str(subject), "exp": expire}, JWT_REFRESH_SECRET_KEY, ALGORITHM)


def decode_token(token: str, secret: str) -> str:
    """Decode a JWT and return the subject, or raise 401."""
    try:
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
        subject: str = payload.get("sub")
        if subject is None:
            raise ValueError
        return subject
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    from models.users import User
    email = decode_token(credentials.credentials, JWT_ACCESS_SECRET_KEY)
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found", headers={"WWW-Authenticate": "Bearer"})
    return user
