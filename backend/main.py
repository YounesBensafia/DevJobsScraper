from fastapi import FastAPI
from backend.database import get_jobs  # must match your folder structure

app = FastAPI()

@app.get("/jobs")
async def read_jobs():
    jobs = await get_jobs()
    return {"jobs": jobs}