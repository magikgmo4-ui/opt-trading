"""Check approval queue for expired entries — reads approval state if present."""
import json, pathlib, datetime

APPROVAL_QUEUE = pathlib.Path("data/runtime_health/approvals_queue.json")
REPORT_PATH = pathlib.Path("reports/ai/approval_expiry_check.json")
EXPIRY_HOURS = 24


def main():
    findings = []
    expired, pending = [], []

    if not APPROVAL_QUEUE.exists():
        findings.append(f"approvals_queue.json not found at {APPROVAL_QUEUE} — queue empty")
        status = "WARN"
    else:
        try:
            queue = json.loads(APPROVAL_QUEUE.read_text())
            now = datetime.datetime.utcnow()
            for entry in queue.get("approvals", []):
                created = entry.get("created_at", "")
                approval_id = entry.get("approval_id", "?")
                try:
                    created_dt = datetime.datetime.fromisoformat(created.rstrip("Z"))
                    age_h = (now - created_dt).total_seconds() / 3600
                    if age_h > EXPIRY_HOURS:
                        expired.append({"id": approval_id, "age_hours": round(age_h, 1)})
                    else:
                        pending.append(approval_id)
                except ValueError:
                    pending.append(approval_id)
        except (json.JSONDecodeError, OSError) as e:
            findings.append(f"queue read error: {e}")
        status = "WARN" if expired else "PASS"

    report = {
        "job_id": "approval-expiry-check",
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "pending_count": len(pending),
        "expired_count": len(expired),
        "expired": expired,
        "findings": findings,
        "status": status,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps({"job_id": report["job_id"], "pending": len(pending),
                      "expired": len(expired), "status": status}, indent=2))

if __name__ == "__main__":
    main()
