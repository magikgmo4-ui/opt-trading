#!/usr/bin/env bash
set -euo pipefail

echo "=== Desk Pro Vision Sanity Check ==="
date -Is

PY="${PYTHON:-python3}"
ROOT="${VISION_ROOT:-/opt/trading/data/desk_pro/vision}"

echo "[python]"
$PY -V

echo "[deps]"
$PY - <<'PY'
import sys
import importlib
mods = ["matplotlib","numpy","PIL"]
for m in mods:
    importlib.import_module(m)
print("OK deps:", ", ".join(mods))
PY

echo "[run placeholder]"
$PY -m desk_pro_vision.vision.vision_generate --root "$ROOT" --mode placeholder

echo "[check outputs]"
ls -lah "$ROOT/latest" || true
test -f "$ROOT/latest/summary.json"
test -f "$ROOT/latest/vision.log.jsonl"
test -f "$ROOT/latest/charts/mosaic_2x2.png"

echo "OK: sanity passed"
