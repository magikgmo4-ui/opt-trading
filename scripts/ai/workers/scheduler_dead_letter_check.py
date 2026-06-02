"""Check cron logs for recent failures — dead-letter detection."""
import json, pathlib, datetime, re

LOGS_DIR = pathlib.Path("data/logs/cron")
REPORT_PATH = pathlib.Path("reports/ai/scheduler_dead_letter_check.json")
LOOKBACK_HOURS = 24
FAILURE_PATTERNS = [re.compile(p, re.IGNORECASE) for p in
                    [r'\bERROR\b', r'\bFAIL\b', r'\bTraceback\b', r'\bException\b']]


def scan_logs():
    failures = []
    if not LOGS_DIR.exists():
        return failures, "cron logs directory not found"
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(hours=LOOKBACK_HOURS)
    for log in sorted(LOGS_DIR.glob("*.log")):
        try:
            mtime = datetime.datetime.utcfromtimestamp(log.stat().st_mtime)
            if mtime < cutoff:
                continue
            for lineno, line in enumerate(log.read_text(errors="ignore").splitlines(), 1):
                if any(p.search(line) for p in FAILURE_PATTERNS):
                    failures.append({"log": log.name, "line": lineno, "content": line[:120]})
                    if len(failures) >= 20:
                        return failures, None
        except OSError:
            pass
    return failures, None


def main():
    failures, error = scan_logs()
    status = "WARN" if failures else "PASS"
    report = {
        "job_id": "scheduler-dead-letter-check",
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "lookback_hours": LOOKBACK_HOURS,
        "failures_found": len(failures),
        "failures": failures,
        "error": error,
        "status": status,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps({"job_id": report["job_id"], "failures": len(failures),
                      "status": status}, indent=2))

if __name__ == "__main__":
    main()
