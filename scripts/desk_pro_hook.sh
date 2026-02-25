#!/usr/bin/env bash
set -euo pipefail

ROOT="$(./scripts/desk_pro_find_root.sh)"
if [[ "$ROOT" == "FAIL" ]]; then
  echo "FAIL: cannot locate repo root. Set REPO_ROOT=/path/to/repo and rerun."
  exit 2
fi
cd "$ROOT"

echo "=== Desk Pro Hook (auto-mount) ==="
echo "Repo root: $ROOT"

# If user provides APP_FILE, use it.
if [[ -n "${APP_FILE:-}" ]]; then
  pick="$APP_FILE"
  [[ -f "$pick" ]] || { echo "FAIL: APP_FILE not found: $pick"; exit 2; }
else
  # Candidate entrypoints (priority order)
  candidates=(main.py app.py src/main.py src/app.py webhook_server.py server.py)

  pick=""
  for f in "${candidates[@]}"; do
    [[ -f "$f" ]] || continue
    if grep -qE 'app\s*=\s*FastAPI\(' "$f"; then
      pick="$f"
      break
    fi
  done

  # Fallback: search in repo (exclude hidden/venv/.git)
  if [[ -z "$pick" ]]; then
    pick="$(grep -RIl --exclude-dir=venv --exclude-dir=.git --exclude-dir=.mozilla --exclude-dir=.cache --exclude='*test*' -E 'app\s*=\s*FastAPI\(' . | head -n 1 || true)"
  fi
fi

if [[ -z "${pick:-}" ]]; then
  echo "FAIL: could not find FastAPI entrypoint (app = FastAPI(...))."
  echo "Tip: export APP_FILE=path/to/entrypoint.py"
  exit 2
fi

echo "Target file: $pick"

# Idempotent check
if grep -q 'modules\.desk_pro\.mount' "$pick" && grep -q 'mount_desk_pro\(app\)' "$pick"; then
  echo "Already mounted."
  exit 0
fi

ts="$(date +%Y%m%d_%H%M%S)"
cp -a "$pick" "$pick.bak.$ts"
echo "Backup: $pick.bak.$ts"

PICK_FILE="$pick" python - <<'PY'
import os, re
from pathlib import Path

pick = os.environ["PICK_FILE"]
p = Path(pick)
s = p.read_text(encoding="utf-8", errors="replace")

mount_import = "from modules.desk_pro.mount import mount as mount_desk_pro"
mount_call = "mount_desk_pro(app)"

if mount_import not in s:
    lines = s.splitlines()
    inserted = False
    for i, line in enumerate(lines[:120]):
        if re.match(r"^from\s+fastapi\s+import\s+FastAPI\b", line) or re.match(r"^import\s+fastapi\b", line):
            j = i + 1
            while j < len(lines) and (lines[j].startswith("from fastapi") or lines[j].startswith("import fastapi")):
                j += 1
            lines.insert(j, mount_import)
            inserted = True
            break
    if not inserted:
        lines.insert(0, mount_import)
    s = "\n".join(lines) + ("\n" if not s.endswith("\n") else "")

if mount_call not in s:
    m = re.search(r"^(\s*app\s*=\s*FastAPI\([^\n]*\)\s*)$", s, flags=re.M)
    if not m:
        raise SystemExit("Could not locate 'app = FastAPI(...)' line.")
    insert_pos = m.end()
    s = s[:insert_pos] + "\n" + mount_call + "\n" + s[insert_pos:]

p.write_text(s, encoding="utf-8")
print("Patched", pick)
PY

echo "OK: mounted Desk Pro into $pick"
echo "Next: restart your service / uvicorn."
