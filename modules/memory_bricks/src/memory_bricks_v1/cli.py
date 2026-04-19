from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class MemoryBricksError(Exception):
    exit_code = 1


class ValidationError(MemoryBricksError):
    exit_code = 2


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        result = _dispatch(args)
    except MemoryBricksError as exc:
        _print_error(exc.exit_code, str(exc), getattr(args, "command", None))
        return exc.exit_code
    except Exception as exc:  # pragma: no cover
        _print_error(1, str(exc), getattr(args, "command", None))
        return 1

    print(json.dumps(result, ensure_ascii=True))
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="memory_bricks_v1")
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_parser = subparsers.add_parser("new")
    new_parser.add_argument("--payload-file", required=True)

    link_parser = subparsers.add_parser("link")
    link_parser.add_argument("--id", required=True)
    link_parser.add_argument("--target", required=True)

    index_parser = subparsers.add_parser("index")
    index_subparsers = index_parser.add_subparsers(dest="index_command", required=True)
    index_subparsers.add_parser("rebuild")

    query_parser = subparsers.add_parser("query")
    query_subparsers = query_parser.add_subparsers(dest="query_command", required=True)
    query_subparsers.add_parser("status")

    return parser


def _dispatch(args: argparse.Namespace) -> dict[str, Any]:
    state_root = _resolve_state_root()
    if args.command == "new":
        return _cmd_new(state_root, Path(args.payload_file))
    if args.command == "link":
        return _cmd_link(state_root, args.id, args.target)
    if args.command == "index" and args.index_command == "rebuild":
        return _cmd_index_rebuild(state_root)
    if args.command == "query" and args.query_command == "status":
        return _cmd_query_status(state_root)
    raise ValidationError("Unsupported command")


