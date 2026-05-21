#!/usr/bin/env python3
from __future__ import annotations

import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = REPO_ROOT / "reports" / "ai" / "workers"
ARCHIVE_DIR = REPO_ROOT / "data" / "runtime_health" / "job_logs" / "archive"
REPORT = REPO_ROOT / "reports" / "ai" / "strict_worker_log_archive.json"


def main() -> int:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    archive_path = ARCHIVE_DIR / f"strict_worker_reports_{ts}.tar.gz"
    files = sorted([p for p in SOURCE_DIR.iterdir() if p.is_file()]) if SOURCE_DIR.exists() else []
    with tarfile.open(archive_path, "w:gz") as tar:
        for path in files:
            tar.add(path, arcname=path.name)
    report = {
        "job_id": "strict-worker-log-archive",
        "archived_files": len(files),
        "archive": str(archive_path.relative_to(REPO_ROOT)),
        "status": "PASS",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
