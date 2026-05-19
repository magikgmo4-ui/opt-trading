#!/usr/bin/env bash
set -euo pipefail

BASE="${1:-http://127.0.0.1:8010}"
VENV_PY="/opt/trading/venv/bin/python"

echo "=== Sanity: Desk Pro UI Toolbox FINAL ==="
echo "Repo: /opt/trading"
echo "Base: $BASE"

"$VENV_PY" - <<'PY'
import importlib, inspect
m = importlib.import_module("modules.desk_pro.api.routes")
print("OK import:", inspect.getsourcefile(m))
PY

"$VENV_PY" - <<PY
import requests, sys
base = "$BASE".rstrip("/")
ui = requests.get(base + "/desk/ui", timeout=5).text
if "/desk/toolbox" not in ui:
    print("FAIL: /desk/ui missing /desk/toolbox")
    for line in ui.splitlines():
        if "Endpoints:" in line:
            print(line.strip())
            break
    sys.exit(2)
print("OK: /desk/ui contains /desk/toolbox")

r = requests.get(base + "/desk/toolbox", timeout=5)
print("OK: /desk/toolbox status", r.status_code)
if r.status_code != 200:
    sys.exit(3)
PY

echo "PASS: Desk Pro UI toolbox sanity OK"
