"""Tests for SPCX V2 paper logger — log, reject, summary, retrieval."""

import json
import tempfile
import os
from pathlib import Path

import pytest
from modules.spcx_v2.config import OUTPUT_DIR, SetupCandidate, ScoreSet
from modules.spcx_v2.paper_logger import (
    log_candidate,
    log_reject,
    log_result,
    list_candidates,
    get_summary,
    _candidate_to_dict,
    _dict_to_candidate,
)


@pytest.fixture(autouse=True)
def temp_output_dir(monkeypatch, tmp_path):
    monkeypatch.setattr("modules.spcx_v2.paper_logger.OUTPUT_DIR", tmp_path)
    return tmp_path


def make_candidate(grade="A", setup_type="IPO_ORB_15M", reason_codes=None):
    return SetupCandidate(
        symbol="SPCX",
        ts="2026-06-12T14:30:00Z",
        setup_type=setup_type,
        grade=grade,
        status="paper_only",
        scores=ScoreSet(trade_ready=78, liquidity=72, risk=38, smart_money=70, catalyst=65),
        reason_codes=reason_codes or ["ORB_BREAK", "VWAP_ALIGNED"],
    )


def test_log_candidate(tmp_path):
    c = make_candidate()
    cid = log_candidate(c)
    assert cid is not None
    assert len(cid) == 8

    cand_file = tmp_path / "candidates.jsonl"
    assert cand_file.exists()
    with open(cand_file) as f:
        data = json.loads(f.readline())
    assert data["candidate_id"] == cid
    assert data["symbol"] == "SPCX"
    assert data["grade"] == "A"


def test_log_reject(tmp_path):
    c = make_candidate(grade="reject", reason_codes=["PRICE_NOT_LIVE"])
    cid = log_reject(c)

    rej_file = tmp_path / "rejects.jsonl"
    assert rej_file.exists()
    with open(rej_file) as f:
        data = json.loads(f.readline())
    assert data["grade"] == "reject"
    assert "PRICE_NOT_LIVE" in data["reason_codes"]


def test_log_result(tmp_path):
    c = make_candidate()
    cid = log_candidate(c)
    log_result(cid, {"mfe": 0.02, "mae": 0.01, "r_multiple": 1.5, "hit_tp1": True})

    res_file = tmp_path / "results.jsonl"
    assert res_file.exists()
    with open(res_file) as f:
        data = json.loads(f.readline())
    assert data["candidate_id"] == cid
    assert data["r_multiple"] == 1.5
    assert data["hit_tp1"] is True


def test_list_candidates(tmp_path):
    log_candidate(make_candidate(grade="A", setup_type="IPO_ORB_15M"))
    log_candidate(make_candidate(grade="B", setup_type="VWAP_HOLD_LONG"))
    log_candidate(make_candidate(grade="reject", setup_type="NONE"))

    all_candidates = list_candidates()
    assert len(all_candidates) == 3

    a_only = list_candidates(status="A")
    assert len(a_only) == 1


def test_get_summary(tmp_path):
    log_candidate(make_candidate(grade="A", setup_type="IPO_ORB_15M"))
    log_candidate(make_candidate(grade="A", setup_type="IPO_ORB_15M"))
    log_candidate(make_candidate(grade="B", setup_type="VWAP_HOLD_LONG"))
    log_reject(make_candidate(grade="reject", reason_codes=["PRICE_NOT_LIVE"]))

    log_result(list_candidates()[0].candidate_id, {"r_multiple": 1.5})
    log_result(list_candidates()[1].candidate_id, {"r_multiple": -0.5})

    summary = get_summary()
    assert summary["total_candidates"] == 3
    assert summary["total_rejects"] == 1
    assert summary["by_grade"]["A"] == 2
    assert summary["by_setup_type"]["IPO_ORB_15M"]["count"] == 2
    assert summary["total_results"] == 2
    assert summary["expectancy_R"] == 0.5


def test_roundtrip_serialization():
    c = make_candidate()
    d = _candidate_to_dict(c)
    restored = _dict_to_candidate(d)
    assert restored.symbol == c.symbol
    assert restored.setup_type == c.setup_type
    assert restored.grade == c.grade
    assert restored.scores.trade_ready == c.scores.trade_ready
