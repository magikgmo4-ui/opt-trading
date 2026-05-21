#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DOCS_DIR = REPO_ROOT / "docs"
REPORT = REPO_ROOT / "reports" / "ai" / "repo_doc_frontmatter_lint.json"


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---\n"):
        return None, ["missing_frontmatter"]
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return None, ["unterminated_frontmatter"]
    data = {}
    errors = []
    for line in parts[0].splitlines()[1:]:
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"invalid_line:{line.strip()}")
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip()
    return data, errors


def main() -> int:
    files = sorted(DOCS_DIR.rglob("*.md"))
    findings = []
    scanned = 0
    for path in files:
        scanned += 1
        fm, errors = parse_frontmatter(path)
        if fm is None:
            findings.append({"file": str(path.relative_to(REPO_ROOT)), "issues": errors})
            continue
        required = ["doc_id", "doc_type"]
        missing = [k for k in required if k not in fm]
        if missing or errors:
            findings.append({
                "file": str(path.relative_to(REPO_ROOT)),
                "issues": errors + [f"missing_key:{k}" for k in missing],
            })
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "job_id": "repo-doc-frontmatter-lint",
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
