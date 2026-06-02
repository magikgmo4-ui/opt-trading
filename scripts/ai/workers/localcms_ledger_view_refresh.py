"""Refresh localcms ledger view — reads ledger, writes rendered summary."""
import json, pathlib, datetime

LEDGER_FILE = pathlib.Path("data/ledger/ledger.jsonl")
LOCALCMS_DIR = pathlib.Path("tmp")
OUT_FILE = LOCALCMS_DIR / "localcms_ledger_view.json"
REPORT_PATH = pathlib.Path("reports/ai/localcms_ledger_view_refresh.json")
MAX_EVENTS = 50


def read_ledger_tail(n: int) -> list[dict]:
    if not LEDGER_FILE.exists():
        return []
    events = []
    for line in LEDGER_FILE.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return events[-n:]


def main():
    events = read_ledger_tail(MAX_EVENTS)
    view = {
        "surface": "localcms_ledger_view",
        "refreshed_at": datetime.datetime.utcnow().isoformat() + "Z",
        "event_count": len(events),
        "latest_events": events,
    }
    LOCALCMS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(view, indent=2))

    report = {
        "job_id": "localcms-ledger-view-refresh",
        "refreshed_at": view["refreshed_at"],
        "events_rendered": len(events),
        "output": str(OUT_FILE),
        "status": "PASS" if events else "WARN",
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