def _cmd_new(state_root: Path, payload_file: Path) -> dict[str, Any]:
    if not payload_file.exists():
        raise ValidationError(f"Payload file not found: {payload_file}")
    raw = json.loads(payload_file.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValidationError("Payload file must contain a JSON object")
    payload = raw.get("brick", raw)
    if not isinstance(payload, dict):
        raise ValidationError("Brick payload must be a JSON object")

    brick_id = _next_brick_id(state_root)
    brick = {
        "id": brick_id,
        "title": _require_string(payload, "title"),
        "type": _optional_string(payload, "type", "decision"),
        "status": _optional_string(payload, "status", "closed"),
        "ia": _optional_string(payload, "ia", "unknown"),
        "machine": _optional_string(payload, "machine", "unknown"),
        "surface": _optional_string(payload, "surface", "unknown"),
        "project": _optional_string(payload, "project", "unknown"),
        "module": _optional_string(payload, "module", "memory_bricks"),
        "summary_short": _optional_string(payload, "summary_short", ""),
        "resume_point": _optional_string(payload, "resume_point", ""),
        "tags": _optional_list_of_strings(payload, "tags"),
        "links": _optional_list_of_strings(payload, "links"),
        "date": _now_z(),
        "decisions": _optional_list_of_strings(payload, "decisions"),
        "todo": _optional_list_of_strings(payload, "todo"),
        "content_markdown": _render_markdown(brick_id, payload),
    }

    brick_path = _bricks_dir(state_root) / f"{brick_id}.json"
    _ensure_dir(brick_path.parent)
    brick_path.write_text(json.dumps(brick, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return {"status": "created", "id": brick_id, "brick_path": str(brick_path)}


def _cmd_link(state_root: Path, brick_id: str, target: str) -> dict[str, Any]:
    brick = _load_brick(state_root, brick_id)
    links = list(brick.get("links", []))
    if target not in links:
        links.append(target)
    brick["links"] = links
    _write_brick(state_root, brick)
    return {"status": "linked", "id": brick_id, "target": target, "links_count": len(links)}


def _cmd_index_rebuild(state_root: Path) -> dict[str, Any]:
    _ensure_dir(state_root)
    bricks = _list_bricks(state_root)
    index_full = {
        "generated_at": _now_z(),
        "root": str(state_root),
        "items": [
            {
                "id": brick["id"],
                "title": brick["title"],
                "status": brick["status"],
                "type": brick["type"],
                "date": brick["date"],
                "tags": brick.get("tags", []),
            }
            for brick in bricks
        ],
    }
    (state_root / "index_full.json").write_text(json.dumps(index_full, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    lines = ["# Memory Bricks Index", ""]
    for brick in bricks:
        lines.append(f"- {brick['id']} | {brick['type']} | {brick['status']} | {brick['title']}")
    (state_root / "index_short.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"status": "rebuilt", "bricks": len(bricks), "root": str(state_root)}


def _cmd_query_status(state_root: Path) -> dict[str, Any]:
    root_exists = state_root.exists()
    bricks_dir = _bricks_dir(state_root)
    return {
        "root": str(state_root),
        "root_exists": root_exists,
        "bricks_dir": bricks_dir.exists(),
        "bricks": len(list(bricks_dir.glob("MB-*.json"))) if bricks_dir.exists() else 0,
        "index_full": (state_root / "index_full.json").exists(),
        "index_short": (state_root / "index_short.md").exists(),
        "sequence": (state_root / "sequence.txt").exists(),
    }


def _resolve_state_root() -> Path:
    raw = sys.modules[__name__].__dict__.get("__cached_state_root")
    if isinstance(raw, Path):
        return raw
    import os

    override = os.environ.get("MEMORY_BRICKS_STATE_ROOT", "").strip()
    if override:
        return Path(override)
    return Path(__file__).resolve().parents[4] / "_state" / "memory_bricks"


def _next_brick_id(state_root: Path) -> str:
    _ensure_dir(state_root)
    sequence_path = state_root / "sequence.txt"
    current = int(sequence_path.read_text(encoding="utf-8").strip()) if sequence_path.exists() else 0
    current += 1
    sequence_path.write_text(str(current) + "\n", encoding="utf-8")
    return f"MB-{current:05d}"


def _load_brick(state_root: Path, brick_id: str) -> dict[str, Any]:
    path = _bricks_dir(state_root) / f"{brick_id}.json"
    if not path.exists():
        raise ValidationError(f"Brick not found: {brick_id}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValidationError(f"Invalid brick payload: {brick_id}")
    return payload


def _write_brick(state_root: Path, brick: dict[str, Any]) -> None:
    brick_id = _require_string(brick, "id")
    path = _bricks_dir(state_root) / f"{brick_id}.json"
    _ensure_dir(path.parent)
    path.write_text(json.dumps(brick, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def _list_bricks(state_root: Path) -> list[dict[str, Any]]:
    bricks: list[dict[str, Any]] = []
    for path in sorted(_bricks_dir(state_root).glob("MB-*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            bricks.append(payload)
    return bricks


def _bricks_dir(state_root: Path) -> Path:
    return state_root / "bricks"


def _render_markdown(brick_id: str, payload: dict[str, Any]) -> str:
    title = _optional_string(payload, "title", brick_id)
    summary = _optional_string(payload, "summary_short", "")
    return f"# {title}\n\n- id: {brick_id}\n- summary: {summary}\n"


def _require_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"Missing required string: {key}")
    return value.strip()


def _optional_string(payload: dict[str, Any], key: str, default: str) -> str:
    value = payload.get(key)
    if value is None:
        return default
    if not isinstance(value, str):
        raise ValidationError(f"Expected string for {key}")
    return value.strip()


def _optional_list_of_strings(payload: dict[str, Any], key: str) -> list[str]:
    value = payload.get(key)
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValidationError(f"Expected list for {key}")
    items = []
    for item in value:
        if not isinstance(item, str):
            raise ValidationError(f"Expected string items in {key}")
        stripped = item.strip()
        if stripped:
            items.append(stripped)
    return items


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _now_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _print_error(code: int, message: str, command: str | None) -> None:
    payload = {"status": "error", "code": code, "command": command, "error": message}
    print(json.dumps(payload, ensure_ascii=True), file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
