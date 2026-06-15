#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE="$BASE/state_cache.json"
SCHEMA="$BASE/state_schema.json"
PROJECT_ROOT="$(cd "$BASE/../../.." && pwd)"
mkdir -p "$BASE"

if [ ! -f "$SCHEMA" ]; then
  echo '{"error":"state_schema.json not found","updated_at":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"}' > "$CACHE"
  exit 1
fi

aggregate_state() {
  python3 - "$SCHEMA" "$CACHE" <<'PY'
import json
import shlex
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

schema = json.loads(Path(sys.argv[1]).read_text())
cache_path = Path(sys.argv[2])

local_names = {socket.gethostname(), socket.getfqdn(), "localhost", "127.0.0.1"}
try:
    r = subprocess.run(["hostname"], capture_output=True, text=True, timeout=2)
    if r.returncode == 0 and r.stdout.strip():
        local_names.add(r.stdout.strip())
except Exception:
    pass


def is_local(machine: str) -> bool:
    return not machine or machine in local_names


def run_remote(machine: str, remote_cmd: str, timeout: int = 8) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=4", machine, remote_cmd],
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def check_http(machine: str, endpoint: str) -> tuple[str, str]:
    probe = (
        "import sys, urllib.request\n"
        "url = sys.argv[1]\n"
        "try:\n"
        "    with urllib.request.urlopen(url, timeout=5) as r:\n"
        "        print(r.status)\n"
        "except Exception as e:\n"
        "    print(f'ERROR::{e}')\n"
        "    raise SystemExit(2)\n"
    )
    try:
        if is_local(machine):
            r = subprocess.run([sys.executable, "-c", probe, endpoint], capture_output=True, text=True, timeout=8)
        else:
            remote_cmd = shlex.join(["python3", "-c", probe, endpoint])
            r = run_remote(machine, remote_cmd)
    except Exception as e:
        return "down", str(e)

    output = (r.stdout or r.stderr).strip()
    if r.returncode == 0:
        code = output.splitlines()[-1] if output else "200"
        return ("up" if code == "200" else "degraded"), f"HTTP {code}"
    if output.startswith("ERROR::"):
        output = output.split("ERROR::", 1)[1]
    return "down", output or f"exit={r.returncode}"


def check_process(machine: str, check_cmd: str) -> tuple[str, str]:
    try:
        if is_local(machine):
            r = subprocess.run(check_cmd, shell=True, capture_output=True, text=True, timeout=6)
        else:
            remote_cmd = shlex.join(["bash", "-lc", check_cmd])
            r = run_remote(machine, remote_cmd)
    except Exception as e:
        return "down", str(e)

    detail = (r.stdout or r.stderr).strip()
    return ("up" if r.returncode == 0 else "down"), detail or "process check"


results = []
checked_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
for mod in schema.get("modules", []):
    mtype = mod.get("type", "")
    machine = mod.get("machine", "")
    status = "unknown"
    detail = ""
    if mtype == "http":
        status, detail = check_http(machine, mod["endpoint"])
    elif mtype == "ws":
        status = "unknown"
        detail = "ws check not implemented"
    elif mtype == "process":
        status, detail = check_process(machine, mod["check"])

    results.append({
        "id": mod["id"],
        "status": status,
        "detail": detail,
        "machine": machine,
        "critical": mod.get("critical", False),
        "last_check": checked_at,
    })

cache_path.write_text(json.dumps({
    "version": "1.0",
    "updated_at": checked_at,
    "modules": results,
}, indent=2))
print("OK")
PY
}

aggregate_state
