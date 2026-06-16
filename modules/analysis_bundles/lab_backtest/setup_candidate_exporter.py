"""
multitf_lab_exporter.py — export multi-TF setups to Lab backtest inbox.

Reads multitf_setup_score.v1 views and writes candidate setups
for historical backtesting / edge scoring.

Produces:
  outputs/lab_backtest/inbox/setup_candidates.jsonl

Usage:
    python -m modules.analysis_bundles.lab_backtest.setup_candidate_exporter

Invariants:
  - Monitor-only — no execution, no broker, no order
  - Export only — does not modify source views
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_VIEWS_DIR = _PROJECT_ROOT / "data" / "data_center" / "views"
_SCORE_DIR = _VIEWS_DIR / "multitf_setup_score.v1" / "by_symbol"
_INBOX = _PROJECT_ROOT / "outputs" / "lab_backtest" / "inbox"


def _load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def export_setup_candidates() -> dict:
    """Read multitf_setup_score.v1 and write candidates to inbox."""
    now = datetime.now(timezone.utc).isoformat()
    _INBOX.mkdir(parents=True, exist_ok=True)
    out_path = _INBOX / "setup_candidates.jsonl"
    exported = 0

    if not _SCORE_DIR.exists():
        return {"error": "multitf_setup_score.v1 views not found", "exported": 0}

    with open(out_path, "w", encoding="utf-8") as fh:
        for score_file in sorted(_SCORE_DIR.glob("*.json")):
            data = _load_json(score_file)
            if not isinstance(data, dict):
                continue

            sym = data.get("symbol", "?")
            bias = data.get("bias", {})
            setups = data.get("setups", [])
            sq = data.get("source_quality", {})

            for st in setups:
                candidate = {
                    "setup_id": f"{st.get('setup_id','?')}_{now[:10]}",
                    "symbol": sym,
                    "asset_class": "crypto_perp",  # inferred, may refine later
                    "setup_type": st.get("setup_type", ""),
                    "direction": st.get("direction", "monitor_only"),
                    "timestamp": now,
                    "timeframe_trigger": "M15",
                    "price": None,
                    "bias": {
                        "htf": bias.get("htf", "neutral"),
                        "ltf": bias.get("ltf", "neutral"),
                        "alignment": bias.get("alignment", "neutral"),
                    },
                    "trigger": {
                        "event": "",
                        "source": "multitf_setup_score",
                        "age_minutes": st.get("trigger_age_minutes"),
                        "trigger_quality_score": st.get("trigger_quality_score", 0),
                    },
                    "score_before_backtest": st.get("score", 0),
                    "grade_before_backtest": st.get("grade", "C"),
                    "probability_before_backtest": st.get("probability_pct", 50),
                    "confidence_before_backtest": st.get("confidence_pct", 50),
                    "core_evidence": st.get("core_evidence", []),
                    "enrichment_evidence": st.get("enrichment_evidence", []),
                    "downgrade_reasons": st.get("downgrade_reasons", []),
                    "missing": st.get("missing", []),
                    "monitor_only": True,
                }
                # Add price from entry_zone
                ez = st.get("entry_zone", [])
                if ez:
                    candidate["price"] = (ez[0] + ez[-1]) / 2 if len(ez) >= 2 else ez[0]
                # Extract trigger event from core_evidence
                for ev in candidate["core_evidence"]:
                    if "CDP " in ev:
                        candidate["trigger"]["event"] = ev
                        break

                fh.write(json.dumps(candidate, default=str) + "\n")
                exported += 1

    return {"exported": exported, "path": str(out_path), "as_of": now}


if __name__ == "__main__":
    import sys
    # Phase 0: run exporter standalone
    result = export_setup_candidates()
    if "error" in result:
        print("ERROR:", result["error"], file=sys.stderr)
        sys.exit(1)
    print(f"Exported {result['exported']} candidates to {result['path']}")
