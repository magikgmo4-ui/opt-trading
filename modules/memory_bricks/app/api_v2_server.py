from __future__ import annotations

import json
import os
import sys
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[1]
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

DEFAULT_STATE_ROOT = MODULE_DIR.parents[1] / "_state" / "memory_bricks"


def get_state_root() -> Path:
    return Path(os.environ.get("MEMORY_BRICKS_STATE_ROOT", str(DEFAULT_STATE_ROOT))).expanduser()


def get_bricks_dir() -> Path:
    return get_state_root() / "bricks"


def get_index_dir() -> Path:
    return get_state_root() / "index"


def get_meta_dir() -> Path:
    return get_state_root() / "meta"


def get_sequence_path() -> Path:
    return get_meta_dir() / "sequence.json"

app = FastAPI(
    title="memory_bricks API V2",
    description="Read-only API for memory_bricks module",
    version="0.1.0-readonly",
)

BRICK_LIST_FIELDS = (
    "id",
    "title",
    "date",
    "type",
    "status",
    "ia",
    "machine",
    "surface",
    "project",
    "module",
    "summary_short",
    "tags",
)


def _load_index_rows() -> list[dict[str, object]]:
    index_path = get_index_dir() / "index_full.json"
    if not index_path.exists():
        raise FileNotFoundError(index_path)

    rows = json.loads(index_path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("index_full.json must contain a JSON array")
    return [row for row in rows if isinstance(row, dict)]


def _matches_filter(row: dict[str, object], key: str, value: str | None) -> bool:
    if not value:
        return True
    row_value = row.get(key)
    return isinstance(row_value, str) and row_value == value


def _matches_tag(row: dict[str, object], tag: str | None) -> bool:
    if not tag:
        return True
    tags = row.get("tags")
    return isinstance(tags, list) and tag in tags


def _to_brick_list_item(row: dict[str, object]) -> dict[str, object]:
    item: dict[str, object] = {}
    for field in BRICK_LIST_FIELDS:
        value = row.get(field)
        if value is None and field == "tags":
            value = []
        item[field] = value
    return item


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


@app.get("/bricks")
def list_bricks(
    status: str | None = None,
    brick_type: str | None = Query(default=None, alias="type"),
    project: str | None = None,
    module: str | None = None,
    machine: str | None = None,
    ia: str | None = None,
    surface: str | None = None,
    tag: str | None = None,
    limit: int = Query(default=50, ge=0),
    offset: int = Query(default=0, ge=0),
):
    try:
        rows = _load_index_rows()
    except FileNotFoundError:
        payload = {
            "items": [],
            "total": 0,
            "limit": limit,
            "offset": offset,
            "error": "index_full.json not found",
        }
        return JSONResponse(status_code=404, content=payload)

    filtered = []
    for row in rows:
        if not _matches_filter(row, "status", status):
            continue
        if not _matches_filter(row, "type", brick_type):
            continue
        if not _matches_filter(row, "project", project):
            continue
        if not _matches_filter(row, "module", module):
            continue
        if not _matches_filter(row, "machine", machine):
            continue
        if not _matches_filter(row, "ia", ia):
            continue
        if not _matches_filter(row, "surface", surface):
            continue
        if not _matches_tag(row, tag):
            continue
        filtered.append(_to_brick_list_item(row))

    total = len(filtered)
    items = filtered[offset : offset + limit]
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8112)


if __name__ == "__main__":
    main()
