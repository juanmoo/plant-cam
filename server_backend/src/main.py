import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from datetime import datetime
from pathlib import Path
from sqlalchemy import select
from db import async_session, Image, Base, engine
from config import settings
from fastapi.responses import JSONResponse

app = FastAPI()
STORAGE_ROOT = Path("/data/plantcam/raw")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    STORAGE_ROOT.mkdir(parents=True, exist_ok=True)

@app.post("/api/upload")
async def upload(device_id: str, taken_at: str, files: List[UploadFile] = File(...)):
    try:
        taken_dt = datetime.fromisoformat(taken_at)
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
