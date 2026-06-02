"""List active cron entries and report their count and schedule."""
import json, subprocess, datetime, pathlib, re

REPORT_PATH = pathlib.Path("reports/ai/scheduler_crontab_list.json")


def parse_crontab():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    if result.returncode != 0:
        return [], "no crontab installed"
    entries = []
    for line in result.stdout.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" in stripped[:20]:
            continue
        # Extract schedule and command
        parts = stripped.split(None, 5)
        if len(parts) >= 6:
            schedule = " ".join(parts[:5])
            command = parts[5]
            entries.append({"schedule": schedule, "command": command[:80]})
        elif len(parts) >= 2:
            entries.append({"schedule": parts[0], "command": " ".join(parts[1:])[:80]})
    return entries, None


def main():
    entries, error = parse_crontab()
    status = "PASS" if entries else "WARN"
    report = {
        "job_id": "scheduler-crontab-list",
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "active_entries": len(entries),
        "entries": entries,
        "error": error,
        "status": status,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps({"job_id": report["job_id"], "entries": len(entries),
                      "status": status}, indent=2))

if __name__ == "__main__":
    main()
