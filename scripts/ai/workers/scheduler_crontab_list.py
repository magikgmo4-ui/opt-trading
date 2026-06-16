#!/usr/bin/env python3
"""Emit current user crontab as a structured snapshot."""

from __future__ import annotations

import json
import subprocess
import sys


def main() -> int:
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    raw = result.stdout if result.returncode == 0 else ""
    entries = []
    comments = []
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            comments.append(stripped)
        else:
            entries.append(stripped)
    payload = {
        "status": "PASS",
        "entry_count": len(entries),
        "entries": entries,
        "comments": comments,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
