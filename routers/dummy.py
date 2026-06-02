from fastapi import APIRouter, HTTPException, Depends, status
from core.utils import get_current_user

private_router = APIRouter(prefix="/private", tags=["private"], dependencies=[Depends(get_current_user)])

@private_router.get("/hello", summary="A dummy endpoint to test authentication")
def hello():
    return {"message": "Hello, authenticated user!"}