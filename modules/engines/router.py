"""
Engine Router
Dispatches incoming payloads to the appropriate registered engine.
"""
from typing import Dict, Any
from modules.engines.registry import get_engine, list_engines

def route_event(engine_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Route an event payload to the specified engine handler.
    
    Args:
        engine_name: The name of the target engine.
        payload: The full webhook payload.
        
    Returns:
        The result dictionary from the engine handler.
    """
    handler = get_engine(engine_name)
    if not handler:
        # Fallback for unknown engines: minimal acknowledgment
        # This matches current behavior of ignoring unknown engines or handling them generically
        return {
            "ok": False,
            "error": f"Engine '{engine_name}' not found",
            "available_engines": list_engines()
        }
    
    try:
        return handler(engine_name, payload)
    except Exception as e:
        return {
            "ok": False,
            "error": f"Engine execution failed: {str(e)}",
            "engine": engine_name
        }

if __name__ == "__main__":
    # Simple CLI Test
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "test":
            res = route_event("ECHO_TEST", {"msg": "hello"})
            print(res)
