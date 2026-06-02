"""Digest of FAIL/BLOCKED/RUNNER_ERROR runner reports — alerts Telegram on failures."""
import json, pathlib, datetime, sys

REPORTS_DIR = pathlib.Path("reports/ai/workers")
REPORT_PATH = pathlib.Path("reports/ai/strict_worker_failure_report.json")

FAILURE_STATUSES = {"FAIL", "BLOCKED", "RUNNER_ERROR", "REFUSED", "INVALID_INPUT"}


def _notify(failures: list) -> None:
    try:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
        from modules.env.env import load_env
        load_env()
        from shared.telegram_channels import send_to_channel
        lines = [f"🔴 <b>strict-worker-failure-report WARN</b>"]
        lines.append(f"{len(failures)} worker(s) en échec :")
        for f in failures[:5]:
            lines.append(f"• <code>{f['job_packet_id']}</code> — {f['status']}")
        send_to_channel("alerts", "\n".join(lines), source="strict_worker_failure_report")
    except Exception:
        pass


def main():
    failures = []
    scanned = 0

    if REPORTS_DIR.exists():
        for f in sorted(REPORTS_DIR.glob("*.json")):
            try:
                data = json.loads(f.read_text())
                scanned += 1
                status = data.get("status") or data.get("runner_result", {}).get("status", "")
                if str(status).upper() in FAILURE_STATUSES:
                    failures.append({
                        "file": f.name,
                        "status": status,
                        "job_packet_id": data.get("job_packet_id", data.get("job_id", "?")),
                        "reason": data.get("reason") or data.get("runner_result", {}).get("reason", ""),
                    })
            except (json.JSONDecodeError, OSError):
                pass

    report = {
        "job_id": "strict-worker-failure-report",
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "reports_scanned": scanned,
        "failure_count": len(failures),
        "failures": failures,
        "status": "WARN" if failures else "PASS",
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    if failures:
        _notify(failures)

if __name__ == "__main__":
    main()
