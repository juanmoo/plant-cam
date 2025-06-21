# server_backend d Image Storage, API, and Video Generator

## Purpose
Receive images from Pi devices, store efficiently, and generate timelapse videos on-demand via REST API.

## Tech Stack
- Python 3.11
- FastAPI
- Uvicorn (ASGI server)
- PostgreSQL (metadata)
- FFmpeg (via `ffmpeg-python`)
- Redis (task queue)

## Directory Layout
```
server_backend/
  src/
    main.py          # FastAPI app
    db.py            # SQLAlchemy models
    storage.py       # Filesystem ops
    video.py         # timelapse assembly
    tasks.py         # Celery/Redis workers
    config.py
 tests/
 SPEC.md
```

## Storage Scheme
- Root data dir `/data/plantcam/raw/YYYY/MM/DD/*.jpg`.
- Generated videos `/data/plantcam/videos/<hash>.mp4` cached.
- DB table `images(id, device_id, path, taken_at)` indexed.

## API
| Method | Path | Body/Params | Response |
|--------|------|-------------|----------|
| POST   | /api/upload | multipart images[] | 200 JSON `{stored:[]}` |
| GET    | /api/images | `start`, `end` | JSON list metadata |
| POST   | /api/timelapse | JSON `{start,end,fps,duration}` | 202 job id |
| GET    | /api/timelapse/{job_id} | - | 200 video or 202 pending |

## Timelapse Generation Logic
1. Validate range.
2. Query `images` to list files.
3. Sample N frames to meet `fps*duration` using uniform step.
4. Use FFmpeg: `ffmpeg -r <fps> -pattern_type glob -i 'frames/*.jpg' -c:v libx264 -pix_fmt yuv420p output.mp4`.
5. Store/caches video; DB table `videos(id, hash, params, path, created_at)`.
6. Async via Celery worker.

## Integration w/ collector_pi
- Accepts upload schema described there.
- Sends 200 JSON; path stored in DB.

## Security
- Network limited to LAN; no auth.
- Validate image mime-types and size (<5 MB).

## Testing
- Pytest for API routes & FFmpeg pipeline (mock subprocess).
- Load test concurrent timelapse requests.
