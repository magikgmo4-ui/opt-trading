"""Tests for SPCX V2 export layer — Desk, Telegram, Sheets, Daily Summary."""

import json
import pytest
from pathlib import Path

from modules.spcx_v2.config import SetupCandidate, ScoreSet, OUTPUT_DIR
from modules.spcx_v2.paper_logger import log_candidate, log_reject, log_result
from modules.spcx_v2.export_desk import get_desk_status, get_desk_candidates, get_desk_stats, export_desk_json
from modules.spcx_v2.export_telegram import _format_alert, _load_sent_ids, _save_sent_ids
from modules.spcx_v2.export_sheets import _candidate_to_row, build_export_rows, export_to_jsonl, export_to_csv
from modules.spcx_v2.daily_summary import generate_daily_summary, write_daily_markdown


@pytest.fixture(autouse=True)
def temp_output_dir(monkeypatch, tmp_path):
    monkeypatch.setattr("modules.spcx_v2.paper_logger.OUTPUT_DIR", tmp_path)
    monkeypatch.setattr("modules.spcx_v2.config.OUTPUT_DIR", tmp_path)
    monkeypatch.setattr("modules.spcx_v2.export_telegram.OUTPUT_DIR", tmp_path)
    monkeypatch.setattr("modules.spcx_v2.export_telegram._SENT_CACHE_FILE", tmp_path / "telegram_sent.json")
    monkeypatch.setattr("modules.spcx_v2.export_sheets.OUTPUT_DIR", tmp_path)
    monkeypatch.setattr("modules.spcx_v2.daily_summary.PROJECT_ROOT", tmp_path)
    return tmp_path


def make_candidate(grade="A", setup_type="IPO_ORB_15M"):
    return SetupCandidate(
        symbol="SPCX",
        ts="2026-06-12T14:30:00Z",
        setup_type=setup_type,
        grade=grade,
        status="paper_only",
        scores=ScoreSet(trade_ready=78, liquidity=72, risk=38, smart_money=70, catalyst=65),
        reason_codes=["ORB_BREAK", "VWAP_ALIGNED"],
    )


# ── Desk Export ──────────────────────────────────────────────────────
def test_desk_status(tmp_path):
    log_candidate(make_candidate("A"))
    log_candidate(make_candidate("A+", "VWAP_RECLAIM"))
    log_reject(make_candidate("reject"))
    status = get_desk_status()
    assert status["status"] == "paper_only"
    assert status["totals"]["candidates"] == 2
    assert status["totals"]["rejects"] == 1
    assert "A" in status["by_grade"]
    assert len(status["recent_candidates"]) == 2


def test_desk_candidates(tmp_path):
    log_candidate(make_candidate("A"))
    log_candidate(make_candidate("B"))
    candidates = get_desk_candidates()
    assert len(candidates) == 2
    assert candidates[0]["grade"] == "A"


def test_desk_candidates_grade_filter(tmp_path):
    log_candidate(make_candidate("A"))
    log_candidate(make_candidate("B"))
    a_only = get_desk_candidates(grade="A")
    assert len(a_only) == 1
    assert a_only[0]["grade"] == "A"


def test_desk_stats(tmp_path):
    log_candidate(make_candidate("A"))
    log_candidate(make_candidate("A+", "VWAP_RECLAIM"))
    stats = get_desk_stats()
    assert stats["by_grade"]["A"] == 1
    assert stats["by_grade"]["A+"] == 1
    assert "winrate" in stats


def test_export_desk_json(tmp_path):
    log_candidate(make_candidate("A"))
    path = export_desk_json()
    assert path.exists()
    with open(path) as f:
        data = json.load(f)
    assert data["status"] == "paper_only"


# ── Telegram Export ──────────────────────────────────────────────────
def test_format_alert():
    c = make_candidate("A+")
    msg = _format_alert(c)
    assert "[A+]" in msg
    assert "SPCX" in msg
    assert "TR78" in msg
    assert "LQ72" in msg


def test_sent_ids_persistence(tmp_path):
    ids = {"abc123", "def456"}
    _save_sent_ids(ids)
    loaded = _load_sent_ids()
    assert loaded == ids


def test_send_a_plus_alerts_no_telegram(monkeypatch, tmp_path):
    def mock_send(msg):
        return True
    monkeypatch.setattr("modules.spcx_v2.export_telegram._send_telegram", mock_send)
    log_candidate(make_candidate("A+"))
    from modules.spcx_v2.export_telegram import send_a_plus_alerts
    n = send_a_plus_alerts()
    assert n == 1


def test_send_a_plus_alerts_no_duplicates(monkeypatch, tmp_path):
    def mock_send(msg):
        return True
    monkeypatch.setattr("modules.spcx_v2.export_telegram._send_telegram", mock_send)
    log_candidate(make_candidate("A+"))
    from modules.spcx_v2.export_telegram import send_a_plus_alerts
    n1 = send_a_plus_alerts()
    n2 = send_a_plus_alerts()
    assert n1 == 1
    assert n2 == 0


def test_send_eod_summary_no_telegram(monkeypatch, tmp_path):
    def mock_send(msg):
        return msg
    monkeypatch.setattr("modules.spcx_v2.export_telegram._send_telegram", mock_send)
    log_candidate(make_candidate("A"))
    from modules.spcx_v2.export_telegram import send_eod_summary
    msg = send_eod_summary()
    assert "SPCX V2" in msg
    assert "EOD Summary" in msg


# ── Sheets Export ────────────────────────────────────────────────────
def test_candidate_to_row():
    c = make_candidate("A")
    row = _candidate_to_row(c)
    assert row["symbol"] == "SPCX"
    assert row["setup_type"] == "IPO_ORB_15M"
    assert row["grade"] == "A"
    assert row["status"] == "paper_only"
    assert row["trade_ready"] == 78


def test_build_export_rows(tmp_path):
    log_candidate(make_candidate("A"))
    log_candidate(make_candidate("A+", "VWAP_RECLAIM"))
    log_candidate(make_candidate("B"))
    rows = build_export_rows()
    assert len(rows) == 2


def test_export_to_jsonl(tmp_path):
    log_candidate(make_candidate("A"))
    path = export_to_jsonl()
    assert path.exists()
    with open(path) as f:
        lines = f.readlines()
    assert len(lines) == 1


def test_export_to_csv(tmp_path):
    log_candidate(make_candidate("A"))
    path = export_to_csv()
    assert path.exists()
    with open(path) as f:
        lines = f.readlines()
    assert len(lines) == 2


# ── Daily Summary ────────────────────────────────────────────────────
def test_generate_daily_summary(tmp_path):
    log_candidate(make_candidate("A"))
    log_candidate(make_candidate("A+"))
    log_candidate(make_candidate("B"))
    log_candidate(make_candidate("reject"))
    log_reject(make_candidate("reject"))
    data = generate_daily_summary("20260612")
    assert data["date"] == "20260612"
    assert data["totals"]["candidates"] == 4
    assert data["totals"]["rejects"] == 1
    assert data["by_grade"]["A+"] == 1
    assert data["by_grade"]["A"] == 1
    assert data["by_grade"]["B"] == 1


def test_write_daily_markdown(tmp_path):
    log_candidate(make_candidate("A"))
    p = write_daily_markdown("20260612")
    assert p.exists()
    content = p.read_text()
    assert "SPCX V2" in content
    assert "20260612" in content
    assert "Paper-only" in content
