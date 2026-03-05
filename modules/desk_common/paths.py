from __future__ import annotations
from pathlib import Path

REPO_ROOT = Path("/opt/trading")

DESK_DIR = REPO_ROOT / "desk"
SNAPSHOT_DIR = DESK_DIR / "snapshots"
SNAPSHOT_LATEST_JSON = SNAPSHOT_DIR / "latest.json"
SNAPSHOT_HISTORY_JSONL = SNAPSHOT_DIR / "history.jsonl"

INPUTS_DIR = DESK_DIR / "inputs"
TV_INPUTS_LATEST_JSON = INPUTS_DIR / "tv_inputs_latest.json"
TV_INPUTS_HISTORY_JSONL = INPUTS_DIR / "tv_inputs_history.jsonl"
