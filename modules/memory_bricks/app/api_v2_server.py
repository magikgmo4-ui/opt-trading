from __future__ import annotations

import sys
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[1]
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from app.core.paths import get_state_root, get_bricks_dir, get_index_dir, get_sequence_path
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="memory_bricks API V2",
    description="Read-only API for memory_bricks module",
    version="0.1.0-readonly",
)


@app.get("/health")
def health():
    """Sanity check: API is alive."""
    return {"status": "ok", "module": "memory_bricks", "version": "0.1.0-readonly"}


@app.get("/status")
def status():
    """
    Return the state of the memory_bricks source.
    Mirrors V1 query status output.
    """
    root = get_state_root()
    bricks_dir = get_bricks_dir()
    index_dir = get_index_dir()
    brick_count = 0
    if bricks_dir.exists():
        brick_count = len(list(bricks_dir.glob("MB-*.md")))

    payload = {
        "root": str(root),
        "root_exists": root.exists(),
        "bricks_dir": bricks_dir.exists(),
        "bricks": brick_count,
        "index_full": (index_dir / "index_full.json").exists(),
        "index_short": (index_dir / "index_short.md").exists(),
        "sequence": get_sequence_path().exists(),
    }

    if not root.exists():
        return JSONResponse(status_code=404, content=payload)

    return payload


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8112)


if __name__ == "__main__":
    main()
