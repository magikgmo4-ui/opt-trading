"""SPCX V2 — Desk Pro export: JSON endpoints for the dashboard."""

import json
from pathlib import Path
from typing import Optional

from modules.spcx_v2.paper_logger import list_candidates, get_summary, _read_jsonl
from modules.spcx_v2.config import OUTPUT_DIR


def get_desk_status() -> dict:
    summary = get_summary()
    recent = list_candidates()[-10:] if list_candidates() else []

    return {
        "status": "paper_only",
        "generated_at": summary.get("generated_at", ""),
        "totals": {
            "candidates": summary.get("total_candidates", 0),
            "rejects": summary.get("total_rejects", 0),
        },
        "by_grade": summary.get("by_grade", {}),
        "by_setup_type": summary.get("by_setup_type", {}),
        "winrate": summary.get("winrate", 0),
        "expectancy_R": summary.get("expectancy_R", 0),
        "profit_factor": summary.get("profit_factor"),
        "recent_candidates": [
            {
                "id": c.candidate_id,
                "ts": c.ts,
                "setup_type": c.setup_type,
                "grade": c.grade,
                "scores": {
                    "trade_ready": c.scores.trade_ready,
                    "liquidity": c.scores.liquidity,
                    "risk": c.scores.risk,
                    "smart_money": c.scores.smart_money,
                    "catalyst": c.scores.catalyst,
                },
            }
            for c in recent
        ],
    }


def get_desk_candidates(limit: int = 20, grade: Optional[str] = None) -> list[dict]:
    candidates = list_candidates()
    if grade:
        candidates = [c for c in candidates if c.grade == grade]

    candidates = candidates[-limit:]

    return [
        {
            "candidate_id": c.candidate_id,
            "ts": c.ts,
            "setup_type": c.setup_type,
            "grade": c.grade,
            "entry_zone": c.entry_zone,
            "invalidation": c.invalidation,
            "scores": {
                "trade_ready": c.scores.trade_ready,
                "liquidity": c.scores.liquidity,
                "risk": c.scores.risk,
                "smart_money": c.scores.smart_money,
                "catalyst": c.scores.catalyst,
            },
            "reason_codes": c.reason_codes,
            "hit_tp1": c.hit_tp1,
            "hit_tp2": c.hit_tp2,
            "hit_sl": c.hit_sl,
            "r_multiple": c.r_multiple,
        }
        for c in candidates
    ]


def get_desk_stats() -> dict:
    summary = get_summary()
    return {
        "winrate": summary.get("winrate", 0),
        "expectancy_R": summary.get("expectancy_R", 0),
        "profit_factor": summary.get("profit_factor"),
        "total_results": summary.get("total_results", 0),
        "by_grade": summary.get("by_grade", {}),
        "by_setup_type": summary.get("by_setup_type", {}),
        "generated_at": summary.get("generated_at", ""),
    }


def export_desk_json(path: Optional[str] = None) -> Path:
    status = get_desk_status()
    if path:
        out = Path(path)
    else:
        out = OUTPUT_DIR / "desk_status.json"

    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(status, f, indent=2, default=str)
    return out
