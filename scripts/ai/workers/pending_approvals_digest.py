"""Digest of pending approvals from approval queue — alerts Telegram when approvals are waiting."""
import json, pathlib, datetime, sys

APPROVAL_QUEUE = pathlib.Path("data/runtime_health/approvals_queue.json")
REPORT_PATH = pathlib.Path("reports/ai/pending_approvals_digest.json")


def _notify(count: int, items: list) -> None:
    try:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
        from modules.env.env import load_env
        load_env()
        from shared.telegram_notify import send_telegram_html
        lines = [f"⏳ <b>pending-approvals-digest WARN</b>"]
        lines.append(f"{count} approbation(s) en attente :")
        for item in items[:5]:
            aid = item.get("approval_id", item.get("id", "?"))
            lines.append(f"• <code>{aid}</code>")
        send_telegram_html("\n".join(lines), source="pending_approvals_digest")
    except Exception:
        pass


def main():
    if not APPROVAL_QUEUE.exists():
        digest = {"count": 0, "items": [], "note": "queue file not found — no pending approvals"}
        status = "PASS"
    else:
        try:
            queue = json.loads(APPROVAL_QUEUE.read_text())
            items = queue.get("approvals", [])
            digest = {"count": len(items), "items": items[:10]}
            status = "WARN" if items else "PASS"
        except Exception as e:
            digest = {"count": 0, "items": [], "error": str(e)}
            status = "WARN"

    report = {
        "job_id": "pending-approvals-digest",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        **digest, "status": status,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps({"job_id": report["job_id"], "pending": digest["count"],
                      "status": status}, indent=2))
    if status == "WARN" and digest["count"] > 0:
        _notify(digest["count"], digest["items"])

if __name__ == "__main__":
    main()
