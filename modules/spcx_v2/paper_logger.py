"""SPCX V2 — Paper logger: logs all candidates, accepted and rejected."""

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from modules.spcx_v2.config import (
    OUTPUT_DIR,
    CANDIDATES_FILE,
    REJECTS_FILE,
    RESULTS_FILE,
    SUMMARY_FILE,
    SetupCandidate,
)
from shared.logger import setup_logger

logger = setup_logger("spcx_v2.paper_logger")


def _ensure_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _candidate_to_dict(c: SetupCandidate) -> dict:
    return {
        "candidate_id": c.candidate_id,
        "symbol": c.symbol,
        "ts": c.ts,
        "setup_type": c.setup_type,
        "grade": c.grade,
        "status": c.status,
        "gates": c.gates,
        "scores": {
            "trade_ready": c.scores.trade_ready,
            "liquidity": c.scores.liquidity,
            "risk": c.scores.risk,
            "smart_money": c.scores.smart_money,
            "catalyst": c.scores.catalyst,
        },
        "entry_zone": c.entry_zone,
        "invalidation": c.invalidation,
        "tp_logic": c.tp_logic,
        "reason_codes": c.reason_codes,
        "entry_price": c.entry_price,
        "stop_loss": c.stop_loss,
        "tp1": c.tp1,
        "tp2": c.tp2,
        "risk_r": c.risk_r,
        "result_15m": c.result_15m,
        "result_30m": c.result_30m,
        "result_1h": c.result_1h,
        "result_eod": c.result_eod,
        "mfe": c.mfe,
        "mae": c.mae,
        "r_multiple": c.r_multiple,
        "hit_tp1": c.hit_tp1,
        "hit_tp2": c.hit_tp2,
        "hit_sl": c.hit_sl,
        "logged_at": _now_iso(),
    }


def _dict_to_candidate(d: dict) -> SetupCandidate:
    from modules.spcx_v2.config import ScoreSet

    return SetupCandidate(
        symbol=d.get("symbol", ""),
        ts=d.get("ts", ""),
        setup_type=d.get("setup_type", "NONE"),
        grade=d.get("grade", "reject"),
        status=d.get("status", "paper_only"),
        gates=d.get("gates", {}),
        scores=ScoreSet(**d.get("scores", {})),
        entry_zone=d.get("entry_zone", ""),
        invalidation=d.get("invalidation", ""),
        tp_logic=d.get("tp_logic", []),
        reason_codes=d.get("reason_codes", []),
        candidate_id=d.get("candidate_id"),
        entry_price=d.get("entry_price"),
        stop_loss=d.get("stop_loss"),
        tp1=d.get("tp1"),
        tp2=d.get("tp2"),
        risk_r=d.get("risk_r"),
        result_15m=d.get("result_15m"),
        result_30m=d.get("result_30m"),
        result_1h=d.get("result_1h"),
        result_eod=d.get("result_eod"),
        mfe=d.get("mfe"),
        mae=d.get("mae"),
        r_multiple=d.get("r_multiple"),
        hit_tp1=d.get("hit_tp1", False),
        hit_tp2=d.get("hit_tp2", False),
        hit_sl=d.get("hit_sl", False),
    )


def _append_jsonl(filepath: Path, data: dict):
    _ensure_dir()
    with open(filepath, "a") as f:
        f.write(json.dumps(data, default=str) + "\n")


def _read_jsonl(filepath: Path) -> list[dict]:
    if not filepath.exists():
        return []
    results = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError:
                logger.warning("skipping malformed JSONL line in %s", filepath)
    return results


# ── Public API ───────────────────────────────────────────────────────
def log_candidate(candidate: SetupCandidate) -> str:
    cid = candidate.candidate_id or str(uuid.uuid4())[:8]
    candidate.candidate_id = cid

    payload = _candidate_to_dict(candidate)
    filepath = OUTPUT_DIR / CANDIDATES_FILE
    _append_jsonl(filepath, payload)
    logger.info("logged candidate %s | %s | %s", cid, candidate.setup_type, candidate.grade)
    return cid


def log_reject(candidate: SetupCandidate) -> str:
    cid = candidate.candidate_id or str(uuid.uuid4())[:8]
    candidate.candidate_id = cid

    payload = _candidate_to_dict(candidate)
    filepath = OUTPUT_DIR / REJECTS_FILE
    _append_jsonl(filepath, payload)
    logger.info("logged reject %s | reasons=%s", cid, candidate.reason_codes)
    return cid


def log_result(candidate_id: str, result: dict) -> None:
    filepath = OUTPUT_DIR / RESULTS_FILE
    result_payload = {
        "candidate_id": candidate_id,
        "logged_at": _now_iso(),
        **result,
    }
    _append_jsonl(filepath, result_payload)
    logger.info("logged result for %s", candidate_id)


def list_candidates(status: Optional[str] = None) -> list[SetupCandidate]:
    filepath = OUTPUT_DIR / CANDIDATES_FILE
    rows = _read_jsonl(filepath)
    candidates = [_dict_to_candidate(r) for r in rows]
    if status:
        candidates = [c for c in candidates if c.grade == status or c.status == status]
    return candidates


def get_summary() -> dict:
    candidates = list_candidates()
    reject_file = OUTPUT_DIR / REJECTS_FILE
    rejects = _read_jsonl(reject_file)

    by_setup = {}
    for c in candidates:
        st = c.setup_type
        if st not in by_setup:
            by_setup[st] = {"count": 0, "by_grade": {}}
        by_setup[st]["count"] += 1
        g = c.grade
        by_setup[st]["by_grade"][g] = by_setup[st]["by_grade"].get(g, 0) + 1

    by_grade = {}
    for c in candidates:
        g = c.grade
        by_grade[g] = by_grade.get(g, 0) + 1

    results_file = OUTPUT_DIR / RESULTS_FILE
    results = _read_jsonl(results_file)

    r_values = [r.get("r_multiple", 0) for r in results if r.get("r_multiple") is not None]
    win_count = sum(1 for rv in r_values if rv > 0)
    total_r = len(r_values)
    winrate = (win_count / total_r * 100) if total_r > 0 else 0
    expectancy = sum(r_values) / total_r if total_r > 0 else 0
    gross_profit = sum(rv for rv in r_values if rv > 0)
    gross_loss = abs(sum(rv for rv in r_values if rv < 0))
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (float("inf") if gross_profit > 0 else 0)

    summary = {
        "total_candidates": len(candidates),
        "total_rejects": len(rejects),
        "by_setup_type": by_setup,
        "by_grade": by_grade,
        "winrate": round(winrate, 2),
        "expectancy_R": round(expectancy, 3),
        "profit_factor": round(profit_factor, 2) if profit_factor != float("inf") else None,
        "total_results": total_r,
        "generated_at": _now_iso(),
    }

    summary_path = OUTPUT_DIR / SUMMARY_FILE
    _ensure_dir()
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)

    return summary
