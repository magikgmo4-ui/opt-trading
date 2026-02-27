from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class VisionPaths:
    root: Path = Path("/opt/trading/data/desk_pro/vision")
    runs: Path = root / "runs"
    latest: Path = root / "latest"

@dataclass(frozen=True)
class VisionConfig:
    # chart output sizes
    chart_w: int = 900
    chart_h: int = 550
    mosaic_w: int = 1800
    mosaic_h: int = 1100

    # default run retention (future step)
    keep_last_n: int = 100

    paths: VisionPaths = VisionPaths()
