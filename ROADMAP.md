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
- [ ] Systemd service + log rotation on Pi
- [ ] Dockerize backend (API + Celery)

## Phase 4 – Nice-to-Have Enhancements
- [ ] Bulk image download zip
- [ ] Adjustable capture schedule via web
- [ ] Video caching & expiry policy
- [ ] Disk space guard on server
- [ ] Multi-Pi support dashboard
- [ ] Auth layer if needed
