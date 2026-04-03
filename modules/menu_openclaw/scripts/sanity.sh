#!/usr/bin/env bash
set -euo pipefail

MODULES_ROOT="${OPENCLAW_MODULE_TARGET_ROOT:-/opt/trading}/modules"
REGISTRY="$MODULES_ROOT/install_module_openclaw/app/modules_registry.json"

command -v openclaw >/dev/null 2>&1 || { echo "FAIL: openclaw non trouvé" >&2; exit 1; }
[ -d "$MODULES_ROOT" ] || { echo "FAIL: modules root introuvable: $MODULES_ROOT" >&2; exit 1; }
[ -f "$REGISTRY" ] || { echo "FAIL: registry OpenClaw introuvable: $REGISTRY" >&2; exit 1; }

python3 - <<PY
import json, pathlib, sys
reg = pathlib.Path(r"$REGISTRY")
data = json.loads(reg.read_text())
mods = data.get("modules") or []
if not mods:
    print("FAIL: registry vide")
    sys.exit(1)
print(f"PASS: registry OpenClaw OK ({len(mods)} modules)")
PY

echo "PASS: menu_openclaw sanity OK"
