import os, subprocess, shlex, tempfile
from pathlib import Path
from datetime import datetime, timezone
from typing import List
from sqlalchemy import select
from db import async_session, Image, Video

ROOT_DIR = Path(os.getenv("STORAGE_ROOT", "/data/plantcam"))
VIDEOS_DIR = ROOT_DIR / "videos"
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

async def _frames(start: datetime, end: datetime):
    async with async_session() as session:
        rows = await session.execute(
            select(Image.path, Image.taken_at)
            .where(Image.taken_at.between(start, end))
            .order_by(Image.taken_at)
        )
    return [(Path(p), ts) for p, ts in rows.all()]

async def _build_async(start: datetime, end: datetime, fps: int = 24, duration: int | None = None) -> Path:
    start_utc = start.replace(tzinfo=timezone.utc)
    end_utc = end.replace(tzinfo=timezone.utc)
    rows = await _frames(start_utc, end_utc)
    if not rows:
        raise ValueError("No frames in range")

    if duration:
        from datetime import timedelta
        from bisect import bisect_left
        target_frames = fps * duration
        span = (end_utc - start_utc).total_seconds()
        step_sec = span / target_frames
        grid = [start_utc + timedelta(seconds=i*step_sec) for i in range(target_frames)]
        ts_list = [ts for _, ts in rows]
        frames = []
        for t in grid:
            i = bisect_left(ts_list, t)
            if i == len(ts_list):
                i -= 1  # cap to last index
            frames.append(rows[i][0])
    else:
        frames=[p for p,_ in rows]

    name = f"tl_{start.strftime('%Y%m%d%H%M%S')}_{end.strftime('%Y%m%d%H%M%S')}_{fps}.mp4"
    out_path = VIDEOS_DIR / name

    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.writelines([f"file '{p}'\n" for p in frames])
        listfile = f.name

    cmd = shlex.split(
        f"ffmpeg -y -r {fps} -f concat -safe 0 -i {listfile} -c:v libx264 -pix_fmt yuv420p {out_path}"
    )
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    async with async_session() as session:
        session.add(Video(path=str(out_path), params=f"{start}-{end}-{fps}"))
        await session.commit()

    return out_path

def build_timelapse(start, end, fps, duration):
    """Sync wrapper for Celery"""
    import asyncio
    return asyncio.run(_build_async(start, end, fps, duration))
