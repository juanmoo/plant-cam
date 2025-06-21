#!/usr/bin/env python3
import asyncio, argparse, os
from datetime import datetime
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "server_backend" / "src"))
from video import build_timelapse

parser = argparse.ArgumentParser(description="Generate timelapse video")
parser.add_argument("start", help="ISO start time e.g. 2025-06-21T00:00:00")
parser.add_argument("end", help="ISO end time")
parser.add_argument("--fps", type=int, default=24)
parser.add_argument("--duration", type=int, help="target seconds")
args = parser.parse_args()

start_dt = datetime.fromisoformat(args.start)
end_dt = datetime.fromisoformat(args.end)

path = asyncio.run(build_timelapse(start_dt, end_dt, args.fps, args.duration))
print("Video saved to", path)
