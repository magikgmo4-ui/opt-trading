from __future__ import annotations

import argparse
import sys

from app.core.constants import ALLOWED_HANDOFF_TARGETS, ALLOWED_STATUSES, ALLOWED_TYPES
from app.core.paths import ensure_state_dirs, get_bricks_dir, get_index_dir, get_sequence_path, get_state_root
from app.services.create_brick import create_brick
from app.services.export_bricks import export_bricks
from app.services.find_bricks import find_bricks
from app.services.handoff_bricks import handoff_bricks
from app.services.link_bricks import link_bricks
from app.services.list_bricks import list_bricks
from app.services.merge_bricks import merge_bricks
from app.services.rebuild_index import rebuild_index
from app.services.show_brick import show_brick
from app.services.update_status import update_status


LIST_FILTERS = ["status", "type", "project", "module", "machine", "ia", "surface", "tag"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="memory_bricks")
    sub = parser.add_subparsers(dest="command", required=True)

    p_new = sub.add_parser("new", help="Create a new memory brick.")
    p_new.add_argument("--type", required=True, choices=sorted(ALLOWED_TYPES))
    p_new.add_argument("--title", required=True)
    p_new.add_argument("--ia", required=True)
    p_new.add_argument("--machine", required=True)
    p_new.add_argument("--surface", required=True)
    p_new.add_argument("--project", required=True)
    p_new.add_argument("--module", required=True)
    p_new.add_argument("--status", required=True, choices=sorted(ALLOWED_STATUSES))
    p_new.add_argument("--summary-short", default="")
    p_new.add_argument("--resume-point", default="")
    p_new.add_argument("--tags", default="")
    p_new.add_argument("--repo", default="")
    p_new.add_argument("--branch", default="")
    p_new.add_argument("--path", default="")
    p_new.add_argument("--decisions", default="")
    p_new.add_argument("--todo", default="")
    p_new.add_argument("--source-ref", default="")
    p_new.add_argument("--canonical-ref", default="")
    p_new.add_argument("--real-state-ref", default="")
    p_new.add_argument("--validated-by", default="")

    p_list = sub.add_parser("list", help="List bricks.")
    _add_list_filters(p_list)

    p_show = sub.add_parser("show", help="Show one brick.")
    p_show.add_argument("--id", required=True)

    p_status = sub.add_parser("status", help="Update brick status.")
    p_status.add_argument("--id", required=True)
    p_status.add_argument("--set", dest="new_status", required=True, choices=sorted(ALLOWED_STATUSES))

    p_link = sub.add_parser("link", help="Link one brick to another.")
    p_link.add_argument("--id", required=True)
    p_link.add_argument("--to", required=True)

    p_index = sub.add_parser("index", help="Index operations.")
    p_index_sub = p_index.add_subparsers(dest="index_command", required=True)
    p_index_sub.add_parser("rebuild", help="Rebuild indexes.")

    p_merge = sub.add_parser("merge", help="Merge bricks into one export.")
    p_merge.add_argument("--ids", required=True)

    p_export = sub.add_parser("export", help="Export bricks.")
    p_export.add_argument("--ids", required=True)
    p_export.add_argument("--format", required=True, choices=["txt", "md", "json"])

    p_handoff = sub.add_parser("handoff", help="Create IA handoff.")
    p_handoff.add_argument("--ids", required=True)
    p_handoff.add_argument("--target", required=True, choices=sorted(ALLOWED_HANDOFF_TARGETS))

    p_query = sub.add_parser("query", help="Read-only queries.")
    p_query_sub = p_query.add_subparsers(dest="query_command", required=True)

    p_query_sub.add_parser("status", help="Summarize the current source.")

    p_query_list = p_query_sub.add_parser("list", help="List bricks without writing state.")
    _add_list_filters(p_query_list)

    p_query_show = p_query_sub.add_parser("show", help="Show one brick without writing state.")
    p_query_show.add_argument("--id", required=True)

    p_query_find = p_query_sub.add_parser("find", help="Search bricks without writing state.")
    p_query_find.add_argument("--text", required=True)

    return parser


