import os, subprocess, shlex, tempfile
from pathlib import Path
from datetime import datetime
from typing import List
from sqlalchemy import select
from db import async_session, Image, Video

ROOT_DIR = Path(os.getenv("STORAGE_ROOT", "/data/plantcam"))
VIDEOS_DIR = ROOT_DIR / "videos"
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

async def _frame_paths(start: datetime, end: datetime) -> List[Path]:
    async with async_session() as session:
        rows = (
            await session.execute(
                select(Image.path).where(Image.taken_at.between(start, end)).order_by(Image.taken_at)
            )
        ).scalars().all()
    return [Path(p) for p in rows]

async def build_timelapse(start: datetime, end: datetime, fps: int = 24, duration: int | None = None) -> Path:
    frames = await _frame_paths(start, end)
    if not frames:
        raise ValueError("No frames in range")

    if duration:
        needed = fps * duration
        step = max(1, len(frames) // needed)
        frames = frames[::step][:needed]

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
