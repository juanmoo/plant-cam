# collector_pi – Raspberry Pi Image Capture & Upload

## Purpose
Capture plant images on a fixed schedule and upload them to the server within 60 min of capture.

## Hardware
- Raspberry Pi 5 (2 GB+) with CSI/USB camera
- 32 GB micro-SD (OS + local buffer)
- Stable network (Wi-Fi or Ethernet)

## Software Stack
- RPi OS Lite (64-bit)
- Python 3.11
- Required packages: `ffmpeg` via V4L2 (USB) or `picamera2` (CSI), `requests`, `yaml`, `schedule`, `retry`, `watchdog`, `ujson`.

## Directory Layout
```
collector_pi/
 ├─ src/
 │   ├─ capture.py       # takes a single photo
 │   ├─ upload.py        # uploads queued photos
 │   ├─ scheduler.py     # main loop
 │   └─ config.yaml      # runtime settings
 ├─ systemd/plantcam.service  # auto-start unit
 └─ logs/
```

## Configuration (`config.yaml`)
```yaml
capture:
  interval_minutes: 10      # how often to shoot
  resolution: [1920, 1080]
  jpeg_quality: 90
upload:
  method: http              # "http" or "scp"
  http_endpoint: "http://SERVER_IP:8000/api/upload"
  batch_size: 20            # max files per POST
  retry_seconds: 300        # wait before retrying failed batch
storage:
  local_buffer: "/home/pi/plantcam_buffer"
  max_disk_gb: 4            # delete oldest after threshold
id: RPI1234                 # unique device id
```

## Workflow
1. **Scheduler** (`scheduler.py`)
   - Every `interval_minutes`, call `capture.py`.
   - Every 1 min, call `upload.py` if buffer not empty.
2. **capture.py**
   - Acquire image; filename: `{YYYYMMDD_HHMMSS}_{device_id}.jpg`.
   - Save to `local_buffer/YYYY/MM/DD/`.
3. **upload.py**
   - Read up to `batch_size` newest images.
   - HTTP upload: `multipart/form-data` field `files[]` + JSON metadata `{device_id, taken_at}`.
   - On 200 OK, delete local copies; else keep and retry.
4. **Disk Guard**
   - Daily cron deletes oldest files when `max_disk_gb` exceeded.

## REST Upload Contract
- Endpoint: `POST /api/upload`
- Headers: `X-Device-ID`
- Body: multipart with images.
- Response: `200` ⇒ JSON `{stored:["abs/path1",...]}`

## Error Handling
- Network failure ⇒ exponential back-off (max 30 min).
- Corrupt photo ⇒ log and discard.

## Logging
- `logs/capture.log`, `logs/upload.log` (rotated, 5 × 1 MB)

## Deployment
```bash
sudo cp systemd/plantcam.service /etc/systemd/system/
sudo systemctl enable --now plantcam
```

## Testing
- `pytest` unit test stubs in `tests/` (mock camera & server).
- Integration: run `scheduler.py --once` to shoot & upload.
