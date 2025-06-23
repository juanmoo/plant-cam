# frontend – Next.js React UI

## Purpose
Deliver a modern, mobile-friendly, and accessible interface for browsing captures and building timelapse videos.

## Tech Stack
- **Next.js 15** (React, App Router, TypeScript)
- Tailwind CSS for styling
- SWR/fetch helpers for FastAPI calls
- D3.js for histogram/violin plot

## Main Page (/)
- **Capture histogram** – violin-style bars (30-min bins); hover shows bin window, count, thumbnail gif.
- **Latest image** card (auto-refresh every 60 s).
- **Date picker** (react-day-picker) limited to first/last capture dates.
- **Time slider** (24-h range) limited to chosen date.
- **Time-zone selector** (UTC / Local) affecting all displays.
- **Timelapse builder**
  - FPS slider (5-60, default 24)
  - Duration input seconds (default 10)
  - Generate button → calls `/api/timelapse`; shows progress bar, embedded player + download link when ready.

## Components
- `<Histogram />`
- `<LatestImage />`
- `<DateTimeSelector />`
- `<TimeZoneSelect />`
- `<TimelapseForm />`
- `lib/api.ts` – typed fetch helpers (SWR).

## Interaction
- `POST /api/timelapse` JSON `{start,end,fps,duration}`
- Poll `/api/timelapse/{job}` every 2 s.
- Use `/videos/{file}` for playback.
