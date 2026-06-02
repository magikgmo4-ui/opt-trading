"""Digest of pending approvals from approval queue."""
import json, pathlib, datetime

APPROVAL_QUEUE = pathlib.Path("data/runtime_health/approvals_queue.json")
REPORT_PATH = pathlib.Path("reports/ai/pending_approvals_digest.json")


def main():
    if not APPROVAL_QUEUE.exists():
        digest = {"count": 0, "items": [], "note": "queue file not found — no pending approvals"}
        status = "PASS"
    else:
        try:
            queue = json.loads(APPROVAL_QUEUE.read_text())
            items = queue.get("approvals", [])
            digest = {"count": len(items), "items": items[:10]}
            status = "PASS"
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

if __name__ == "__main__":
    main()
