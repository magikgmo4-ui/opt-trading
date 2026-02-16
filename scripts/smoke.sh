#!/usr/bin/env bash
set -euo pipefail

BASE="${BASE:-http://127.0.0.1:8010}"

echo "[1/4] webhook health (best-effort)"
curl -sf "$BASE/api/state" >/dev/null || true

echo "[2/4] perf summary"
curl -sf "$BASE/perf/summary" >/dev/null

echo "[3/4] create dummy trade OPEN/CLOSE"
TID="T_SMOKE_$(date +%Y%m%d_%H%M%S)"

curl -sf "$BASE/perf/event" \
  -H "Content-Type: application/json" \
  -d @- >/dev/null <<JSON
{
  "type": "OPEN",
  "trade_id": "$TID",
  "engine": "SMOKE",
  "symbol": "XAUUSD",
  "side": "LONG",
  "entry": 1.0,
  "stop": 0.9,
  "qty": 1.0,
  "risk_usd": 0.1
}
JSON

curl -sf "$BASE/perf/event" \
  -H "Content-Type: application/json" \
  -d @- >/dev/null <<JSON
{
  "type": "CLOSE",
  "trade_id": "$TID",
  "exit": 1.1
}
JSON

echo "[4/4] verify trade appears"
curl -sf "$BASE/perf/trades?limit=5&engine=SMOKE" | head -c 200
echo
echo "OK"
