import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from typing import List
from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy import select
from db import async_session, Image, Base, engine
from config import settings
from fastapi.responses import JSONResponse

app = FastAPI()

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = int(os.getenv("PORT", 8000))
ROOT_DIR = Path(os.getenv("STORAGE_ROOT", "/data/plantcam"))
STORAGE_ROOT = ROOT_DIR / "raw"

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    STORAGE_ROOT.mkdir(parents=True, exist_ok=True)

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
            with open(dest, "wb") as out:
                out.write(await f.read())
            img = Image(device_id=device_id, path=str(dest), taken_at=taken_dt)
            session.add(img)
            stored_paths.append(str(dest))
        await session.commit()
    return JSONResponse({"stored": stored_paths})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=DEFAULT_HOST, port=DEFAULT_PORT, reload=False)
