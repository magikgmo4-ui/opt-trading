import json, time
from pathlib import Path
from collections import Counter

health_file = Path("data/runtime_health/healthcheck.jsonl")
if not health_file.exists():
    print(json.dumps({"job_id": "stuck-job-detector", "status": "FAIL", "error": "healthcheck.jsonl not found"}, indent=2))
    exit(0)

entries = []
for line in health_file.read_text().strip().splitlines():
    if line.strip():
        entries.append(json.loads(line))

now = time.time()
stuck = []
status_breakdown = Counter()

# Only report as stuck if status is non-PASS AND new entries since have been PASS (i.e., it recovered but wasn't cleared)
# OR if the LATEST entry is non-PASS and old
latest_status = entries[-1].get("overall_status", "UNKNOWN") if entries else "UNKNOWN"

for e in entries:
    ts = e.get("timestamp", "")
    status = e.get("overall_status", "UNKNOWN")
    status_breakdown[status] += 1
    if ts:
        try:
            from datetime import datetime
            t = datetime.fromisoformat(ts).timestamp()
            age_mins = (now - t) / 60
            # Only flag if the LATEST entry is still non-PASS and old, or if entry is old and never recovered
            if age_mins > 60 and status != "PASS":
                stuck.append({"timestamp": ts, "run_id": e.get("run_id"), "status": status, "age_minutes": round(age_mins, 1)})
        except:
            pass

latest_entry = entries[-1] if entries else {}
latest_age = "unknown"
if latest_entry.get("timestamp"):
    try:
        from datetime import datetime
        t = datetime.fromisoformat(latest_entry["timestamp"]).timestamp()
        latest_age = f"{round((now - t) / 60, 1)} min ago"
    except:
        pass

result = {
    "job_id": "stuck-job-detector",
    "total_entries": len(entries),
    "status_breakdown": dict(status_breakdown),
    "stuck_jobs_found": len(stuck),
    "stuck_details": stuck[:10] if stuck else [],
    "latest_entry_age": latest_age,
    "latest_status": latest_status,
    "findings": [],
    "status": "PASS",
}
# Only WARN if the LATEST entry is non-PASS (stuck RIGHT NOW)
if latest_status != "PASS":
    result["findings"].append(f"latest entry is {latest_status}, age: {latest_age}")
if not entries:
    result["findings"].append("no entries found")

if result["findings"]:
    result["status"] = "WARN"
print(json.dumps(result, indent=2))
