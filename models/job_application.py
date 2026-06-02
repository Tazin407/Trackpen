from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from db.database import Base
from models.users import User

class Status(Enum):
    APPLIED = "APPLIED"
    INTERVIEWING = "INTERVIEWING"
    OFFERED = "OFFERED"
    REJECTED = "REJECTED"

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value == value.upper():
                return member

class JobApplication(Base):
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user = relationship("User", backref="job_applications")

    company_name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    status = Column(SqlEnum(Status), default=Status.APPLIED.value)    
    notes = Column(String, nullable=True)

    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)