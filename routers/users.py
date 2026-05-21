from fastapi import APIRouter
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.users import User
from schemas.user_schema import UserSchema, UserOut, UserAuth
from db.database import get_db
from core.utils import get_hashed_password, create_access_token, create_refresh_token, verify_password
from fastapi import Depends

router = APIRouter()

@router.get("/users/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.post("/create_users/", summary="Create new user", response_model=UserOut)
def create_user(data:UserSchema, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(select(User).where(User.email == data.email)).first()
    if result:
        return {"message": "User already exists"}
    hashed_pass = get_hashed_password(data.password)
    user = User(
    **data.model_dump(exclude={"password", "created_at"}),
    hashed_password=hashed_pass)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



    
    
    