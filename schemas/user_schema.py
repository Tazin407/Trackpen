from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone


class UserSchema(BaseModel):
    # id: int
    username: str | None = None
    email: EmailStr
    # hashed_password: str
    password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    
class UserAuth(BaseModel):
    email: EmailStr
    password: str


    