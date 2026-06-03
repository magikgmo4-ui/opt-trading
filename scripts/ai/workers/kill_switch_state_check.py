"""Read kill_switch.state and report PASS / WARN — alerts Telegram on WARN."""
import json, pathlib, datetime, sys

STATE_FILE = pathlib.Path("data/runtime_health/kill_switch.state")
REPORT_PATH = pathlib.Path("reports/ai/kill_switch_state_check.json")


def _notify(findings: list, state_value: str | None) -> None:
    try:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
        from modules.env.env import load_env
        load_env()
        from shared.telegram_channels import send_to_channel
        lines = ["🚨 <b>kill-switch-state-check WARN</b>"]
        if state_value:
            lines.append(f"État : <code>{state_value}</code>")
        for f in findings:
            lines.append(f"• {f}")
        send_to_channel("alerts", "\n".join(lines), source="kill_switch_state_check")
    except Exception:
        pass


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
    if status == "WARN":
        _notify(findings, state_value)

if __name__ == "__main__":
    main()
