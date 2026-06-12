#!/usr/bin/env python3
"""Aggregate local LLM file audit JSON outputs into a Markdown report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any


def load_reports(input_dir: Path) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for path in sorted(input_dir.glob("*.json")):
        try:
            reports.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError as exc:
            reports.append(
                {
                    "file": str(path),
                    "file_type": "invalid_json",
                    "purpose": "Invalid JSON output",
                    "established": [],
                    "hypothesis": [],
                    "remaining_gap": [f"Invalid JSON: {exc}"],
                    "todo": ["Review invalid audit output manually."],
                    "risk": ["Audit output cannot be aggregated safely."],
                    "duplicate_candidate": [],
                    "patch_proposal": "",
                    "confidence": 0,
                }
            )
    return reports


def collect_items(reports: list[dict[str, Any]], key: str) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    for report in reports:
        source = str(report.get("file", "UNKNOWN"))
        for item in report.get(key, []) or []:
            if isinstance(item, str) and item.strip():
                items.append((source, item.strip()))
    return items


def render_section(title: str, items: list[tuple[str, str]], limit: int | None = None) -> str:
    if not items:
        return f"## {title}\n\n- Aucun élément.\n"
    selected = items if limit is None else items[:limit]
    lines = [f"## {title}", ""]
    for source, item in selected:
        lines.append(f"- `{source}` — {item}")
    return "\n".join(lines) + "\n"


def render_report(reports: list[dict[str, Any]]) -> str:
    confidences = [
        int(report.get("confidence", 0))
        for report in reports
        if isinstance(report.get("confidence", 0), int)
    ]
    avg_confidence = round(mean(confidences), 2) if confidences else 0

    lines = [
        "# Student Local LLM Audit Report",
        "",
        "## SUMMARY",
        "",
        f"- Files audited: {len(reports)}",
        f"- Average confidence: {avg_confidence}",
        "",
    ]

    lines.append(render_section("13_ESTABLISHED", collect_items(reports, "established")))
    lines.append(render_section("14_HYPOTHESIS", collect_items(reports, "hypothesis")))
    lines.append(render_section("15_REMAINING_GAP", collect_items(reports, "remaining_gap")))
    lines.append(render_section("16_TODO", collect_items(reports, "todo")))
    lines.append(render_section("RISKS", collect_items(reports, "risk")))
    lines.append(render_section("DUPLICATE_CANDIDATES", collect_items(reports, "duplicate_candidate")))

    patch_items = [
        (str(report.get("file", "UNKNOWN")), str(report.get("patch_proposal", "")).strip())
        for report in reports
        if str(report.get("patch_proposal", "")).strip()
    ]
    lines.append(render_section("PATCH_PROPOSALS", patch_items))

    lines.extend(
        [
            "## 17_RESUME_POINT",
            "",
            "```text",
            "review report → validate hallucination rate → decide extension or stop",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input directory containing JSON reports.")
    parser.add_argument("--output", required=True, help="Output Markdown report path.")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_report(load_reports(input_dir)), encoding="utf-8")
    print(f"Wrote report: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
