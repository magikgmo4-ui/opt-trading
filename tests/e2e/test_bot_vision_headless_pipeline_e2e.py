from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

from modules.desk_pro.service.telegram_claim_reader import read_telegram_claim
from modules.desk_pro.service.vision_analysis_reader import read_vision_analysis
from modules.desk_pro.service.vision_context_reader import read_vision_context_coinglass


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = PROJECT_ROOT / "modules" / "bot_vision" / "headless_capture" / "scripts"


def _load_script(name: str):
    path = SCRIPTS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, str(path))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_chart_pipeline_roundtrip_to_data_center_deskpro_and_telegram(tmp_path, monkeypatch):
    vaw = _load_script("vision_analysis_writer")
    sv = _load_script("signal_validator")
    tf = _load_script("telegram_filter")

    deskpro_dir = tmp_path / "data" / "deskpro" / "inputs" / "vision_analysis"
    dc_dir = tmp_path / "data" / "data_center" / "views" / "vision_analysis"
    by_symbol_dir = dc_dir / "by_symbol"
    history_dir = dc_dir / "history"
    cooldown_state = tmp_path / "data" / "bot_vision" / "telegram_cooldown" / "cooldown_state.json"

    monkeypatch.setattr(vaw, "DESKPRO_VISION_ANALYSIS_DIR", deskpro_dir)
    monkeypatch.setattr(vaw, "DC_VISION_ANALYSIS_DIR", dc_dir)
    monkeypatch.setattr(vaw, "DC_VISION_BY_SYMBOL_DIR", by_symbol_dir)
    monkeypatch.setattr(vaw, "DC_VISION_HISTORY_DIR", history_dir)
    monkeypatch.setattr(sv, "DC_VISION_ANALYSIS_DIR", dc_dir)
    monkeypatch.setattr(sv, "DC_VISION_BY_SYMBOL_DIR", by_symbol_dir)
    monkeypatch.setattr(tf, "COOLDOWN_STATE_PATH", cooldown_state)
    monkeypatch.setattr(tf, "COOLDOWN_STATE_DIR", cooldown_state.parent)

    summary_15m = {
        "run_id": "run_btc_15m",
        "ts": "2026-05-31T10:00:00Z",
        "analysis_text": "Support à 65000\nRésistance à 68500\nTendance: bullish",
        "source_screenshot": "btc_15m.png",
    }
    summary_1h = {
        "run_id": "run_btc_1h",
        "ts": "2026-05-31T11:00:00Z",
        "analysis_text": "Support à 65000\nRésistance à 68500\nTrend bullish",
        "source_screenshot": "btc_1h.png",
    }
    meta_15m = {"symbol": "BTCUSDT.P", "timeframe": "15m", "screen_type": "CHART_TECHNICAL"}
    meta_1h = {"symbol": "BTCUSDT.P", "timeframe": "1h", "screen_type": "CHART_TECHNICAL"}

    data_15m = vaw.build_vision_analysis(summary_15m, meta_15m)
    data_1h = vaw.build_vision_analysis(summary_1h, meta_1h)

    vaw.write_deskpro(data_15m)
    vaw.write_data_center(data_15m)
    vaw.write_deskpro(data_1h)
    vaw.write_data_center(data_1h)

    deskpro_latest = deskpro_dir / "latest.json"
    deskpro_payload = read_vision_analysis(path=deskpro_latest)
    assert deskpro_payload is not None
    assert deskpro_payload["input_class"] == "vision_analysis.v1"
    assert deskpro_payload["timeframe"] == "1h"
    assert deskpro_payload["symbol"] == "BTCUSDT.P"

    by_symbol_payload = json.loads((by_symbol_dir / "BTCUSDT.P.json").read_text(encoding="utf-8"))
    assert isinstance(by_symbol_payload, list)
    assert len(by_symbol_payload) == 2
    assert {item["timeframe"] for item in by_symbol_payload} == {"15m", "1h"}

    by_tf = sv.load_all_timeframes("BTCUSDT.P")
    validated = sv.cross_validate(by_tf)
    assert validated["confirmed_count"] >= 1
    assert set(validated["timeframes_checked"]) == {"15m", "1h"}
    assert any(sig.get("cross_validated") for sig in validated["validated_signals"])

    telegram_input = {
        "run_id": summary_1h["run_id"],
        "analysis_text": summary_1h["analysis_text"],
        "signals": validated["validated_signals"],
    }
    filtered = tf.filter_signals(telegram_input, 0.70)
    telegram_result = tf.build_telegram_summary(telegram_input, filtered, 0.70)
    assert telegram_result["send"] is True
    assert telegram_result["filtered_signal_count"] >= 1
    assert "confidence" in telegram_result["reason"]
    assert "Support" in telegram_result["summary"] or "Trend" in telegram_result["summary"]

    assert read_telegram_claim(path=tmp_path / "data" / "deskpro" / "inputs" / "telegram_claim" / "latest.json") is None


