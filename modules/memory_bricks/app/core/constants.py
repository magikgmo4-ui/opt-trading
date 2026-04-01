from __future__ import annotations

from pathlib import Path

DEFAULT_TIMEZONE = "America/Montreal"
DEFAULT_PROJECT = "opt-trading"
DEFAULT_MODULE = "memory_bricks"
MODULE_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_STATE_ROOT = REPO_ROOT / "_state" / "memory_bricks"

ALLOWED_STATUSES = {"draft", "open", "mentioned", "resumed", "blocked", "closed"}
ALLOWED_TYPES = {"session", "decision", "resume_point", "closeout", "issue", "reference", "handoff"}
ALLOWED_HANDOFF_TARGETS = {"chatgpt", "claude", "generic"}
ALLOWED_IAS = {"chatgpt", "claude", "trae", "generic"}
