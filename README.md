# PlantCam

Automated Plant Photo Timelapse System

## Quick start
A system for capturing, storing, and generating timelapse videos of plant growth using a Raspberry Pi and a local server. The web app allows users to select time intervals and video settings for timelapse creation.

### Backend setup
```bash
# 1. start databases
cd server_backend/docker
cp .env.example .env  # edit if desired
docker compose up -d postgres redis

# 2. install deps and run API
cd ../../src
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

# 3. run Celery worker (new shell)
celery -A tasks.celery_app worker --loglevel=info
```

### Raspberry Pi collector
```bash
pip install -r collector_pi/requirements.txt
python collector_pi/src/capture_upload.py
```

Timelapse jobs can now be requested:
```bash
curl -X POST 'http://SERVER:8000/api/timelapse?start=2025-06-21T00:00:00&end=2025-06-21T01:00:00&fps=24&duration=5'
# => {"job_id":"..."}
```
Poll `/api/timelapse/{job_id}` until status `done` then download from `/videos/<file>.mp4` or visit the web UI at `/`.

---

## Features
- Raspberry Pi data capture & scheduled upload
- Centralized server storage
- Python backend for API and video processing
- Simple frontend for request & download

## Structure
- `/collector_pi/` - Pi-side scripts
- `/server_backend/` - Python backend
- `/frontend/` - Web UI

## See PROJECT_PLAN.md for detailed planning.