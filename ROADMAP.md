# PlantCam Roadmap

> Mark tasks with `[x]` when completed.

## Phase 1 – MVP
- [ ] Pi capture every 10 min and HTTP upload
- [ ] Backend endpoint `/api/upload` storing images
- [ ] Basic DB schema & filesystem layout
- [ ] Manual script to generate timelapse (CLI)
- [ ] Serve static index.html allowing manual download

## Phase 2 – Timelapse API & Simple UI
- [ ] `/api/timelapse` async video job
- [ ] Redis/Celery worker
- [ ] Uniform frame sampling algorithm
- [ ] Minimal web UI with range pickers & progress

## Phase 3 – Production Hardening
- [ ] Systemd service + log rotation on Pi
- [ ] Video caching & expiry policy
- [ ] Disk space guard on server
- [ ] Unit + integration tests CI

## Phase 4 – Nice-to-Have Enhancements
- [ ] Bulk image download zip
- [ ] Adjustable capture schedule via web
- [ ] Multi-Pi support dashboard
- [ ] Auth layer if needed
