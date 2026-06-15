from __future__ import annotations

import json
from pathlib import Path

from modules.stock_true_value.cli import run_fixture_only


def test_fixture_only_cli_writes_outputs(tmp_path: Path) -> None:
    output = run_fixture_only(
        fixture_path=Path("fixtures/stock_true_value/sample_scores_input.json"),
        output_root=tmp_path / "stock_true_value",
    )
    scores_path = tmp_path / "stock_true_value" / "latest" / "scores.json"
    summary_path = tmp_path / "stock_true_value" / "latest" / "summary.md"

    assert scores_path.exists()
    assert summary_path.exists()
    payload = json.loads(scores_path.read_text(encoding="utf-8"))
    assert payload["model_version"] == "spacex_true_value_final_v1"
    assert len(payload["items"]) == len(output["items"])
    assert all("confidence_score" in item for item in payload["items"])
    assert all("source_health" in item for item in payload["items"])
