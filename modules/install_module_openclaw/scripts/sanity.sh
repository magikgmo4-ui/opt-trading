#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REG="$BASE/app/modules_registry.json"
[ -f "$REG" ] || { echo "FAIL: registry manquante: $REG" >&2; exit 1; }
python3 - <<PY
import json, pathlib, sys
reg = pathlib.Path(r"$REG")
data = json.loads(reg.read_text())
mods = data.get("modules") or []
if not mods:
    print("FAIL: aucun module dans la registry")
    sys.exit(1)
print(f"PASS: registry OK ({len(mods)} modules)")
PY
echo "PASS: install_module_openclaw sanity OK"
