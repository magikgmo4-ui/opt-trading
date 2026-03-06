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
