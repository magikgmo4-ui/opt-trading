"""Sync strict worker runner reports → localcms worker state view."""
import json, pathlib, datetime

RUNNERS_DIR = pathlib.Path("reports/ai/workers")
LOCALCMS_DIR = pathlib.Path("tmp")
OUT_FILE = LOCALCMS_DIR / "localcms_workers_state.json"
REPORT_PATH = pathlib.Path("reports/ai/localcms_workers_state_sync.json")


def collect_worker_states():
    states = []
    if not RUNNERS_DIR.exists():
        return states
    for f in sorted(RUNNERS_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text())
            states.append({
                "report": f.name,
                "status": data.get("status", data.get("runner_result", {}).get("status", "?")),
                "job_id": data.get("job_packet_id", data.get("job_id", f.stem)),
                "completed_at": data.get("completed_at", ""),
            })
        except (json.JSONDecodeError, OSError):
            pass
    return states


def main():
    states = collect_worker_states()
    snapshot = {
        "surface": "localcms_workers_state",
        "synced_at": datetime.datetime.utcnow().isoformat() + "Z",
        "worker_reports": len(states),
        "states": states,
    }
    LOCALCMS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(snapshot, indent=2))

    report = {
        "job_id": "localcms-workers-state-sync",
        "synced_at": snapshot["synced_at"],
        "reports_synced": len(states),
        "output": str(OUT_FILE),
        "status": "PASS",
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