def _add_list_filters(parser: argparse.ArgumentParser) -> None:
    for arg in LIST_FILTERS:
        parser.add_argument(f"--{arg}", default="")


def _build_list_filters(args: argparse.Namespace) -> dict[str, str]:
    return {name: getattr(args, name) for name in LIST_FILTERS}


def _is_read_only_command(args: argparse.Namespace) -> bool:
    if args.command in {"list", "show"}:
        return True
    return args.command == "query" and args.query_command in {"status", "list", "show", "find"}


def _render_query_status() -> list[str]:
    root = get_state_root()
    bricks_dir = get_bricks_dir()
    index_dir = get_index_dir()
    brick_count = len(sorted(bricks_dir.glob("MB-*.md")))
    return [
        f"ROOT: {root}",
        f"ROOT_EXISTS: {'yes' if root.exists() else 'no'}",
        f"BRICKS_DIR: {'yes' if bricks_dir.exists() else 'no'}",
        f"BRICKS: {brick_count}",
        f"INDEX_FULL: {'yes' if (index_dir / 'index_full.json').exists() else 'no'}",
        f"INDEX_SHORT: {'yes' if (index_dir / 'index_short.md').exists() else 'no'}",
        f"SEQUENCE: {'yes' if get_sequence_path().exists() else 'no'}",
    ]


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not _is_read_only_command(args):
        ensure_state_dirs()

    try:
        if args.command == "new":
            result = create_brick(
                brick_type=args.type,
                title=args.title,
                ia=args.ia,
                machine=args.machine,
                surface=args.surface,
                project=args.project,
                module_name=args.module,
                status=args.status,
                summary_short=args.summary_short,
                resume_point=args.resume_point,
                tags=[t.strip() for t in args.tags.split(",") if t.strip()],
                repo=args.repo,
                branch=args.branch,
                path=args.path,
                decisions=[t.strip() for t in args.decisions.split(",") if t.strip()],
                todo=[t.strip() for t in args.todo.split(",") if t.strip()],
                source_ref=[t.strip() for t in args.source_ref.split(",") if t.strip()],
                canonical_ref=[t.strip() for t in args.canonical_ref.split(",") if t.strip()],
                real_state_ref=[t.strip() for t in args.real_state_ref.split(",") if t.strip()],
                validated_by=args.validated_by,
            )
            print(f"CREATED: {result['id']}")
            print(f"FILE: {result['file']}")
            return 0

        if args.command == "list":
            rows = list_bricks(_build_list_filters(args))
            for row in rows:
                print(row)
            return 0

        if args.command == "show":
            print(show_brick(args.id))
            return 0

        if args.command == "query" and args.query_command == "status":
            for line in _render_query_status():
                print(line)
            return 0

        if args.command == "query" and args.query_command == "list":
            rows = list_bricks(_build_list_filters(args))
            for row in rows:
                print(row)
            return 0

        if args.command == "query" and args.query_command == "show":
            print(show_brick(args.id))
            return 0

        if args.command == "query" and args.query_command == "find":
            rows = find_bricks(args.text)
            for row in rows:
                print(row)
            return 0

        if args.command == "status":
            before, after = update_status(args.id, args.new_status)
            print(f"UPDATED: {args.id} status={before} -> {after}")
            return 0

        if args.command == "link":
            link_bricks(args.id, args.to)
            print(f"LINKED: {args.id} -> {args.to}")
            return 0

        if args.command == "index" and args.index_command == "rebuild":
            paths = rebuild_index()
            print("INDEX REBUILT:")
            for path in paths:
                print(f"- {path}")
            return 0

        if args.command == "merge":
            out = merge_bricks(args.ids.split(","))
            print("MERGE CREATED:")
            print(f" {out}")
            return 0

        if args.command == "export":
            out = export_bricks(args.ids.split(","), args.format)
            print("EXPORT CREATED:")
            print(f" {out}")
            return 0

        if args.command == "handoff":
            out = handoff_bricks(args.ids.split(","), args.target)
            print("HANDOFF CREATED:")
            print(f" {out}")
            return 0

        parser.print_help()
        return 1
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
