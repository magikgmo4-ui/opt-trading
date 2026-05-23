import json, time
from pathlib import Path

health_file = Path("data/runtime_health/healthcheck.jsonl")
latest_file = Path("data/runtime_health/latest.json")
kill_switch_file = Path("data/runtime_health/kill_switch.state")
archive_dir = Path("data/runtime_health/job_logs/archive")

paths_map = {
    "healthcheck.jsonl": health_file,
    "latest.json": latest_file,
    "kill_switch.state": kill_switch_file,
}

files = {}
for name, p in paths_map.items():
    info = {"path": str(p)}
    if p.exists():
        s = p.stat()
        info["exists"] = True
        info["size_bytes"] = s.st_size
        info["mtime"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(s.st_mtime))
        info["age_hours"] = round((time.time() - s.st_mtime) / 3600, 1)
    else:
        info["exists"] = False
    files[name] = info

archive_files = list(archive_dir.rglob("*")) if archive_dir.exists() else []
rotation_result = {
    "job_id": "ledger-rotation-check",
    "files": files,
    "archive": {
        "exists": archive_dir.exists(),
        "file_count": len(archive_files),
        "archive_path": str(archive_dir) if archive_dir.exists() else None,
    },
    "findings": [],
}
if health_file.exists() and files["healthcheck.jsonl"].get("size_bytes", 0) > 5 * 1024 * 1024:
    rotation_result["findings"].append("healthcheck.jsonl >5MB, rotation recommended")
if not archive_dir.exists():
    rotation_result["findings"].append("archive directory missing")

rotation_result["status"] = "PASS" if not rotation_result["findings"] else "WARN"
print(json.dumps(rotation_result, indent=2))
