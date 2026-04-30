from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: int
    username: str | None = None
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))