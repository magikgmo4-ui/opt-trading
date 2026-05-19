#!/usr/bin/env bash
set -euo pipefail
echo "=== desk_capture_inputs sanity ==="
date -Iseconds

VENV="/opt/trading/.venvs/desk_capture_inputs"

if [[ ! -x "$VENV/bin/python" ]]; then
  echo "ERROR: missing venv $VENV. Run INSTALL.sh first." >&2
  exit 2
fi

if [[ ! -f /opt/trading/desk/snapshots/latest.json ]]; then
  echo "ERROR: missing /opt/trading/desk/snapshots/latest.json (run ingest/bridge first)" >&2
  exit 3
fi

"$VENV/bin/python" - <<'PY'
import json
from pathlib import Path
p = Path("/opt/trading/desk/snapshots/latest.json")
j = json.loads(p.read_text(encoding="utf-8"))
assert isinstance(j, dict) and len(j) > 0, "latest.json empty"
missing = []
for sym, rec in j.items():
    path = Path(rec.get("path",""))
    if not path.exists():
        missing.append((sym, str(path)))
if missing:
    raise SystemExit("Missing images: " + ", ".join([f"{s}:{p}" for s,p in missing]))
print("PASS: latest.json + image paths OK (", len(j), "symbols )")
PY
