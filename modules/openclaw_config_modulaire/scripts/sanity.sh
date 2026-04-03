#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP="$BASE/app"
CFG="$HOME/.openclaw/openclaw.json"

fail() { echo "FAIL: $*" >&2; exit 1; }

command -v openclaw >/dev/null 2>&1 || fail "openclaw non trouvé dans PATH"
[ -f "$CFG" ] || fail "config manquante: $CFG"
[ -f "$APP/openclaw_root_template.json5" ] || fail "template racine manquant"
[ -f "$APP/agents.json5" ] || fail "agents.json5 manquant"
[ -f "$APP/tools.json5" ] || fail "tools.json5 manquant"

python3 - <<'PY' || exit 1
import json, pathlib, sys
cfg = pathlib.Path.home()/'.openclaw'/'openclaw.json'
try:
    data = json.loads(cfg.read_text())
except Exception as e:
    print(f"FAIL: config live non lisible: {e}")
    sys.exit(1)
tok = (((data.get('gateway') or {}).get('auth') or {}).get('token'))
if not tok:
    print("FAIL: gateway.auth.token manquant dans la config live")
    sys.exit(1)
print("PASS: token gateway détecté")
PY

echo "PASS: openclaw_config_modulaire sanity OK"
