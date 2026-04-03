from __future__ import annotations

import ast
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

BRICK_DETAIL_FIELDS = (
    "id",
    "title",
    "type",
    "status",
    "ia",
    "machine",
    "surface",
    "project",
    "module",
    "date",
    "summary_short",
    "resume_point",
    "tags",
    "links",
    "decisions",
    "todo",
)


def _load_index_rows() -> list[dict[str, object]]:
    index_path = get_index_dir() / "index_full.json"
    if not index_path.exists():
        raise FileNotFoundError(index_path)

    rows = json.loads(index_path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("index_full.json must contain a JSON array")
    return [row for row in rows if isinstance(row, dict)]


def _parse_scalar(value: str) -> object:
    value = value.strip()
    if value == "[]":
        return []
    if value.startswith(('"', "[", "{")):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return ast.literal_eval(value)
    return value


def _parse_frontmatter(text: str) -> dict[str, object]:
    result: dict[str, object] = {}
    current_list_key: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("  - "):
            if current_list_key is None:
                raise ValueError(f"Invalid frontmatter list item: {raw_line}")
            values = result.setdefault(current_list_key, [])
            if not isinstance(values, list):
                raise ValueError(f"Frontmatter key is not a list: {current_list_key}")
            values.append(_parse_scalar(line[4:]))
            continue

        current_list_key = None
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {raw_line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"Invalid frontmatter key: {raw_line}")
        if not value:
            result[key] = []
            current_list_key = key
            continue
        result[key] = _parse_scalar(value)

    return result


def _load_brick_detail(brick_id: str) -> dict[str, object]:
    matches = sorted(get_bricks_dir().glob(f"{brick_id}__*.md"))
    if not matches:
        raise FileNotFoundError(brick_id)
    if len(matches) > 1:
        raise ValueError(f"Multiple brick files found for {brick_id}")

    raw_text = matches[0].read_text(encoding="utf-8")
    if not raw_text.startswith("---\n"):
        raise ValueError("Markdown file missing frontmatter")

    _, rest = raw_text.split("---\n", 1)
    frontmatter_text, content_markdown = rest.split("\n---\n", 1)
    data = _parse_frontmatter(frontmatter_text)

    payload: dict[str, object] = {}
    for field in BRICK_DETAIL_FIELDS:
        value = data.get(field)
        if value is None and field in {"tags", "links", "decisions", "todo"}:
            value = []
        payload[field] = value
    payload["content_markdown"] = content_markdown.strip()
    return payload


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


def _build_excerpt(detail: dict[str, object], query_text: str, max_length: int = 160) -> str:
    searchable_parts = []
    for field in ("title", "summary_short", "resume_point", "content_markdown"):
        value = detail.get(field)
        if isinstance(value, str) and value:
            searchable_parts.append(value)

    haystack = "\n\n".join(searchable_parts)
    haystack_lower = haystack.lower()
    query_lower = query_text.lower()
    index = haystack_lower.find(query_lower)
    if index == -1:
        return haystack[:max_length].strip()

    start = max(0, index - 40)
    end = min(len(haystack), index + len(query_text) + 80)
    excerpt = haystack[start:end].strip()
    if start > 0:
        excerpt = "..." + excerpt
    if end < len(haystack):
        excerpt = excerpt + "..."
    return excerpt


def _find_bricks(query_text: str) -> list[dict[str, str]]:
    rows = []
    for path in sorted(get_bricks_dir().glob("MB-*.md")):
        brick_id = path.name.split("__", 1)[0]
        detail = _load_brick_detail(brick_id)
        searchable_parts = []
        for field in ("title", "summary_short", "resume_point", "content_markdown"):
            value = detail.get(field)
            if isinstance(value, str) and value:
                searchable_parts.append(value)
        haystack = "\n\n".join(searchable_parts)
        if query_text.lower() not in haystack.lower():
            continue
        rows.append(
            {
                "id": str(detail.get("id") or brick_id),
                "title": str(detail.get("title") or brick_id),
                "excerpt": _build_excerpt(detail, query_text),
            }
        )
    return rows


def _index_status_payload() -> dict[str, object]:
    index_dir = get_index_dir()
    return {
        "index_dir": str(index_dir),
        "index_dir_exists": index_dir.exists(),
        "index_full_exists": (index_dir / "index_full.json").exists(),
        "index_short_exists": (index_dir / "index_short.md").exists(),
        "sequence_exists": get_sequence_path().exists(),
    }


def _load_full_index() -> object:
    index_path = get_index_dir() / "index_full.json"
    if not index_path.exists():
        raise FileNotFoundError(index_path)
    return json.loads(index_path.read_text(encoding="utf-8"))


def _load_short_index() -> str:
    index_path = get_index_dir() / "index_short.md"
    if not index_path.exists():
        raise FileNotFoundError(index_path)
    return index_path.read_text(encoding="utf-8")


def _load_sequence() -> object:
    sequence_path = get_sequence_path()
    if not sequence_path.exists():
        raise FileNotFoundError(sequence_path)
    return json.loads(sequence_path.read_text(encoding="utf-8"))


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
    index_status_payload = _index_status_payload()
    brick_count = 0
    if bricks_dir.exists():
        brick_count = len(list(bricks_dir.glob("MB-*.md")))

    payload = {
        "root": str(root),
        "root_exists": root.exists(),
        "bricks_dir": bricks_dir.exists(),
        "bricks": brick_count,
        "index_full": index_status_payload["index_full_exists"],
        "index_short": index_status_payload["index_short_exists"],
        "sequence": index_status_payload["sequence_exists"],
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


@app.get("/bricks/{brick_id}")
def get_brick(brick_id: str):
    try:
        return _load_brick_detail(brick_id)
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"error": "Brick not found"})


@app.get("/find")
def find_bricks(text: str | None = None, limit: int = Query(default=50, ge=0), offset: int = Query(default=0, ge=0)):
    query_text = (text or "").strip()
    if not query_text:
        return JSONResponse(status_code=400, content={"error": "Query text cannot be empty"})

    matches = _find_bricks(query_text)
    total = len(matches)
    items = matches[offset : offset + limit]
    return {"items": items, "total": total, "query": query_text}


@app.get("/indexes/status")
def index_status():
    return _index_status_payload()


@app.get("/indexes/full")
def index_full():
    try:
        return _load_full_index()
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"error": "index_full.json not found"})


@app.get("/indexes/short")
def index_short():
    try:
        return {"content": _load_short_index()}
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"error": "index_short.md not found"})


@app.get("/indexes/sequence")
def index_sequence():
    try:
        return _load_sequence()
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"error": "sequence.json not found"})


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8112)


if __name__ == "__main__":
    main()
