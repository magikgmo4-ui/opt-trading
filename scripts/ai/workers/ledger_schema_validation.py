import json, sys
from pathlib import Path

health_file = Path("data/runtime_health/healthcheck.jsonl")
latest_file = Path("data/runtime_health/latest.json")
kill_switch_file = Path("data/runtime_health/kill_switch.state")

expected_latest_keys = {"timestamp", "hostname", "run_id", "overall_status", "block_statuses", "checks", "elapsed_seconds"}
expected_block_names = {"MACHINE_IDENTITY", "SYSTEMD_SERVICES", "SYSTEMD_TIMERS", "FORBIDDEN_SERVICES", "VENV", "ENV", "PORTS", "HTTP", "PATHS", "ARTIFACTS", "LOGS", "ORCHESTRATOR"}
expected_check_fields = {"check", "status"}

findings = []

# Validate latest.json
if latest_file.exists():
    latest = json.loads(latest_file.read_text())
    missing = expected_latest_keys - set(latest.keys())
    if missing:
        findings.append(f"latest.json missing keys: {missing}")
    bs = set(latest.get("block_statuses", {}).keys())
    missing_blocks = expected_block_names - bs
    if missing_blocks:
        findings.append(f"latest.json missing block_statuses: {missing_blocks}")
    for check_list in latest.get("checks", {}).values():
        for check in check_list:
            if "status" not in check:
                findings.append(f"check missing 'status' field: {check.get('check', 'unknown')}")
else:
    findings.append("latest.json not found")

# Validate healthcheck.jsonl format
if health_file.exists():
    lines = health_file.read_text().strip().splitlines()
    parse_errors = 0
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            json.loads(line)
        except json.JSONDecodeError:
            parse_errors += 1
    if parse_errors:
        findings.append(f"healthcheck.jsonl: {parse_errors} parse errors")
    if len(lines) < 1:
        findings.append("healthcheck.jsonl is empty")
else:
    findings.append("healthcheck.jsonl not found")

# Validate kill_switch.state format
if kill_switch_file.exists():
    val = kill_switch_file.read_text().strip()
    if val not in ("NORMAL", "BLOCKED", "FULLSTOP"):
        findings.append(f"kill_switch.state unexpected value: {val}")
else:
    findings.append("kill_switch.state not found")

result = {
    "job_id": "ledger-schema-validation",
    "files_checked": ["latest.json", "healthcheck.jsonl", "kill_switch.state"],
    "findings": findings,
    "status": "PASS" if not findings else "WARN",
}
print(json.dumps(result, indent=2))
