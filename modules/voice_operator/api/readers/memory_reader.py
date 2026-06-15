"""
Memory Reader — placeholder for future Memory Bricks integration
GO_DESKPRO_VOICE_OPERATOR_01 — Lot B

Memory Bricks serves as knowledge base for the voice operator.
Currently returns placeholder — to be wired when memory_bricks API is available.
"""
from __future__ import annotations
from typing import Any


def read_bricks(query: str = "", limit: int = 10) -> dict:
    """Placeholder for memory bricks query."""
    return {
        "ok": False,
        "source": "memory_bricks",
        "status": "not_yet_integrated",
        "note": "Memory Bricks integration deferred to Lot C/D",
        "bricks": [],
    }


def read_status() -> dict:
    """Placeholder for memory bricks status."""
    return {
        "ok": False,
        "source": "memory_bricks",
        "status": "not_yet_integrated",
    }
