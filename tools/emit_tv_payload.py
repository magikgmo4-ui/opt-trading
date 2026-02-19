import json
import os
import urllib.request
from datetime import datetime, timezone

# Default to the actual FastAPI route we discovered in webhook_server.py
WEBHOOK_URL = os.environ.get("TV_WEBHOOK_URL", "http://127.0.0.1:8000/tv")
TV_WEBHOOK_KEY = os.environ.get("TV_WEBHOOK_KEY", "")

def post(payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        WEBHOOK_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))

def main():
    if not TV_WEBHOOK_KEY:
        raise SystemExit("Missing TV_WEBHOOK_KEY in environment (.env / systemd).")

    # /tv expects:
    # - key (valid)
    # - engine (non-empty)
    # - signal in {"BUY","SELL"}
    # - price and sl non-zero (risk sizing)
    # Optional: tp, tf, reason, symbol
    payload = {
        "key": TV_WEBHOOK_KEY,
        "engine": os.environ.get("TV_ENGINE", "TV_TEST"),
        "signal": os.environ.get("TV_SIGNAL", "BUY").strip().upper(),  # BUY or SELL
        "symbol": os.environ.get("TV_SYMBOL", "XAUUSD"),
        "tf": os.environ.get("TV_TF", "5"),
        "price": float(os.environ.get("TV_PRICE", "100.0")),
        "tp": float(os.environ.get("TV_TP", "0.0")),   # can be 0
        "sl": float(os.environ.get("TV_SL", "90.0")),   # must be non-zero for risk sizing
        "reason": os.environ.get("TV_REASON", "probe-tv"),
        "ts": datetime.now(timezone.utc).isoformat(),
    }

    resp = post(payload)
    print("resp:", resp)

if __name__ == "__main__":
    main()
