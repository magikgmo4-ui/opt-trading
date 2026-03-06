"""
Position Storage
Handles JSON persistence for trading positions.
"""
import json
import os
import pathlib
from typing import Dict, Any

STATE_DIR = pathlib.Path("state")
POSITIONS_FILE = STATE_DIR / "positions.json"

def ensure_state_dir():
    STATE_DIR.mkdir(parents=True, exist_ok=True)

def load_positions() -> Dict[str, Any]:
    """
    Load positions from JSON file.
    """
    ensure_state_dir()
    if not POSITIONS_FILE.exists():
        return {}
    
    try:
        return json.loads(POSITIONS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def save_positions(positions: Dict[str, Any]) -> None:
    """
    Save positions to JSON file.
    """
    ensure_state_dir()
    # Convert Position objects to dict if needed, or assume caller passes dicts
    # For simplicity, we expect the caller to pass serializable data or we handle serialization here
    
    # If positions is Dict[str, Position], we need to serialize
    serializable = {}
    for k, v in positions.items():
        if hasattr(v, "__dict__"):
            # Convert Position object to dict, handling datetime
            d = v.__dict__.copy()
            if "opened_at" in d and hasattr(d["opened_at"], "isoformat"):
                d["opened_at"] = d["opened_at"].isoformat()
            serializable[k] = d
        else:
            serializable[k] = v
            
    POSITIONS_FILE.write_text(json.dumps(serializable, indent=2), encoding="utf-8")
