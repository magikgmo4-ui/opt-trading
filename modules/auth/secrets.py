from __future__ import annotations
import os
from typing import Optional

def get_secret(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Read secret from environment variables.
    """
    v = os.environ.get(name)
    if v is None or v == "":
        return default
    return v

def require_secret(name: str) -> str:
    """
    Like get_secret but raises if missing.
    """
    v = get_secret(name)
    if v is None:
        raise RuntimeError(f"Missing required secret env var: {name}")
    return v
