import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from typing import List
from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy import select
from db import async_session, Image, Base, engine
from config import settings
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR.parent / "static"
from routers_timelapse import router as tl_router

app = FastAPI()
app.include_router(tl_router)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = int(os.getenv("PORT", 8000))
ROOT_DIR = Path(os.getenv("STORAGE_ROOT", "/data/plantcam"))
STORAGE_ROOT = ROOT_DIR / "raw"
VIDEOS_DIR = ROOT_DIR / "videos"

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    STORAGE_ROOT.mkdir(parents=True, exist_ok=True)
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    app.mount("/videos", StaticFiles(directory=str(VIDEOS_DIR)), name="videos")

@app.get("/videos")
async def list_videos(limit: int = 10):
    """Return newest videos, pass ?limit=N to adjust."""
    vids = sorted(VIDEOS_DIR.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)[:limit]
    return [{"name": p.name, "created": datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat()} for p in vids]

@app.post("/api/upload")
async def upload(
    device_id: str = Form(...),
    taken_at: str = Form(...),
    files: List[UploadFile] = File(...),
):
    try:
        taken_dt = datetime.fromisoformat(taken_at).replace(tzinfo=timezone.utc)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid taken_at format")

    stored_paths = []
    async with async_session() as session:
        for f in files:
            subdir = STORAGE_ROOT / taken_dt.strftime("%Y/%m/%d")
            subdir.mkdir(parents=True, exist_ok=True)
            dest = subdir / f.filename
            rel_path = dest.relative_to(STORAGE_ROOT)
            with open(dest, "wb") as out:
                out.write(await f.read())
            img = Image(device_id=device_id, path=str(rel_path), taken_at=taken_dt)
            session.add(img)
            stored_paths.append(str(dest))
        await session.commit()
    return JSONResponse({"stored": stored_paths})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=DEFAULT_HOST, port=DEFAULT_PORT, reload=False)
