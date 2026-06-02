"""Digest of FAIL/BLOCKED/RUNNER_ERROR runner reports in reports/ai/workers/."""
import json, pathlib, datetime

REPORTS_DIR = pathlib.Path("reports/ai/workers")
REPORT_PATH = pathlib.Path("reports/ai/strict_worker_failure_report.json")

FAILURE_STATUSES = {"FAIL", "BLOCKED", "RUNNER_ERROR", "REFUSED", "INVALID_INPUT"}


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

if __name__ == "__main__":
    main()
