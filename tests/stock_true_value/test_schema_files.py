from __future__ import annotations

import json
from pathlib import Path


def _load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_schema_files_are_valid_json() -> None:
    score_schema = _load("schemas/stock_true_value/score_snapshot.schema.json")
    output_schema = _load("schemas/stock_true_value/output.schema.json")
    spacex_schema = _load("schemas/ipo/spacex_true_value_final.v1.schema.json")

    assert score_schema["title"] == "Stock True Value Score Snapshot"
    assert output_schema["title"] == "SpaceX True Value Final Daily Output"
    assert spacex_schema["title"] == "SpaceX True Value Final Daily Output"


def test_fixture_is_valid_json() -> None:
    payload = _load("fixtures/stock_true_value/sample_scores_input.json")
    assert payload["model_version"] == "spacex_true_value_final_v1"
    assert len(payload["items"]) >= 3
