from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_consistency_pass_when_json_points_to_processed_png(tmp_path):
    inbox = tmp_path / "vision_inbox"
    processed = tmp_path / "vision_processed"
    inbox.mkdir()
    processed.mkdir()

    _write_json(
        inbox / "screen_tradingview_BTCUSDT.P_H1_2026-05-31_03-41-05.json",
        {"status": "ready", "symbol": "BTCUSDT.P"},
    )
    (processed / "screen_tradingview_BTCUSDT.P_H1_2026-05-31_03-41-05.png").write_bytes(b"png")

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "e2e" / "bot_vision_inbox_processed_consistency.py"),
            "--inbox",
            str(inbox),
            "--processed",
            str(processed),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    report = json.loads(result.stdout)
    assert report["overall_status"] == "PASS"
    assert report["counts"]["json_with_png_in_processed"] == 1


def test_consistency_warn_for_blocked_json_without_png(tmp_path):
    inbox = tmp_path / "vision_inbox"
    processed = tmp_path / "vision_processed"
    inbox.mkdir()
    processed.mkdir()

    _write_json(
        inbox / "screen_tradingview_BTCUSDT.P_H1_2026-05-31_03-41-05.json",
        {"status": "blocked", "symbol": "BTCUSDT.P"},
    )

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "e2e" / "bot_vision_inbox_processed_consistency.py"),
            "--inbox",
            str(inbox),
            "--processed",
            str(processed),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 2
    report = json.loads(result.stdout)
    assert report["overall_status"] == "WARN"
    assert report["counts"]["blocked_or_invalid_without_png"] == 1
    assert report["counts"]["true_orphan_json"] == 0


def test_consistency_fail_for_true_orphan_ready_json(tmp_path):
    inbox = tmp_path / "vision_inbox"
    processed = tmp_path / "vision_processed"
    inbox.mkdir()
    processed.mkdir()

    _write_json(
        inbox / "screen_tradingview_BTCUSDT.P_H1_2026-05-31_03-41-05.json",
        {"status": "ready", "symbol": "BTCUSDT.P"},
    )

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "e2e" / "bot_vision_inbox_processed_consistency.py"),
            "--inbox",
            str(inbox),
            "--processed",
            str(processed),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["overall_status"] == "FAIL"
    assert report["counts"]["true_orphan_json"] == 1
