from __future__ import annotations
from .ipo_dataset import compute_analog_match as _dataset_match


def compute_analog_score(spcx_metrics: dict) -> dict:
    return _dataset_match(
        spcx_gap_pct=spcx_metrics.get("gap_pct", 0) or 0,
        spcx_rel_vol=spcx_metrics.get("relative_volume", 1) or 1,
        spcx_fvg=spcx_metrics.get("fvg_bullish", False),
        spcx_bos=spcx_metrics.get("bos", False),
    )
