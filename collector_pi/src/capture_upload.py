import time, os, requests, yaml
from datetime import datetime
from pathlib import Path
from subprocess import run

CONFIG_PATH = Path(__file__).parent / "../config.yaml"
with open(CONFIG_PATH) as f:
    cfg = yaml.safe_load(f)

BUFFER = Path(cfg["storage"]["local_buffer"])
BUFFER.mkdir(parents=True, exist_ok=True)

CAP_INTERVAL = cfg["capture"]["interval_minutes"] * 60
DEVICE_ID = cfg["id"]
ENDPOINT = cfg["upload"]["http_endpoint"]


def capture_image():
    ts = datetime.utcnow()
    rel = ts.strftime("%Y%m%d_%H%M%S") + f"_{DEVICE_ID}.jpg"
    out_path = BUFFER / rel
    # simple capture using libcamera-still
    run([
        "libcamera-still",
        "-o",
        str(out_path),
        "-q",
        str(cfg["capture"]["jpeg_quality"]),
    ], check=True)
    return out_path, ts


def upload_batch():
    files = sorted(BUFFER.glob("*.jpg"))[: cfg["upload"]["batch_size"]]
    if not files:
        return
    taken_time = files[0].stem.split("_")[0]
    taken_iso = datetime.strptime(taken_time, "%Y%m%d_%H%M%S").isoformat()
    multipart = [("files", open(fp, "rb")) for fp in files]
    data = {"device_id": DEVICE_ID, "taken_at": taken_iso}
    try:
        r = requests.post(ENDPOINT, files=multipart, data=data, timeout=30)
        r.raise_for_status()
        for fp in files:
            fp.unlink()
    except Exception as e:
        print("upload failed", e)


while True:
    path, _ = capture_image()
    upload_batch()
    time.sleep(CAP_INTERVAL)
