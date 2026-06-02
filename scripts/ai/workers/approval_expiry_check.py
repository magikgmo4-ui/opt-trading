"""Check approval queue for expired entries — alerts Telegram on expiry."""
import json, pathlib, datetime, sys

APPROVAL_QUEUE = pathlib.Path("data/runtime_health/approvals_queue.json")
REPORT_PATH = pathlib.Path("reports/ai/approval_expiry_check.json")
EXPIRY_HOURS = 24


def _notify(expired: list) -> None:
    try:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
        from shared.telegram_notify import send_telegram_html
        lines = [f"⚠️ <b>approval-expiry-check WARN</b>"]
        lines.append(f"{len(expired)} approbation(s) expirée(s) (>{EXPIRY_HOURS}h) :")
        for e in expired[:5]:
            lines.append(f"• <code>{e['id']}</code> — {e['age_hours']}h")
        send_telegram_html("\n".join(lines), source="approval_expiry_check")
    except Exception:
        pass


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
    if status == "WARN" and expired:
        _notify(expired)

if __name__ == "__main__":
    main()
