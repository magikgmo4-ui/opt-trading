"""Future FastAPI surface for memory_bricks (reserved for V2)."""

def get_api_status() -> dict:
    return {
        "module": "memory_bricks",
        "status": "reserved_v2",
        "message": "API layer intentionally not enabled in V1."
    }
