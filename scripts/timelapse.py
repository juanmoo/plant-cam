#!/usr/bin/env python3
import asyncio, argparse, os
from datetime import datetime
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "server_backend" / "src"))
from video import build_timelapse

parser = argparse.ArgumentParser(description="Generate timelapse video")
parser.add_argument("--start", help="ISO start time; default now-1h")
parser.add_argument("--end", help="ISO end time; default now")
parser.add_argument("--fps", type=int, default=24)
parser.add_argument("--duration", type=int, default=5, help="target seconds (default 5)")
args = parser.parse_args()

from datetime import timedelta, timezone
now = datetime.now(timezone.utc)
end_dt = datetime.fromisoformat(args.end) if args.end else now
start_dt = datetime.fromisoformat(args.start) if args.start else end_dt - timedelta(hours=1)

path = asyncio.run(build_timelapse(start_dt, end_dt, args.fps, args.duration))
print("Video saved to", path)
