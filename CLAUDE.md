# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common commands

### Backend service (FastAPI)
```
# install deps
pip install -r server_backend/src/requirements.txt

# start Postgres (reads .env in server_backend/docker)
docker compose -f server_backend/docker/docker-compose.yml --env-file server_backend/docker/.env.example up -d postgres

# run API (serves upload, static index and /videos)
cd server_backend/src
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Collector on Raspberry Pi
```
# install deps
pip install -r collector_pi/requirements.txt

# run capture loop
python collector_pi/src/capture_upload.py
```
Systemd unit template lives in `collector_pi/systemd/`.

### Timelapse generation (manual CLI)
```
./scripts/timelapse.py                 # defaults to last 1 h   5 s @24 fps
./scripts/timelapse.py --start ISO --end ISO --fps 30 --duration 10
```
Output videos stored under `$STORAGE_ROOT/videos/` and automatically exposed at `http://<server>:8000/videos/<file>.mp4`.

## Repository layout & architecture

```
collector_pi/
  src/               capture & upload loop (ffmpeg via V4L2)
  requirements.txt   Pi-side deps
  systemd/           service definition

server_backend/
  src/
    main.py          FastAPI app
    db.py            SQLAlchemy async models (Postgres, timestamptz)
    video.py         Timelapse builder (ffmpeg concat)
    config.py        env-driven settings
  docker/            docker-compose + .env.example for Postgres
  static/            index.html (lists videos)

scripts/timelapse.py  project-root helper CLI
```

Key runtime directories are derived from `STORAGE_ROOT` env (default `/data/plantcam`):
* raw images   `$STORAGE_ROOT/raw/YYYY/MM/DD/`  
* generated videos   `$STORAGE_ROOT/videos/`

## Testing hints
No automated tests yet.  Add pytest under `server_backend/tests/` and target async FastAPI routes.

## Development Guidance
- Claude should apply file changes directly rather than asking the user to edit files manually.
- When a task if finished or a broad task is asked where multiple steps are required, suggest the next step to implement to keep development focused.
- When suggesting edits, make a quick description of what the change is simply.  
- Prefer adding dependencies using package manager CLIs over modifying dependency files when possible.

- Always keep the todo list up to updated. When finishing a task or about to start one, update the todo list.

```