from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.database import get_db
from core.utils import get_current_user
from models.job_application import JobApplication, Status
from models.users import User
from schemas.job_schema import CreateJob, UpdateJob, JobResponse

router = APIRouter()

@router.post("/create_job", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(job: CreateJob,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)]
        ):
    job_application = JobApplication(
        user_id=current_user.id,
        company_name=job.company_name,
        position=job.position,
        status=job.status or Status.APPLIED,
        notes=job.notes
    )
    db.add(job_application)
    db.commit()
    db.refresh(job_application) 
    return job_application

@router.get("/get_jobs", response_model=list[JobResponse])
async def get_jobs(
        current_user: Annotated[User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)],
        id: int | None = None,
        company_name: str | None = None,
        position: str | None = None,
        status: Status | None = None
        ):
    if id is not None:
        job = db.execute(select(JobApplication).where(JobApplication.id == id)).scalars().first()
        if not job:
            raise HTTPException(status_code=404, detail="Job application not found")
        return [job]
    query = select(JobApplication).where(JobApplication.user_id == current_user.id)
    if company_name:
        query = query.where(JobApplication.company_name.ilike(f"%{company_name}%"))
    if position:
        query = query.where(JobApplication.position.ilike(f"%{position}%"))
    if status:
        query = query.where(JobApplication.status == status)
    return db.execute(query).scalars().all()


@router.patch("/update_job/{id}", response_model=JobResponse)
async def update_job(
        id: int,
        updates: UpdateJob,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)]
        ):
    job = db.execute(select(JobApplication).where(JobApplication.id == id, JobApplication.user_id == current_user.id)).scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job application not found")
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job


@router.delete("/delete_job/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
        id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)]
        ):
    job = db.execute(select(JobApplication).where(JobApplication.id == id, JobApplication.user_id == current_user.id)).scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job application not found")
    db.delete(job)
    db.commit()

