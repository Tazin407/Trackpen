from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# Backward compatibility alias
UserSchema = UserCreate


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class TokenRefresh(BaseModel):
    refresh_token: str


class MessageResponse(BaseModel):
    message: str
