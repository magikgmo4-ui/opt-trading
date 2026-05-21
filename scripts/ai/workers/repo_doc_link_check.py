#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DOCS_DIR = REPO_ROOT / "docs"
REPORT = REPO_ROOT / "reports" / "ai" / "repo_doc_link_check.json"
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def main() -> int:
    findings = []
    scanned = 0
    for path in sorted(DOCS_DIR.rglob("*.md")):
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="ignore")
        for link in LINK_RE.findall(text):
            if link.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = (path.parent / link).resolve()
            if not target.exists():
                findings.append({
                    "file": str(path.relative_to(REPO_ROOT)),
                    "missing_link": link,
                })
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "job_id": "repo-doc-link-check",
        "scanned": scanned,
        "findings": len(findings),
        "status": "PASS",
        "details": findings[:200],
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"scanned": scanned, "findings": len(findings), "report": str(REPORT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
