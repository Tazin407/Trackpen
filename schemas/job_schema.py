from pydantic import BaseModel
from models.job_application import Status

class CreateJob(BaseModel):
    company_name: str
    position: str
    status: Status | None = None
    notes: str | None = None

class UpdateJob(BaseModel):
    company_name: str | None = None
    position: str | None = None
    status: Status | None = None
    notes: str | None = None

class JobResponse(BaseModel):
    id: int
    company_name: str
    position: str
    status: str
    notes: str | None = None

    class Config:
        from_attributes = True