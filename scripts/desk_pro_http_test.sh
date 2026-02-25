#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# shellcheck disable=SC1091
source ./scripts/load_env.sh
HOST="${HOST:-$TV_PERF_BASE_URL}"

echo "=== Desk Pro HTTP Test ==="
echo "BASE URL: $HOST"
echo

echo "[1] GET /desk/health"
curl -s "$HOST/desk/health" | (command -v jq >/dev/null && jq || cat)
echo

echo "[2] GET /desk/snapshot"
curl -s "$HOST/desk/snapshot" | (command -v jq >/dev/null && jq || cat)
echo

echo "[3] POST /desk/form (sample)"
curl -s -X POST "$HOST/desk/form" -H 'Content-Type: application/json' -d '{
  "symbol":"BTC",
  "bias":"neutral",
  "vol_regime":"normal",
  "sr":[
    {"tf":"W","kind":"S","level":67900,"label":"W support"},
    {"tf":"D","kind":"R","level":69000,"label":"D resistance"}
  ],
  "etf_flow_bias":"out",
  "onchain_flow_bias":"in",
  "futures_flow_bias":"out",
  "funding_bias":"pos",
  "fear_greed":42,
  "dxy_trend":"up",
  "corr_xau_btc":0.35
}' | (command -v jq >/dev/null && jq || cat)
echo

echo "PASS (if responses returned JSON without error)."
