\
#!/usr/bin/env bash
set -euo pipefail
KEY_PATH="/opt/trading/ingest/INGEST_API_KEY"
sudo mkdir -p /opt/trading/ingest
openssl rand -hex 24 | sudo tee "$KEY_PATH" >/dev/null
sudo chown student:student "$KEY_PATH" 2>/dev/null || true
sudo chmod 600 "$KEY_PATH"
sudo systemctl restart student-ingest 2>/dev/null || true
echo "New key:"
cat "$KEY_PATH"