def test_coinglass_writer_roundtrip_to_deskpro_reader(tmp_path, monkeypatch):
    vcw = _load_script("vision_context_writer")

    deskpro_dir = tmp_path / "data" / "deskpro" / "inputs" / "vision_context" / "coinglass"
    deskpro_path = deskpro_dir / "latest.json"
    dc_dir = tmp_path / "data" / "data_center" / "views" / "vision_context" / "coinglass"
    history_dir = dc_dir / "history"

    monkeypatch.setattr(vcw, "DESKPRO_VISION_CONTEXT_DIR", deskpro_dir)
    monkeypatch.setattr(vcw, "DESKPRO_VISION_CONTEXT_PATH", deskpro_path)
    monkeypatch.setattr(vcw, "DC_VISION_CONTEXT_DIR", dc_dir)
    monkeypatch.setattr(vcw, "DC_VISION_CONTEXT_HISTORY", history_dir)

    payload = {
        "input_class": "vision_context.coinglass.v1",
        "source_id": "coinglass_headless_bot",
        "analysis_ts": "2026-05-31T11:15:00Z",
        "screenshot_ts": "2026-05-31T11:10:00Z",
        "symbol": "BTCUSDT.P",
        "timeframe": "1H",
        "board": "liquidations",
        "page": "liquidation_heatmap",
        "freshness_state": "fresh",
        "detections": [
            {
                "detected_metric_type": "liquidations_long",
                "extracted_value": 48500000.0,
                "unit": "USD",
                "confidence": 0.82,
                "evidence_ref": "cg.png",
                "notes": "",
            },
            {
                "detected_metric_type": "liquidations_short",
                "extracted_value": 21300000.0,
                "unit": "USD",
                "confidence": 0.78,
                "evidence_ref": "cg.png",
                "notes": "",
            },
        ],
        "warnings": [],
        "refs": {
            "raw_screenshot": "cg.png",
            "normalized": "normalized.json",
            "latest": "latest.json",
            "events": "events.jsonl",
        },
    }

    assert vcw.validate(payload) is True
    vcw.write_deskpro(payload)
    vcw.write_data_center(payload)

    metrics = read_vision_context_coinglass(path=deskpro_path)
    assert len(metrics) == 2
    assert {m.metric for m in metrics} == {"liquidations_long", "liquidations_short"}
    assert all(m.asset == "BTCUSDT.P" for m in metrics)
    assert (dc_dir / "latest.json").exists()
    assert len(list(history_dir.glob("BTCUSDT.P_*.json"))) == 1


