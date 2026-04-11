#!/usr/bin/env python3
import argparse
import json
import re
import socket
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


TZ = ZoneInfo("America/Montreal")
REPO_ID = "magikgmo4-ui/opt-trading"
CONTINUITY_BRANCH = "sot/mainline"
GO_RE = re.compile(r"\b(GO_[A-Z0-9_]+)\b")
DATE_RE = re.compile(r"(?:Date \(America/Montreal\)|Dernière mise à jour \(America/Montreal\))\s*:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})")
CLOSING_REF_RE = re.compile(r"(OT_[A-Z0-9_]+_CLOSING(?:_REPORT)?\.txt)")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def relpath(path: Path, repo: Path) -> str:
    return str(path.relative_to(repo))


def now_iso() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def git_output(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def extract_doc_date(text: str) -> str | None:
    matches = DATE_RE.findall(text)
    return matches[-1] if matches else None


def extract_line_refs(path: Path, repo: Path, go_id: str) -> list[str]:
    refs = []
    for idx, line in enumerate(read_text(path).splitlines(), start=1):
        if go_id in line:
            refs.append(f"{relpath(path, repo)}:{idx}")
    return refs


def extract_item_caption(line: str, go_id: str) -> str | None:
    cleaned = line.strip().lstrip("- ").strip()
    cleaned = cleaned.replace(f"`{go_id}`", go_id)
    if not cleaned.startswith(go_id):
        return None
    remainder = cleaned[len(go_id):].strip(" .:-")
    if remainder.startswith("(") and remainder.endswith(")"):
        remainder = remainder[1:-1].strip()
    return remainder or None


def collect_section_lines(lines: list[str], heading: str) -> tuple[int | None, list[str]]:
    start = None
    for idx, line in enumerate(lines):
        if line.strip() == heading:
            start = idx
            break
    if start is None:
        return None, []

    out = []
    for line in lines[start + 1 :]:
        if line.startswith("## "):
            break
        out.append(line)
    return start + 1, out


def collect_nested_steps(section_lines: list[str], go_id: str) -> list[str]:
    steps = []
    in_target = False
    for raw in section_lines:
        stripped = raw.strip()
        if not stripped:
            if in_target:
                break
            continue
        if stripped.startswith("-") and go_id in stripped:
            in_target = True
            continue
        if not in_target:
            continue
        if raw.startswith("- ") and go_id not in stripped:
            break
        if raw.startswith("  - ") or raw.startswith("    - "):
            steps.append(stripped[2:].strip())
            continue
        if stripped.startswith("## "):
            break
    return steps


def discover_active_go_data(repo: Path) -> dict[str, dict]:
    kanban = repo / "docs/ot/kanban/opt_trading_kanban_source_of_truth.md"
    reprise = repo / "docs/ot/trae/OT_TRAE_SESSION_REPRISE.md"
    mission_start = repo / "docs/master_pack/mission_starter_pack/00_mission_start_guide.md"
    current_state = repo / "docs/master_pack/00_current_state_and_standards.md"
    closings_dir = repo / "docs/ot/closings"

    kanban_text = read_text(kanban)
    reprise_text = read_text(reprise)
    kanban_lines = kanban_text.splitlines()
    reprise_lines = reprise_text.splitlines()
    reprise_closing_refs = CLOSING_REF_RE.findall(reprise_text)

    records: dict[str, dict] = {}

    section_specs = [
        (kanban, kanban_lines, "## 4. POINT DE REPRISE SUIVANT", "ACTIVE"),
        (kanban, kanban_lines, "## 6. POINT DE REPRISE SUIVANT (DOCS)", "ACTIVE"),
        (kanban, kanban_lines, "## 7. POINT DE REPRISE SUIVANT (OPS)", "ACTIVE"),
        (kanban, kanban_lines, "## 10. POINT ACTIF CONSERVÉ", "ACTIVE"),
        (kanban, kanban_lines, "## 11. POINT CANDIDAT SI OUVERTURE DU CHANTIER TRAE V1", "CANDIDATE"),
        (reprise, reprise_lines, "## 5. Point de reprise global", "ACTIVE"),
    ]

    for path, lines, heading, state in section_specs:
        base_line, section_lines = collect_section_lines(lines, heading)
        if base_line is None:
            continue
        for offset, raw in enumerate(section_lines, start=1):
            match = GO_RE.search(raw)
            if not match:
                continue
            go_id = match.group(1)
            record = records.setdefault(
                go_id,
                {
                    "go_id": go_id,
                    "title": None,
                    "nature": "reprise_operatoire",
                    "state": state,
                    "canonical_docs": set(),
                    "evidence_refs": set(),
                    "step_fragments": [],
                    "last_established_candidates": [],
                },
            )
            if record["state"] != "ACTIVE" and state == "ACTIVE":
                record["state"] = "ACTIVE"
            if state == "CANDIDATE" and record["nature"] != "reprise_operatoire":
                record["nature"] = "candidat_ouverture"
            record["canonical_docs"].add(relpath(path, repo))
            record["evidence_refs"].add(f"{relpath(path, repo)}:{base_line + offset}")

            caption = extract_item_caption(raw, go_id)
            if caption and not record["title"]:
                record["title"] = caption

            doc_date = extract_doc_date(read_text(path))
            if doc_date:
                record["last_established_candidates"].append(doc_date)

    docs_section_start, docs_section_lines = collect_section_lines(
        kanban_lines, "## 6. POINT DE REPRISE SUIVANT (DOCS)"
    )
    ops_section_start, ops_section_lines = collect_section_lines(
        kanban_lines, "## 7. POINT DE REPRISE SUIVANT (OPS)"
    )

    for go_id, record in records.items():
        next_steps = []
        for step in collect_nested_steps(docs_section_lines, go_id):
            next_steps.append(f"docs: {step}")
        for step in collect_nested_steps(ops_section_lines, go_id):
            next_steps.append(f"ops: {step}")
        record["step_fragments"] = next_steps

        latest_closing = None
        latest_closing_key = None
        locked_from_reprise = False
        for closing_name in reversed(reprise_closing_refs):
            closing = closings_dir / closing_name
            if not closing.exists():
                continue
            closing_text = read_text(closing)
            if go_id not in closing_text:
                continue
            latest_closing = closing
            closing_date = extract_doc_date(closing_text)
            latest_closing_key = (
                closing_date or "0000-00-00",
                int(closing.stat().st_mtime),
                closing.name,
            )
            locked_from_reprise = True
            break
        if not locked_from_reprise:
            for closing in sorted(closings_dir.glob("OT_*_CLOSING*.txt")):
                closing_text = read_text(closing)
                if go_id not in closing_text:
                    continue
                closing_date = extract_doc_date(closing_text)
                candidate_key = (
                    closing_date or "0000-00-00",
                    int(closing.stat().st_mtime),
                    closing.name,
                )
                if latest_closing_key is None or candidate_key > latest_closing_key:
                    latest_closing = closing
                    latest_closing_key = candidate_key
        if latest_closing is not None:
            record["canonical_docs"].add(relpath(latest_closing, repo))
            for ref in extract_line_refs(latest_closing, repo, go_id):
                record["evidence_refs"].add(ref)
            if latest_closing_key and latest_closing_key[0] != "0000-00-00":
                record["last_established_candidates"].append(latest_closing_key[0])

        for path in (kanban, reprise, mission_start, current_state):
            record["canonical_docs"].add(relpath(path, repo))

        for path in (kanban, reprise):
            for ref in extract_line_refs(path, repo, go_id):
                record["evidence_refs"].add(ref)

        if not record["title"]:
            record["title"] = go_id

    return records


def build_rows(repo: Path) -> list[dict]:
    work_branch = git_output(repo, "rev-parse", "--abbrev-ref", "HEAD")
    updated_at = now_iso()
    hostname = socket.gethostname()

    rows = []
    for go_id, record in sorted(discover_active_go_data(repo).items()):
        last_established = None
        if record["last_established_candidates"]:
            last_established = sorted(record["last_established_candidates"])[-1]

        nature = record["nature"]
        if record["state"] == "CANDIDATE":
            nature = "candidat_ouverture"

        rows.append(
            {
                "go_id": go_id,
                "title": record["title"],
                "nature": nature,
                "owner_machine": hostname,
                "repo": REPO_ID,
                "continuity_branch": CONTINUITY_BRANCH,
                "work_branch": work_branch,
                "state": record["state"],
                "last_established": last_established,
                "next_step": " ; ".join(record["step_fragments"]) if record["step_fragments"] else "n/a",
                "canonical_docs": sorted(record["canonical_docs"]),
                "evidence_refs": sorted(record["evidence_refs"]),
                "updated_at": updated_at,
                "tags": sorted({record["state"].lower(), nature, hostname, CONTINUITY_BRANCH.replace("/", "_")}),
            }
        )
    return rows


def render_markdown(rows: list[dict]) -> str:
    stamp = now_iso()
    lines = [
        "# ACTIVE GO MATRIX",
        "",
        f"Generated at: `{stamp}`",
        "",
        "Source rule: this matrix is generated from canonical docs and machine git context; it does not replace the kanban or closings.",
        "",
        "| go_id | state | owner_machine | work_branch | last_established | next_step |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['go_id']}` | `{row['state']}` | `{row['owner_machine']}` | `{row['work_branch']}` | `{row['last_established'] or 'n/a'}` | {row['next_step']} |"
        )

    for row in rows:
        lines.extend(
            [
                "",
                f"## {row['go_id']}",
                f"- title: `{row['title']}`",
                f"- nature: `{row['nature']}`",
                f"- owner_machine: `{row['owner_machine']}`",
                f"- repo: `{row['repo']}`",
                f"- continuity_branch: `{row['continuity_branch']}`",
                f"- work_branch: `{row['work_branch']}`",
                f"- state: `{row['state']}`",
                f"- last_established: `{row['last_established'] or 'n/a'}`",
                f"- next_step: {row['next_step']}",
                f"- canonical_docs: {'; '.join(f'`{doc}`' for doc in row['canonical_docs'])}",
                f"- evidence_refs: {'; '.join(f'`{ref}`' for ref in row['evidence_refs'])}",
                f"- updated_at: `{row['updated_at']}`",
                f"- tags: `{', '.join(row['tags'])}`",
            ]
        )

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=None)
    parser.add_argument("--out-dir", default=None)
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    repo = Path(args.repo).resolve() if args.repo else script_dir.parents[2]
    out_dir = Path(args.out_dir).resolve() if args.out_dir else repo / "journal/index"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = build_rows(repo)
    payload = {
        "generated_at": now_iso(),
        "source_of_truth": {
            "kanban": "docs/ot/kanban/opt_trading_kanban_source_of_truth.md",
            "session_reprise": "docs/ot/trae/OT_TRAE_SESSION_REPRISE.md",
            "mission_start": "docs/master_pack/mission_starter_pack/00_mission_start_guide.md",
            "current_state": "docs/master_pack/00_current_state_and_standards.md",
        },
        "rows": rows,
    }

    md_path = out_dir / "ACTIVE_GO_MATRIX.md"
    json_path = out_dir / "ACTIVE_GO_MATRIX.json"
    md_path.write_text(render_markdown(rows), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(md_path)
    print(json_path)
    print(f"ROWS={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
