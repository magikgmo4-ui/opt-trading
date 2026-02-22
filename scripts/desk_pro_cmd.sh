#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# shellcheck disable=SC1091
source ./scripts/load_env.sh
HOST="${HOST:-$TV_PERF_BASE_URL}"

cmd="${1:-help}"

case "$cmd" in
  help|-h|--help|"")
    echo "Usage: $0 <cmd>"
    echo "  sanity            Run sanity check"
    echo "  health            GET /desk/health"
    echo "  snapshot          GET /desk/snapshot"
    echo "  form-sample       POST /desk/form (sample SR W/D)"
    echo "  tree              Show module files"
    echo
    echo "Base URL: $TV_PERF_BASE_URL"
    ;;
  sanity) exec ./scripts/desk_pro_sanity.sh ;;
  health) curl -s "$HOST/desk/health" | (command -v jq >/dev/null && jq || cat) ;;
  snapshot) curl -s "$HOST/desk/snapshot" | (command -v jq >/dev/null && jq || cat) ;;
  form-sample)
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
    ;;
  tree) find modules/desk_pro -maxdepth 3 -type f -print | sort ;;
  *) echo "Unknown cmd: $cmd"; exit 1 ;;
esac
