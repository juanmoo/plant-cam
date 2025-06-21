from fastapi import APIRouter, BackgroundTasks, HTTPException
from datetime import datetime
from tasks import generate_timelapse

router = APIRouter()

@router.post("/api/timelapse")
async def create_job(start: str, end: str, fps: int = 24, duration: int | None = 5):
    try:
        datetime.fromisoformat(start)
        datetime.fromisoformat(end)
    except ValueError:
        raise HTTPException(status_code=400, detail="bad datetime format")
    task = generate_timelapse.delay(start, end, fps, duration)
    return {"job_id": task.id}

@router.get("/api/timelapse/{job_id}")
async def job_status(job_id: str):
    task = generate_timelapse.AsyncResult(job_id)
    if task.state == "SUCCESS":
        return {"status": "done", "video": task.result}
    return {"status": task.state.lower()}
