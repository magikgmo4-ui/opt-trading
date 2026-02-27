from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Tuple

from .config import VisionPaths

def make_run_id() -> str:
    # local time (America/Montreal equivalent offset). Later step uses zoneinfo.
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

@dataclass(frozen=True)
class RunPaths:
    run_id: str
    run_dir: Path
    charts_dir: Path
    summary_path: Path
    log_path: Path
    mosaic_path: Path

def ensure_run_dirs(paths: VisionPaths, run_id: str) -> RunPaths:
    run_dir = paths.runs / run_id
    charts_dir = run_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)
    return RunPaths(
        run_id=run_id,
        run_dir=run_dir,
        charts_dir=charts_dir,
        summary_path=run_dir / "summary.json",
        log_path=run_dir / "vision.log.jsonl",
        mosaic_path=charts_dir / "mosaic_2x2.png",
    )

def update_latest_symlink(paths: VisionPaths, run_dir: Path) -> None:
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.runs.mkdir(parents=True, exist_ok=True)

    # atomic-ish: replace symlink
    latest = paths.latest
    try:
        if latest.is_symlink() or latest.exists():
            latest.unlink()
    except Exception:
        # fallback: if it's a directory, do not delete here
        pass

    os.symlink(str(run_dir), str(latest))
