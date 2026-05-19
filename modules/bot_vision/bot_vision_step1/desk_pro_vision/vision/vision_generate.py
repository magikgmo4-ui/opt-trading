from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

from .charts import generate_placeholder_charts
from .config import VisionConfig
from .log import JsonlLogger
from .mosaic import build_mosaic_2x2
from .pack import ensure_run_dirs, make_run_id, update_latest_symlink

def write_summary(path: Path, run_id: str, chart_rel_paths: List[str], log_rel: str) -> None:
    summary = {
        "run_id": run_id,
        "ts": __import__("datetime").datetime.now().astimezone().isoformat(),
        "signals": {
            "btc_netflow_bias": "PLACEHOLDER",
            "etf_bias": "PLACEHOLDER",
            "futures_bias": "PLACEHOLDER",
            "liq_bias": "PLACEHOLDER",
        },
        "metrics": {},
        "files": {
            "charts": chart_rel_paths,
            "mosaic": "charts/mosaic_2x2.png",
            "log": log_rel,
        },
    }
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main() -> int:
    ap = argparse.ArgumentParser(description="Desk Pro Bot Vision generator (Step 1 skeleton)")
    ap.add_argument("--root", default="/opt/trading/data/desk_pro/vision", help="Vision root dir")
    ap.add_argument("--run-id", default="", help="Optional run id (defaults to timestamp)")
    ap.add_argument("--mode", default="placeholder", choices=["placeholder"], help="Data mode (Step 1 only placeholder)")
    args = ap.parse_args()

    cfg = VisionConfig()
    # override root
    paths = cfg.paths.__class__(root=Path(args.root))  # VisionPaths
    cfg = VisionConfig(paths=paths)

    run_id = args.run_id.strip() or make_run_id()
    rp = ensure_run_dirs(cfg.paths, run_id)

    logger = JsonlLogger(rp.log_path)
    logger.write("INFO", "start", True, run_id=run_id, root=str(cfg.paths.root))

    try:
        chart_map = generate_placeholder_charts(rp.charts_dir, cfg)
        logger.write("INFO", "charts_generated", True, charts=[p.name for p in chart_map.values()])

        ordered = ["01_btc_flows.png", "02_etf_flows.png", "03_futures_volume.png", "04_liquidations.png"]
        img_paths = [chart_map[name] for name in ordered]
        build_mosaic_2x2(img_paths, rp.mosaic_path)
        logger.write("INFO", "mosaic_built", True, out=str(rp.mosaic_path))

        # summary references relative to run_dir
        rels = [f"charts/{name}" for name in ordered]
        write_summary(rp.summary_path, run_id, rels, "vision.log.jsonl")
        logger.write("INFO", "summary_written", True, path=str(rp.summary_path))

        update_latest_symlink(cfg.paths, rp.run_dir)
        logger.write("INFO", "latest_updated", True, latest=str(cfg.paths.latest))

        logger.write("INFO", "done", True)
        return 0
    except Exception as e:
        logger.write("ERROR", "failed", False, error=str(e))
        raise

if __name__ == "__main__":
    raise SystemExit(main())
