# PlantCam Roadmap

> Mark tasks with `[x]` when completed.

## Phase 1 – MVP
- [x] Pi capture every 10 min and HTTP upload
- [x] Backend endpoint `/api/upload` storing images
- [x] Basic DB schema & filesystem layout
- [x] Manual script to generate timelapse (CLI)
- [x] Serve static index.html allowing manual download

## Phase 2 – Timelapse API & Simple UI
- [x] `/api/timelapse` async video job
- [x] Redis/Celery worker
- [x] Uniform frame sampling algorithm
- [x] Minimal web UI with range pickers & progress

## Phase 3 – Production Hardening
- [x] Systemd service + log rotation on Pi
- [x] Dockerize backend (API + Celery)

## Phase 4 – Next.js React UI
- [ ] Graphical capture histogram with hover count
- [ ] Latest image preview panel
- [ ] Date picker + time slider bound to data range
- [ ] Time-zone selector affects all timestamps
- [ ] Timelapse builder with FPS slider (default 24) and duration input (default 10 s)

## Backlog
- Bulk image download zip
- Adjustable capture schedule via web
- Video caching & expiry policy
- Disk space guard on server
- Multi-Pi support dashboard
- Auth layer if needed
