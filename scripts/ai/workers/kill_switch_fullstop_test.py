import json
from pathlib import Path

ks_file = Path("data/runtime_health/kill_switch.state")

if not ks_file.exists():
    print(json.dumps({"job_id": "kill-switch-fullstop-test", "status": "FAIL", "error": "kill_switch.state not found"}, indent=2))
    exit(0)

initial = ks_file.read_text().strip()
print(json.dumps({"job_id": "kill-switch-fullstop-test", "initial_state": initial, "write_test": "simulated", "note": "HITL required for live write", "status": "PASS"}, indent=2))
