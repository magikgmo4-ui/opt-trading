import json, sys
from pathlib import Path
from collections import Counter

health_file = Path("data/runtime_health/healthcheck.jsonl")
if not health_file.exists():
    print(json.dumps({"job_id": "ledger-blocked-events-digest", "status": "FAIL", "error": "healthcheck.jsonl not found"}))
    sys.exit(0)

entries = []
for line in health_file.read_text().strip().splitlines():
    if line.strip():
        entries.append(json.loads(line))

statuses = Counter(e.get("overall_status", "UNKNOWN") for e in entries)
block_fails = Counter()
for e in entries:
    bs = e.get("block_statuses", {})
    for block, status in bs.items():
        if status != "PASS":
            block_fails[block] += 1

blocked = [e for e in entries if e.get("overall_status") != "PASS"]
latest = entries[-1] if entries else {}

result = {
    "job_id": "ledger-blocked-events-digest",
    "total_entries": len(entries),
    "status_summary": dict(statuses),
    "block_failures": dict(block_fails.most_common()),
    "blocked_events": len(blocked),
    "latest_entry": {
        "timestamp": latest.get("timestamp"),
        "overall_status": latest.get("overall_status"),
        "run_id": latest.get("run_id"),
    },
    "current_status": latest.get("overall_status"),
    "current_block_statuses": latest.get("block_statuses"),
    "status": "PASS" if latest.get("overall_status") == "PASS" else "WARN",
}
print(json.dumps(result, indent=2))
