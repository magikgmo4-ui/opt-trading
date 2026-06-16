"""
Voice Operator — Executive Reader (PR8).

Reads executive intelligence from DeskPro executive_reader bridge.
No business logic. No recalculation. Pure pass-through.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def _read_executive() -> Optional[Dict[str, Any]]:
    try:
        from modules.desk_pro.service.executive_reader import get_executive
        return get_executive()
    except Exception:
        return None


def _read_regime() -> Optional[Dict[str, Any]]:
    try:
        from modules.desk_pro.service.executive_reader import get_executive_regime
        return get_executive_regime()
    except Exception:
        return None


def _read_leaders() -> Optional[Dict[str, Any]]:
    try:
        from modules.desk_pro.service.executive_reader import get_executive_leaders
        return get_executive_leaders()
    except Exception:
        return None


def _read_risks() -> Optional[Dict[str, Any]]:
    try:
        from modules.desk_pro.service.executive_reader import get_executive_risks
        return get_executive_risks()
    except Exception:
        return None


def read_executive_briefing() -> Optional[Dict[str, Any]]:
    return _read_executive()


def read_executive_regime() -> Optional[Dict[str, Any]]:
    return _read_regime()


def read_executive_leaders() -> Optional[Dict[str, Any]]:
    return _read_leaders()


def read_executive_risks() -> Optional[Dict[str, Any]]:
    return _read_risks()
