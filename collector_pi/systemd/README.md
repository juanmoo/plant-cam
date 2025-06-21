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
