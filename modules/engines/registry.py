"""
Engine Registry
Central registry for all available trading engines.
"""
from typing import Dict, Any, Callable

# Simple registry: Name -> Handler Function
# Handler signature: (engine: str, payload: dict) -> dict
_ENGINES: Dict[str, Callable[[str, Dict[str, Any]], Dict[str, Any]]] = {}

def register_engine(name: str, handler: Callable):
    """
    Register a new engine handler.
    """
    if not name:
        return
    _ENGINES[name] = handler

def get_engine(name: str) -> Callable | None:
    """
    Retrieve an engine handler by name.
    """
    return _ENGINES.get(name)

def list_engines() -> list[str]:
    """
    List all registered engine names.
    """
    return sorted(list(_ENGINES.keys()))

# --- Built-in / Dummy Engines ---

def _echo_engine(engine: str, payload: dict) -> dict:
    """
    Minimal dummy engine for validation.
    Returns the payload as-is with a status.
    """
    return {
        "ok": True,
        "engine": engine,
        "processed_by": "echo_engine",
        "original_payload": payload
    }

# Register default dummy engine
register_engine("ECHO_TEST", _echo_engine)

def _noop_engine(engine: str, payload: dict) -> dict:
    """
    Standard No-Op handler for legacy engines.
    The server handles Risk/Perf/Log; the engine logic is implicit or upstream.
    """
    return {"ok": True, "engine": engine, "status": "noop"}

# Legacy / Production Engines
# These are the hardcoded engines from webhook_server.py
register_engine("COINM_SHORT", _noop_engine)
register_engine("USDTM_LONG", _noop_engine)
register_engine("GOLD_CFD_LONG", _noop_engine)
register_engine("TV_TEST", _noop_engine)
register_engine("NGROK_TEST", _noop_engine)
register_engine("PAPER_TEST", _noop_engine)

