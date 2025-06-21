from celery import Celery
import os
from datetime import datetime
from video import build_timelapse

celery_app = Celery(
    "plantcam",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1"),
)

@celery_app.task
def generate_timelapse(start_iso: str, end_iso: str, fps: int, duration: int | None):
    start = datetime.fromisoformat(start_iso)
    end = datetime.fromisoformat(end_iso)
    path = build_timelapse(start, end, fps, duration)
    return str(path)
