## Installing PlantCam systemd Service

```bash
# Copy service file
sudo cp plantcam.service /etc/systemd/system/
# Reload systemd
sudo systemctl daemon-reload
# Enable at boot
sudo systemctl enable plantcam
# Start now
sudo systemctl start plantcam
# Check status
sudo systemctl status plantcam
```

## Log Rotation
- Logfile: `/var/log/plantcam.log`
- Provided: `plantcam.logrotate` sample config.
- To enable rotation:
  1. Copy file to `/etc/logrotate.d/plantcam`
  2. It keeps 7 daily compressed logs (`rotate 7`, `compress`), truncates in place (`copytruncate`).
- Test: `sudo logrotate -f /etc/logrotate.d/plantcam`

