from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict
from pathlib import Path

from .scanner import Finding


def write_reports(findings: list[Finding], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    by_surface = Counter(item.surface for item in findings)
    md_path = output_dir / "naming_audit_report.md"
    json_path = output_dir / "naming_audit_report.json"

    lines = [
        "# naming_audit_report",
        "",
        "## Summary",
        f"- total_findings: {len(findings)}",
    ]
    for surface, count in sorted(by_surface.items()):
        lines.append(f"- {surface}: {count}")
    if not findings:
        lines.extend(["", "## Result", "- no findings"])
    else:
        lines.extend(["", "## Findings", "| surface | path | current | proposal | reason |", "| --- | --- | --- | --- | --- |"])
        for item in findings:
            lines.append(
                f"| {item.surface} | `{item.path}` | `{item.current_name}` | `{item.proposed_name}` | {item.reason} |"
            )

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    json_path.write_text(json.dumps([asdict(item) for item in findings], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return md_path, json_path
