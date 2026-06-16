"""
setup_edge_scorer.py — Lab backtest edge scorer.

Reads candidate setups from inbox and scores historical edge.
In production: replays setup against OHLCV history.
Currently: provides structural scoring with simulated baselines.

Produces:
  outputs/lab_backtest/results/setup_edge_scores.jsonl

Usage:
    python -m modules.analysis_bundles.lab_backtest.setup_edge_scorer

Invariants:
  - Monitor-only — no execution, no broker, no order
  - Does NOT create setups — only scores existing ones
  - Insufficient sample → no boost, no penalty
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_INBOX = _PROJECT_ROOT / "outputs" / "lab_backtest" / "inbox"
_RESULTS = _PROJECT_ROOT / "outputs" / "lab_backtest" / "results"

# Simulated baseline data per setup_type × asset_class
# In production: replaced by real OHLCV replay
_SIMULATED_EDGES = {
    ("vwap_rejection", "crypto_perp"):   {"sample_size": 45, "win_rate": 0.55, "avg_r": 1.28, "profit_factor": 1.42},
    ("vwap_reclaim", "crypto_perp"):     {"sample_size": 52, "win_rate": 0.58, "avg_r": 1.35, "profit_factor": 1.55},
    ("orb_break_long", "crypto_perp"):   {"sample_size": 38, "win_rate": 0.62, "avg_r": 1.45, "profit_factor": 1.72},
    ("orb_break_short", "crypto_perp"):  {"sample_size": 38, "win_rate": 0.60, "avg_r": 1.40, "profit_factor": 1.65},
    ("structure_break_long", "crypto_perp"):  {"sample_size": 30, "win_rate": 0.52, "avg_r": 1.20, "profit_factor": 1.25},
    ("structure_break_short", "crypto_perp"): {"sample_size": 30, "win_rate": 0.54, "avg_r": 1.22, "profit_factor": 1.30},
    ("liquidity_sweep_long", "crypto_perp"):  {"sample_size": 22, "win_rate": 0.65, "avg_r": 1.60, "profit_factor": 1.90},
    ("liquidity_sweep_short", "crypto_perp"): {"sample_size": 22, "win_rate": 0.63, "avg_r": 1.55, "profit_factor": 1.80},
    ("vwap_reclaim", "ipo"):             {"sample_size": 18, "win_rate": 0.60, "avg_r": 1.50, "profit_factor": 1.70},
    ("vwap_rejection", "ipo"):           {"sample_size": 14, "win_rate": 0.50, "avg_r": 1.10, "profit_factor": 1.10},
    ("support_watch", "crypto_perp"):    {"sample_size": 80, "win_rate": 0.35, "avg_r": 0.70, "profit_factor": 0.65},
    ("support_watch", "forex_cfd"):      {"sample_size": 40, "win_rate": 0.38, "avg_r": 0.80, "profit_factor": 0.75},
    ("support_watch", "ipo"):            {"sample_size": 12, "win_rate": 0.45, "avg_r": 0.90, "profit_factor": 0.85},
}


def _score_edge(sample: dict) -> dict:
    """Score historical edge from sample data. Returns edge_score 0-100."""
    n = sample.get("sample_size", 0)
    wr = sample.get("win_rate", 0)
    avg_r = sample.get("avg_r", 0)
    pf = sample.get("profit_factor", 1.0)

    # Minimum sample threshold
    if n < 20:
        return {
            "sample_size": n,
            "win_rate": wr,
            "avg_r": avg_r,
            "profit_factor": pf,
            "max_drawdown_r": -3.0,
            "mfe_median_r": avg_r * 0.6 if avg_r > 0 else 0,
            "mae_median_r": -0.3,
            "edge_score": 0,
            "edge_confidence": 0.3,
            "recommendation": "insufficient_sample",
            "warnings": [f"Sample too small ({n} < 20) — no boost applied"],
        }

    # Score components
    wr_score = min(40, int(wr * 65))
    avg_r_score = min(30, int(max(0, avg_r - 0.5) * 20))
    pf_score = min(20, int(max(0, pf - 0.8) * 15))
    sample_bonus = min(10, n // 15)

    edge = wr_score + avg_r_score + pf_score + sample_bonus
    edge = max(0, min(100, edge))

    # Confidence
    conf = min(0.95, 0.4 + n / 200)

    # Recommendation
    if edge >= 65:
        rec = "supportive"
    elif edge >= 45:
        rec = "neutral"
    else:
        rec = "negative"

    warnings = []
    if pf < 1.1:
        warnings.append("Low profit factor — edge may not cover costs")
    if n < 50:
        warnings.append(f"Moderate sample ({n}) — edge confidence reduced")

    return {
        "sample_size": n,
        "win_rate": wr,
        "avg_r": avg_r,
        "profit_factor": pf,
        "max_drawdown_r": -3.0,
        "mfe_median_r": avg_r * 0.6 if avg_r > 0 else 0,
        "mae_median_r": -0.35,
        "edge_score": edge,
        "edge_confidence": round(conf, 2),
        "recommendation": rec,
        "warnings": warnings,
    }


def score_candidates() -> dict:
    """Read inbox candidates and produce edge scores."""
    now = datetime.now(timezone.utc).isoformat()
    _RESULTS.mkdir(parents=True, exist_ok=True)
    inbox_path = _INBOX / "setup_candidates.jsonl"
    out_path = _RESULTS / "setup_edge_scores.jsonl"

    if not inbox_path.exists():
        return {"error": "No candidates in inbox", "scored": 0}

    scored = 0
    with open(inbox_path, encoding="utf-8") as fh_in, open(out_path, "w", encoding="utf-8") as fh_out:
        for line in fh_in:
            line = line.strip()
            if not line:
                continue
            try:
                candidate = json.loads(line)
            except json.JSONDecodeError:
                continue

            setup_type = candidate.get("setup_type", "")
            asset_class = candidate.get("asset_class", "crypto_perp")
            sample = _SIMULATED_EDGES.get((setup_type, asset_class),
                                          _SIMULATED_EDGES.get((setup_type, "crypto_perp"),
                                           {"sample_size": 0, "win_rate": 0, "avg_r": 0, "profit_factor": 0}))

            edge = _score_edge(sample)
            edge["setup_id"] = candidate.get("setup_id", "?")
            edge["symbol"] = candidate.get("symbol", "?")
            edge["setup_type"] = setup_type
            edge["scored_at"] = now
            edge["monitor_only"] = True

            fh_out.write(json.dumps(edge, default=str) + "\n")
            scored += 1

    return {"scored": scored, "path": str(out_path), "as_of": now}


if __name__ == "__main__":
    import sys
    result = score_candidates()
    if "error" in result:
        print("ERROR:", result["error"], file=sys.stderr)
        sys.exit(1)
    print(f"Scored {result['scored']} candidates → {result['path']}")
