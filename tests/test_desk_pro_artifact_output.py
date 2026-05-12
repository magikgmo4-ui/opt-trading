import json
from pathlib import Path

from modules.desk_pro.dry_run import (
    build_desk_pro_dry_run_report,
    build_desk_pro_dry_run_synthesis,
    run_desk_pro_dry_run,
    write_desk_pro_dry_run_artifacts,
)
from modules.desk_pro.signal_event_adapter import normalize_signal_event_v1


FIXTURES = Path(__file__).parent / "fixtures" / "admin_trading_contract_smoke"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class TestDeskProArtifactOutput:
    def test_writes_latest_json(self, tmp_path):
        v0 = _load("signal_event_v0_minimal.json")
        synthesis = run_desk_pro_dry_run(v0)
        meta = write_desk_pro_dry_run_artifacts(synthesis, tmp_path)
        latest_json = Path(meta["written_files"]["latest_json"])
        assert latest_json.exists()
        content = json.loads(latest_json.read_text(encoding="utf-8"))
        assert content["status"] == "WARN"

    def test_writes_latest_md(self, tmp_path):
        v0 = _load("signal_event_v0_minimal.json")
        synthesis = run_desk_pro_dry_run(v0)
        meta = write_desk_pro_dry_run_artifacts(synthesis, tmp_path)
        latest_md = Path(meta["written_files"]["latest_md"])
        assert latest_md.exists()
        text = latest_md.read_text(encoding="utf-8")
        assert "**Status:** WARN" in text

    def test_appends_history_jsonl(self, tmp_path):
        v0 = _load("signal_event_v0_minimal.json")
        for _ in range(3):
            synthesis = run_desk_pro_dry_run(v0)
            write_desk_pro_dry_run_artifacts(synthesis, tmp_path)
        history = Path(tmp_path / "history.jsonl")
        lines = history.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 3

    def test_latest_json_contains_safety_flags(self, tmp_path):
        v0 = _load("signal_event_v0_minimal.json")
        synthesis = run_desk_pro_dry_run(v0)
        meta = write_desk_pro_dry_run_artifacts(synthesis, tmp_path)
        latest_json = Path(meta["written_files"]["latest_json"])
        content = json.loads(latest_json.read_text(encoding="utf-8"))
        assert content["no_trade"] is True
        assert content["no_telegram"] is True
        assert content["no_webhook"] is True
        assert content["no_systemd"] is True

    def test_errors_empty_in_warn_artifact(self, tmp_path):
        v0 = _load("signal_event_v0_minimal.json")
        synthesis = run_desk_pro_dry_run(v0)
        meta = write_desk_pro_dry_run_artifacts(synthesis, tmp_path)
        latest_json = Path(meta["written_files"]["latest_json"])
        content = json.loads(latest_json.read_text(encoding="utf-8"))
        assert content["errors"] == []

    def test_missing_output_dir_created(self, tmp_path):
        out = tmp_path / "nonexistent" / "nested"
        v0 = _load("signal_event_v0_minimal.json")
        synthesis = run_desk_pro_dry_run(v0)
        meta = write_desk_pro_dry_run_artifacts(synthesis, out)
        latest_json = Path(meta["written_files"]["latest_json"])
        assert latest_json.exists()

    def test_no_write_outside_output_dir(self, tmp_path):
        other = tmp_path / "safe"
        other.mkdir()
        v0 = _load("signal_event_v0_minimal.json")
        synthesis = run_desk_pro_dry_run(v0)
        write_desk_pro_dry_run_artifacts(synthesis, tmp_path / "out")
        created = list((tmp_path / "out").glob("*"))
        assert len(created) == 3
        no_leak = list(other.iterdir())
        assert no_leak == []

    def test_report_render_contains_symbol(self):
        v0 = _load("signal_event_v0_minimal.json")
        v1 = normalize_signal_event_v1(v0)
        synthesis = build_desk_pro_dry_run_synthesis(v1)
        report = build_desk_pro_dry_run_report(synthesis)
        assert "BTCUSDT" in report

    def test_report_render_contains_direction(self):
        v0 = _load("signal_event_v0_minimal.json")
        v1 = normalize_signal_event_v1(v0)
        synthesis = build_desk_pro_dry_run_synthesis(v1)
        report = build_desk_pro_dry_run_report(synthesis)
        assert "BUY" in report
