from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .config import VisionConfig

def _save_fig(path: Path, title: str, x: np.ndarray, y: np.ndarray, xlabel: str, ylabel: str, w: int, h: int) -> None:
    dpi = 100
    fig = plt.figure(figsize=(w/dpi, h/dpi), dpi=dpi)
    ax = fig.add_subplot(111)
    ax.plot(x, y)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)

def generate_placeholder_charts(out_dir: Path, cfg: VisionConfig) -> Dict[str, Path]:
    # Step 1: placeholders only (no external data). We’ll wire sources in Step 2+.
    x = np.arange(0, 100)
    rng = np.random.default_rng(42)

    paths: Dict[str, Path] = {}
    charts = [
        ("01_btc_flows.png", "BTC On-chain Flows (placeholder)", rng.normal(0, 1, size=100).cumsum(), "t", "flow"),
        ("02_etf_flows.png", "ETF Net Flows (placeholder)", rng.normal(0, 1, size=100).cumsum(), "t", "usd"),
        ("03_futures_volume.png", "Futures Volume (placeholder)", np.abs(rng.normal(0, 1, size=100)).cumsum(), "t", "usd"),
        ("04_liquidations.png", "Liquidations / Heatmap proxy (placeholder)", np.abs(rng.normal(0, 1, size=100)).cumsum(), "t", "liq"),
    ]
    for fname, title, y, xl, yl in charts:
        p = out_dir / fname
        _save_fig(p, title, x, y, xl, yl, cfg.chart_w, cfg.chart_h)
        paths[fname] = p
    return paths
