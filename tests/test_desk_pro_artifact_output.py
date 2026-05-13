import json
from pathlib import Path

from modules.desk_pro.dry_run import (
    build_desk_pro_dry_run_report,
    build_desk_pro_dry_run_synthesis,
    load_latest_desk_snapshot,
    load_latest_visual_context,
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


class TestDeskSnapshotInput:
    def test_load_latest_snapshot_returns_matching_entry(self, tmp_path):
        index = {
            "BTCUSDT.P": {"symbol": "BTCUSDT.P", "tf": "H1", "snapshot_ts": "2026-05-12T23:55:46", "path": "/tmp/test.png"},
        }
        f = tmp_path / "index.json"
        f.write_text(json.dumps(index))
        result = load_latest_desk_snapshot(f, target_symbol="BTCUSDT")
        assert result is not None
        assert result["symbol"] == "BTCUSDT.P"

    def test_load_latest_snapshot_returns_none_if_missing(self, tmp_path):
        f = tmp_path / "nonexistent.json"
        result = load_latest_desk_snapshot(f, target_symbol="BTCUSDT")
        assert result is None

    def test_load_latest_snapshot_returns_none_if_no_match(self, tmp_path):
        index = {"ETHUSDT.P": {"symbol": "ETHUSDT.P", "tf": "H1", "snapshot_ts": "now", "path": "/tmp/e.png"}}
        f = tmp_path / "index.json"
        f.write_text(json.dumps(index))
        result = load_latest_desk_snapshot(f, target_symbol="BTCUSDT")
        assert result is None

    def test_dry_run_with_filled_snapshot_shows_present(self, tmp_path):
        snap = {"symbol": "BTCUSDT.P", "tf": "H1", "snapshot_ts": "now", "path": "/tmp/test.png"}
        v0 = _load("signal_event_v0_minimal.json")
        result = run_desk_pro_dry_run(v0, desk_snapshot=snap)
        assert result["summary"]["desk_snapshot_present"] is True
        assert "desk_snapshot missing" not in str(result["warnings"])

    def test_snapshot_enrichment_keeps_safety_flags(self, tmp_path):
        snap = {"symbol": "BTCUSDT.P", "tf": "H1", "snapshot_ts": "now", "path": "/tmp/test.png"}
        v0 = _load("signal_event_v0_minimal.json")
        result = run_desk_pro_dry_run(v0, desk_snapshot=snap)
        assert result["no_trade"] is True
        assert result["no_telegram"] is True
        assert result["no_webhook"] is True
        assert result["no_systemd"] is True


class TestVisualContextInput:
    def test_load_visual_context_from_file(self, tmp_path):
        vc = _load("visual_context_v1_minimal.json")
        f = tmp_path / "vc.json"
        f.write_text(json.dumps(vc))
        result = load_latest_visual_context(f)
        assert result is not None
        assert result["capture_id"] == vc["capture_id"]

    def test_load_visual_context_none_if_missing(self, tmp_path):
        f = tmp_path / "nonexistent.json"
        result = load_latest_visual_context(f)
        assert result is None

    def test_dry_run_with_visual_context_resolves_warning(self, tmp_path):
        vc = _load("visual_context_v1_minimal.json")
        snap = {"symbol": "BTCUSDT.P", "tf": "H1", "snapshot_ts": "now", "path": "/tmp/test.png"}
        v0 = _load("signal_event_v0_minimal.json")
        result = run_desk_pro_dry_run(v0, visual_context=vc, desk_snapshot=snap)
        assert result["summary"]["visual_context_present"] is True
        assert "visual_context missing" not in str(result["warnings"])

    def test_dry_run_combined_inputs_returns_pass(self, tmp_path):
        vc = _load("visual_context_v1_minimal.json")
        snap = {"symbol": "BTCUSDT.P", "tf": "H1", "snapshot_ts": "now", "path": "/tmp/test.png"}
        v0 = _load("signal_event_v0_complete.json")
        result = run_desk_pro_dry_run(v0, visual_context=vc, desk_snapshot=snap)
        assert result["summary"]["visual_context_present"] is True
        assert result["summary"]["desk_snapshot_present"] is True
        assert "missing" not in str(result["warnings"])

    def test_combined_inputs_keep_safety_flags(self, tmp_path):
        vc = _load("visual_context_v1_minimal.json")
        snap = {"symbol": "BTCUSDT.P", "tf": "H1", "snapshot_ts": "now", "path": "/tmp/test.png"}
        v0 = _load("signal_event_v0_complete.json")
        result = run_desk_pro_dry_run(v0, visual_context=vc, desk_snapshot=snap)
        assert result["no_trade"] is True
        assert result["no_telegram"] is True
        assert result["no_webhook"] is True
        assert result["no_systemd"] is True
