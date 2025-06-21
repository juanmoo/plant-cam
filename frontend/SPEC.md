# frontend d Web UI

## Purpose
Provide a simple interface to request and download timelapse videos.

## Tech Stack
- Plain HTML/CSS + Vanilla JS (no framework) OR lightweight Svelte.
- Axios/fetch to FastAPI backend.

## Pages
1. **Dashboard (/)**
   - Date/time range pickers.
   - FPS (select: 15, 24, 30).
   - Target video length slider (50 s).
   - **Generate** button.
   - Shows progress bar polling `/api/timelapse/{job}`.
   - Video preview element with download link when ready.

## Components
- `api.js` – wrapper for fetch.
- `timeline.js` – computes duration & displays ETA.
- `index.html` – single-page app.

## Interaction
- `POST /api/timelapse` with JSON.
- Poll every 2 s until video ready.
- Handle errors (e.g., 422 range invalid) with toast overlay.

## Deployment
- Static files served by FastAPI `StaticFiles` from `/frontend/dist`.

## Testing
- Cypress e2e: generate 10 s video over last day.
- Lighthouse performance budget (<100 KB JS).