def test_run_vision_pipeline_full_chart_execution_path_uses_validated_signals_for_telegram(tmp_path, monkeypatch, capsys):
    rvp = _load_script("run_vision_pipeline")

    inbox_dir = tmp_path / "vision_inbox"
    inbox_dir.mkdir(parents=True, exist_ok=True)
    sidecar = inbox_dir / "screen_btc.json"
    sidecar.write_text(
        json.dumps(
            {
                "screen_type": "CHART_TECHNICAL",
                "symbol": "BTCUSDT.P",
                "timeframe": "1h",
                "status": "ready",
                "png_path": str(tmp_path / "btc.png"),
            }
        ),
        encoding="utf-8",
    )

    summary_payload = {
        "run_id": "run_pipeline_chart",
        "analysis_text": "Support à 65000\nRésistance à 68500\nTrend bullish",
        "signals": [],
    }
    validated_payload = {
        "validated_signal_count": 2,
        "confirmed_count": 1,
        "deduped_count": 1,
        "validated_signals": [
            {"type": "support_level", "value": 65000.0, "confidence": 0.9, "symbol": "BTCUSDT.P", "cross_validated": True},
            {"type": "trend_direction", "value": "bullish", "confidence": 0.85, "symbol": "BTCUSDT.P", "cross_validated": False},
        ],
    }

    calls: list[dict[str, object]] = []

    def fake_run(cmd, *args, **kwargs):
        cmd_list = list(cmd)
        calls.append({"cmd": cmd_list, "input": kwargs.get("input")})
        script = cmd_list[1] if len(cmd_list) > 1 else ""

        if script == str(rvp.VISION_ANALYSIS_WRITER):
            return subprocess.CompletedProcess(cmd_list, 0, stdout="OK: vision_analysis published\n", stderr="")

        if script == str(rvp.SIGNAL_VALIDATOR):
            return subprocess.CompletedProcess(cmd_list, 0, stdout=json.dumps(validated_payload), stderr="")

        if script == str(rvp.TELEGRAM_FILTER_SCRIPT):
            assert "--stdin" in cmd_list
            forwarded = json.loads(kwargs.get("input") or "{}")
            assert forwarded["run_id"] == summary_payload["run_id"]
            assert forwarded["signals"] == validated_payload["validated_signals"]
            return subprocess.CompletedProcess(
                cmd_list,
                0,
                stdout=json.dumps(
                    {
                        "send": True,
                        "reason": "2 signal(s) above 70% confidence",
                        "summary": "Support à 65000\nTrend bullish",
                        "filtered_signal_count": 2,
                        "run_id": summary_payload["run_id"],
                    }
                ),
                stderr="",
            )

        raise AssertionError(f"Unexpected subprocess call: {cmd_list}")

    monkeypatch.setattr(rvp, "VISION_INBOX", inbox_dir)
    monkeypatch.setattr(rvp, "DESKPRO_VISION_ANALYSIS_DIR", tmp_path / "deskpro" / "inputs" / "vision_analysis")
    monkeypatch.setattr(rvp, "DESKPRO_VISION_ANALYSIS_PATH", tmp_path / "deskpro" / "inputs" / "vision_analysis" / "latest.json")
    monkeypatch.setattr(rvp, "find_latest_capture", lambda inbox: json.loads(sidecar.read_text(encoding="utf-8")))
    monkeypatch.setattr(rvp, "delegate_to_bot_vision_step2", lambda meta: 0)
    monkeypatch.setattr(rvp, "_read_latest_summary", lambda: dict(summary_payload))
    monkeypatch.setattr(rvp.subprocess, "run", fake_run)

    import sys

    old_argv = sys.argv[:]
    try:
        sys.argv = ["run_vision_pipeline.py", "--skip-capture", "--no-telegram"]
        rc = rvp.main()
    finally:
        sys.argv = old_argv

    assert rc == 0
    out = capsys.readouterr().out
    assert "OK: bot_vision_step2 analysis complete" in out
    assert "Validated: 2 signals (1 confirmed, 1 deduplicated)" in out
    assert "Decision: SKIP (2 signal(s) above 70% confidence)" in out
    assert any(call["cmd"][1] == str(rvp.VISION_ANALYSIS_WRITER) for call in calls)
    assert any(call["cmd"][1] == str(rvp.SIGNAL_VALIDATOR) for call in calls)
    assert any(call["cmd"][1] == str(rvp.TELEGRAM_FILTER_SCRIPT) for call in calls)
