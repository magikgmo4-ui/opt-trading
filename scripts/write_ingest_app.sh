\
#!/usr/bin/env bash
set -euo pipefail
cat > /opt/trading/ingest/app.py <<'EOF'
from fastapi import FastAPI, Request, Header, HTTPException
from datetime import datetime, timezone
import json, os, socket

APP = FastAPI()
HOST = socket.gethostname()
JSON_PATH = "/opt/trading/journal/events/events.jsonl"
KEY_PATH = "/opt/trading/ingest/INGEST_API_KEY"

def get_key() -> str:
    with open(KEY_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()

def write_event(evt: dict):
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    with open(JSON_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(evt, ensure_ascii=False) + "\n")

@APP.get("/ingest/health")
def health():
    return {"ok": True, "host": HOST}

@APP.post("/ingest")
async def ingest(req: Request, x_api_key: str | None = Header(default=None)):
    if x_api_key is None or x_api_key != get_key():
        raise HTTPException(status_code=401, detail="invalid api key")
    payload = await req.json()
    evt = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "host": HOST,
        "type": "ingest",
        "payload": payload,
    }
    write_event(evt)
    return {"ok": True}
EOF
echo "Wrote /opt/trading/ingest/app.py"
