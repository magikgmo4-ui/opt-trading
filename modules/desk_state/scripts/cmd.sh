#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
BASE="$(cd "$SCRIPT_DIR/.." && pwd)"
CFG="$BASE/config/desk_state.env"

load_cfg() { if [ -f "$CFG" ]; then source "$CFG"; fi; }

usage() {
  cat <<'EOF'
Usage: cmd.sh <command>

Commands:
  build_once     Build state latest.json (append history)
  print_latest   Print latest.json (head)
  print_schema   Quick summary
  print_config   Show config
EOF
}

CMD="${1:-}"
[ -z "$CMD" ] && { usage; exit 1; }

load_cfg

case "$CMD" in
  build_once)
    python3 "$BASE/desk_state.py"
    ;;
  print_latest)
    STATE_LATEST="${STATE_LATEST:-/opt/trading/desk/state/latest.json}"
    test -f "$STATE_LATEST" || { echo "No state: $STATE_LATEST"; exit 2; }
    sed -n '1,220p' "$STATE_LATEST"
    ;;
  print_schema)
    STATE_LATEST="${STATE_LATEST:-/opt/trading/desk/state/latest.json}"
    test -f "$STATE_LATEST" || { echo "No state: $STATE_LATEST"; exit 2; }
    python3 - "$STATE_LATEST" <<'PY'
import json,sys
p=sys.argv[1]
d=json.load(open(p,'r',encoding='utf-8'))
print("ts:", d.get("ts"))
print("host:", d.get("host"))
print("timeframe:", d.get("timeframe"))
syms=d.get("symbols") or []
print("symbols:", syms)
sn=d.get("snapshots") or {}
for s in syms:
    x=sn.get(s) or {}
    print(f"- {s}: age_min={x.get('age_min')} stale={x.get('stale')}")
PY
    ;;
  print_config)
    if [ -f "$CFG" ]; then sed -n '1,240p' "$CFG"; else echo "No config at $CFG"; exit 2; fi
    ;;
  *)
    echo "Unknown command: $CMD"
    usage
    exit 1
    ;;
esac
