from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base

# class User(BaseModel):
#     id: int
#     username: str | None = None
#     email: EmailStr
#     hashed_password: str
#     created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class User(Base):
    __tablename__="users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    refresh_token = Column(String, nullable=True)
