# app/routes/jobs.py
from fastapi import APIRouter
from backend.database import get_jobs

router = APIRouter()

@router.get("/")
async def fetch_jobs():
    jobs = await get_jobs()
    return {"jobs": jobs}
