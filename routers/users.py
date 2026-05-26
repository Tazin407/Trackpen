from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.users import User
from schemas.user_schema import UserSchema, UserOut, UserAuth, TokenRefresh, MessageResponse
from db.database import get_db
from core.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
    decode_token,
    get_current_user,
    JWT_REFRESH_SECRET_KEY,
)

router = APIRouter(prefix="/auth", tags=["auth"])
# router = APIRouter(prefix="/auth", tags=["auth"], dependencies=[Depends(get_current_user)])


bearer_scheme = HTTPBearer()


@router.post("/register", summary="Create new user", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(data: UserSchema, db: Annotated[Session, Depends(get_db)]):
    if db.execute(select(User).where(User.email == data.email)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if db.execute(select(User).where(User.username == data.username)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=get_hashed_password(data.password),
    )
    user.refresh_token = create_refresh_token(data.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "access_token": create_access_token(user.email),
        "refresh_token": user.refresh_token,
    }


@router.post("/login", summary="User login", response_model=UserOut)
def login(data: UserAuth, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.email == data.email)).scalar_one_or_none()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    refresh_token = create_refresh_token(user.email)
    user.refresh_token = refresh_token
    db.commit()
    return {
        "id": user.id,
        "access_token": create_access_token(user.email),
        "refresh_token": refresh_token,
    }


@router.post("/refresh", summary="Refresh access token", response_model=UserOut)
def refresh_token(data: TokenRefresh, db: Annotated[Session, Depends(get_db)]):
    email = decode_token(data.refresh_token, JWT_REFRESH_SECRET_KEY)
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if not user or user.refresh_token != data.refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    new_refresh_token = create_refresh_token(user.email)
    user.refresh_token = new_refresh_token
    db.commit()
    return {
        "id": user.id,
        "access_token": create_access_token(user.email),
        "refresh_token": new_refresh_token,
    }


@router.post("/logout", summary="User logout", response_model=MessageResponse)
def logout(current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    current_user.refresh_token = None
    db.commit()
    return {"message": "Logged out successfully"}

# @router.get('/all_users', response_model=list[UserOut], summary="Get all users")
# def get_all_users(db: Annotated[Session, Depends(get_db)]):
#     users = db.execute(select(User)).scalars().all()
#     return [UserOut(id=user.id) for user in users]
