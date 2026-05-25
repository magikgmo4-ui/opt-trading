import json
from pathlib import Path

from modules.desk_pro.service.vision_analysis_reader import read_vision_analysis

FIXTURES = Path(__file__).parent / "fixtures" / "admin_trading_contract_smoke"
_FIXTURE = FIXTURES / "vision_analysis_v1_minimal.json"


class TestVisionAnalysisReaderFixture:
    def test_fixture_file_exists(self):
        assert _FIXTURE.exists(), f"Fixture not found: {_FIXTURE}"

    def test_fixture_is_valid_vision_analysis_v1(self):
        data = json.loads(_FIXTURE.read_text(encoding="utf-8"))
        assert data["input_class"] == "vision_analysis.v1"
        assert "capture_id" in data
        assert "symbol" in data
        assert "analysis_ts" in data
        assert isinstance(data.get("signals"), list)

    def test_fixture_has_signals(self):
        data = json.loads(_FIXTURE.read_text(encoding="utf-8"))
        assert len(data["signals"]) > 0

    def test_read_vision_analysis_from_fixture_returns_dict(self, tmp_path):
        fixture_data = json.loads(_FIXTURE.read_text(encoding="utf-8"))
        path = tmp_path / "vision_analysis_latest.json"
        path.write_text(json.dumps(fixture_data), encoding="utf-8")
        result = read_vision_analysis(path=path)
        assert result is not None
        assert isinstance(result, dict)

    def test_read_vision_analysis_from_fixture_has_correct_class(self, tmp_path):
        fixture_data = json.loads(_FIXTURE.read_text(encoding="utf-8"))
        path = tmp_path / "va.json"
        path.write_text(json.dumps(fixture_data), encoding="utf-8")
        result = read_vision_analysis(path=path)
        assert result["input_class"] == "vision_analysis.v1"

    def test_read_vision_analysis_from_fixture_has_signals(self, tmp_path):
        fixture_data = json.loads(_FIXTURE.read_text(encoding="utf-8"))
        path = tmp_path / "va.json"
        path.write_text(json.dumps(fixture_data), encoding="utf-8")
        result = read_vision_analysis(path=path)
        assert len(result["signals"]) > 0


class TestVisionAnalysisReaderEdgeCases:
    def test_returns_none_if_file_absent(self, tmp_path):
        result = read_vision_analysis(path=tmp_path / "nonexistent.json")
        assert result is None

    def test_returns_none_if_wrong_input_class(self, tmp_path):
        path = tmp_path / "va.json"
        path.write_text(json.dumps({"input_class": "other.v1", "data": 1}), encoding="utf-8")
        result = read_vision_analysis(path=path)
        assert result is None

    def test_returns_none_if_malformed_json(self, tmp_path):
        path = tmp_path / "va.json"
        path.write_text("not json {{{{", encoding="utf-8")
        result = read_vision_analysis(path=path)
        assert result is None

    def test_returns_none_if_not_dict(self, tmp_path):
        path = tmp_path / "va.json"
        path.write_text(json.dumps([1, 2, 3]), encoding="utf-8")
        result = read_vision_analysis(path=path)
        assert result is None
