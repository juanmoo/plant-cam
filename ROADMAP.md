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
### Milestone 1 – Scaffold
- [ ] Initialise Next.js 15 + TypeScript + Tailwind project
- [ ] Configure ESLint / Prettier & absolute imports

### Milestone 2 – Core Layout
- [ ] App shell with header & dark-mode toggle
- [ ] Fetch capture min/max dates on load

### Milestone 3 – Components
- [ ] Graphical capture histogram (30-min bins, hover shows count/thumbnail)
- [ ] Latest image preview (auto-refresh)
- [ ] Date picker + time slider limited to data range
- [ ] Time-zone selector (UTC / Local) stored in localStorage
- [ ] Timelapse builder form: FPS slider (5-60, default 24) & duration seconds (default 10)

### Milestone 4 – Timelapse Workflow
- [ ] Call `/api/timelapse` and poll status
- [ ] Progress bar then embedded player & download link

### Milestone 5 – Polish & Deploy
- [ ] Responsive/mobile layout & a11y
- [ ] Error toasts
- [ ] Lighthouse/perf budget <150 KB JS
- [ ] `next export` assets copied to `server_backend/static`

## Backlog
- Bulk image download zip
- Adjustable capture schedule via web
- Video caching & expiry policy
- Disk space guard on server
- Multi-Pi support dashboard
- Auth layer if needed
