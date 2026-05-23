import json, os, stat
from pathlib import Path
from collections import defaultdict

critical_paths = [
    Path("data/runtime_health"),
    Path("data/runtime_health/kill_switch.state"),
    Path("config/machine_runtime_map.yml"),
    Path(".gitignore"),
]

permissions = defaultdict(list)
findings = []

for p in critical_paths:
    if not p.exists():
        findings.append(f"MISSING: {p}")
        continue
    s = p.stat()
    mode = s.st_mode
    perm_oct = oct(stat.S_IMODE(mode))
    is_world_writable = bool(mode & stat.S_IWOTH)
    owner = s.st_uid
    group = s.st_gid

    info = {
        "path": str(p),
        "permissions": perm_oct,
        "is_world_writable": is_world_writable,
        "uid": owner,
        "gid": group,
        "is_dir": p.is_dir(),
    }
    permissions[str(p)] = info

    if is_world_writable:
        findings.append(f"world-writable: {p} ({perm_oct})")

# Check if any .env files have open permissions
for env_file in Path(".").glob(".env*"):
    if env_file.is_file():
        s = env_file.stat()
        if bool(s.st_mode & stat.S_IWOTH) or bool(s.st_mode & stat.S_IROTH):
            findings.append(f"exposed permissions on {env_file}: {oct(stat.S_IMODE(s.st_mode))}")

result = {
    "job_id": "permission-drift-check",
    "paths_checked": [str(p) for p in critical_paths],
    "permissions": dict(permissions),
    "findings": findings,
    "status": "PASS" if not findings else "WARN",
}
print(json.dumps(result, indent=2))
