import json
from pathlib import Path
from collections import Counter

health_file = Path("data/runtime_health/healthcheck.jsonl")
if not health_file.exists():
    print(json.dumps({"job_id": "ledger-trace-id-audit", "status": "FAIL", "error": "healthcheck.jsonl not found"}, indent=2))
    exit(0)

entries = []
for line in health_file.read_text().strip().splitlines():
    if line.strip():
        entries.append(json.loads(line))

run_ids = [e.get("run_id") for e in entries]
timestamps = [e.get("timestamp") for e in entries]
hostnames = [e.get("hostname") for e in entries]

missing_run_id = sum(1 for r in run_ids if not r)
missing_ts = sum(1 for t in timestamps if not t)
missing_host = sum(1 for h in hostnames if not h)

host_counts = Counter(hostnames)

result = {
    "job_id": "ledger-trace-id-audit",
    "total_entries": len(entries),
    "trace_id_coverage": {
        "with_run_id": len(entries) - missing_run_id,
        "missing_run_id": missing_run_id,
        "unique_run_ids": len(set(run_ids)),
    },
    "timestamp_coverage": {
        "with_timestamp": len(entries) - missing_ts,
        "missing_timestamp": missing_ts,
    },
    "host_coverage": {
        "hosts_found": dict(host_counts.most_common()),
        "missing_hostname": missing_host,
    },
    "findings": [],
    "status": "PASS",
}

if missing_run_id:
    result["findings"].append(f"{missing_run_id} entries missing run_id")
if missing_ts:
    result["findings"].append(f"{missing_ts} entries missing timestamp")
if len(set(run_ids)) < len(entries) * 0.9:
    result["findings"].append("low run_id uniqueness (<90%)")

if result["findings"]:
    result["status"] = "WARN"
print(json.dumps(result, indent=2))
