#!/usr/bin/env bash
set -euo pipefail

BASE="${BASE:-http://127.0.0.1:8010}"

retry() {
  # retry <tries> <sleep_sec> <cmd...>
  local tries="$1"; shift
  local sleep_s="$1"; shift
  local n=1
  until "$@"; do
    if [ "$n" -ge "$tries" ]; then
      return 1
    fi
    sleep "$sleep_s"
    n=$((n+1))
  done
}

curl_ok() {
  # fail fast but quiet
  curl -sS -f "$@"
}

curl_dbg() {
  # show response when failing
  curl -sS -i "$@" || true
}

echo "[1/4] webhook health (best-effort)"
curl_ok "$BASE/api/state" >/dev/null 2>&1 || true

echo "[2/4] perf summary (wait-ready)"
retry 10 0.3 curl_ok "$BASE/perf/summary" >/dev/null

echo "[3/4] create dummy trade OPEN/CLOSE"
TID="T_SMOKE_$(date +%Y%m%d_%H%M%S)"

OPEN_PAYLOAD=$(cat <<JSON
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
)

CLOSE_PAYLOAD=$(cat <<JSON
{
  "type": "CLOSE",
  "trade_id": "$TID",
  "exit": 1.1
}
JSON
)

# OPEN with retries; if still failing, print server response and exit
if ! retry 6 0.4 bash -lc 'curl -sS -f "$0/perf/event" -H "Content-Type: application/json" -d "$1" >/dev/null' "$BASE" "$OPEN_PAYLOAD"; then
  echo "!! OPEN failed; response:"
  curl_dbg "$BASE/perf/event" -H "Content-Type: application/json" -d "$OPEN_PAYLOAD"
  exit 1
fi

# CLOSE with retries; if still failing, print server response and exit
if ! retry 6 0.4 bash -lc 'curl -sS -f "$0/perf/event" -H "Content-Type: application/json" -d "$1" >/dev/null' "$BASE" "$CLOSE_PAYLOAD"; then
  echo "!! CLOSE failed; response:"
  curl_dbg "$BASE/perf/event" -H "Content-Type: application/json" -d "$CLOSE_PAYLOAD"
  exit 1
fi

echo "[4/4] verify trade appears"
curl_ok "$BASE/perf/trades?limit=5&engine=SMOKE" | head -c 200
echo
echo "OK"
