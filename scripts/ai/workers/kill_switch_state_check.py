"""Read kill_switch.state and report PASS / WARN."""
import json, pathlib, datetime

STATE_FILE = pathlib.Path("data/runtime_health/kill_switch.state")
REPORT_PATH = pathlib.Path("reports/ai/kill_switch_state_check.json")

def main():
    findings = []
    state_value = None

    if not STATE_FILE.exists():
        findings.append(f"kill_switch.state not found at {STATE_FILE}")
        status = "WARN"
    else:
        raw = STATE_FILE.read_text().strip()
        state_value = raw
        if raw == "STOP":
            findings.append("kill switch is STOP — system halted")
            status = "WARN"
        elif raw in ("OK", "RUN", ""):
            status = "PASS"
        else:
            findings.append(f"unknown kill_switch value: {raw!r}")
            status = "WARN"

    report = {
        "job_id": "kill-switch-state-check",
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "state_file": str(STATE_FILE),
        "state_value": state_value,
        "findings": findings,
        "status": status,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
