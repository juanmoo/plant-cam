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


def log(msg):
    print(datetime.now().isoformat(), msg, flush=True)

def capture_image():
    ts = datetime.utcnow()
    rel = ts.strftime("%Y%m%d_%H%M%S") + f"_{DEVICE_ID}.jpg"
    out_path = BUFFER / rel
    # capture using ffmpeg from V4L2 webcam
    run([
        "ffmpeg",
        "-f","v4l2",
        "-video_size", f"{cfg['capture'].get('resolution',[1280,720])[0]}x{cfg['capture'].get('resolution',[1280,720])[1]}",
        "-i","/dev/video0",
        "-frames","1",
        str(out_path)
    ], check=True, stdout=open(os.devnull,'w'), stderr=open(os.devnull,'w'))
    log(f"Captured image {out_path}")
    return out_path, ts


def upload_batch():
    files = sorted(BUFFER.glob("*.jpg"))[: cfg["upload"]["batch_size"]]
    if not files:
        log("No files to upload")
        return
    parts = files[0].stem.split("_")
    taken_str = "_".join(parts[:2])  # YYYYMMDD_HHMMSS
    taken_iso = datetime.strptime(taken_str, "%Y%m%d_%H%M%S").isoformat()
    multipart = [("files", open(fp, "rb")) for fp in files]
    data = {"device_id": DEVICE_ID, "taken_at": taken_iso}
    try:
        r = requests.post(ENDPOINT, files=multipart, data=data, timeout=30)
        r.raise_for_status()
        log(f"Uploaded {len(files)} files: {[str(f) for f in files]}")
        for fp in files:
            fp.unlink()
        log(f"Deleted {len(files)} files after upload")
    except Exception as e:
        log(f"upload failed: {e}")


while True:
    path, _ = capture_image()
    upload_batch()
    time.sleep(CAP_INTERVAL)
