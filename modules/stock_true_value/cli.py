"""Fixture-only CLI for SpaceX True Value Final.

This command reads fixtures and writes local outputs only.
No live collectors. No registry writes. No alerts.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from .scoring_engine import MODEL_VERSION, compute_score_snapshot


def _parse_asof(value: str) -> datetime:
    return datetime.fromisoformat(value)


def run_fixture_only(
    fixture_path: Path = Path("fixtures/stock_true_value/sample_scores_input.json"),
    output_root: Path = Path("outputs/stock_true_value"),
) -> dict:
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    asof = _parse_asof(payload["asof"])
    items = []
    for item in payload["items"]:
        snapshot = compute_score_snapshot(
            ticker=item["ticker"],
            universe=item["universe"],
            raw_scores=item["raw_scores"],
            source_health_payload=item.get("source_health_payload") or {},
            asof=asof,
        )
        items.append(snapshot.to_dict())

    output = {
        "asof": asof.isoformat(),
        "model_version": MODEL_VERSION,
        "universe": payload.get("universe", "FIXTURE_ONLY"),
        "items": items,
        "summary": {
            "count": len(items),
            "low_confidence_count": sum(1 for x in items if x["confidence_score"] < 60),
            "grades": {grade: sum(1 for x in items if x["final_grade"] == grade) for grade in ["A+", "A", "B", "C", "D", "RESEARCH_REQUIRED"]},
        },
    }

    latest = output_root / "latest"
    latest.mkdir(parents=True, exist_ok=True)
    (latest / "scores.json").write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (latest / "summary.md").write_text(_summary_markdown(output), encoding="utf-8")
    return output


def _summary_markdown(output: dict) -> str:
    lines = [
        "# Stock / SpaceX True Value Fixture Summary",
        "",
        f"- asof: `{output['asof']}`",
        f"- model_version: `{output['model_version']}`",
        f"- items: `{len(output['items'])}`",
        "",
        "| Ticker | Grade | True Value | Hype | Risk | Confidence | Action |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for item in output["items"]:
        lines.append(
            f"| {item['ticker']} | {item['final_grade']} | {item['true_value_score']} | {item['hype_score']} | {item['risk_score']} | {item['confidence_score']} | {item['action_bias']} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture-only", action="store_true", help="Run without live collectors.")
    parser.add_argument("--fixture", default="fixtures/stock_true_value/sample_scores_input.json")
    parser.add_argument("--output-root", default="outputs/stock_true_value")
    args = parser.parse_args()

    if not args.fixture_only:
        raise SystemExit("Only --fixture-only is supported in this consolidated bundle.")

    output = run_fixture_only(Path(args.fixture), Path(args.output_root))
    print(json.dumps({"ok": True, "items": len(output["items"]), "output": str(Path(args.output_root) / "latest" / "scores.json")}, indent=2))


if __name__ == "__main__":
    main()
