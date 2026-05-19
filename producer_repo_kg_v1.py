#!/usr/bin/env python3
"""Producer Repo KG V1 - lecture seule. Genere graph_bundle.json depuis le repo reel."""

import hashlib
import json
import re
import subprocess
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# --- CONFIG ---
SCHEMA_VERSION = "repo_kg.v1"
PRODUCER_VERSION = "0.3.0"
SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "node_modules",
    "_archive",
    ".obsidian",
    "assets",
    "backups",
    "cache",
}
SKIP_FILES = {".env", ".secrets", ".token", "credentials.json", ".gitignore", "package-lock.json"}
SKIP_PATTERNS = [r"\.env$", r"\.secret", r"secret", r"_archive/legacy"]
MACHINES_KNOWN = {
    "admin-trading": {"name": "admin-trading", "role": "runtime", "confidence": "ESTABLISHED"},
    "student": {"name": "student", "role": "dev", "confidence": "ESTABLISHED"},
    "db-layer": {"name": "db-layer", "role": "db", "confidence": "ESTABLISHED"},
    "cursor-ai": {"name": "cursor-ai", "role": "windows_gui", "confidence": "ESTABLISHED"},
    "fantome": {"name": "fantome", "role": "dev", "confidence": "ESTABLISHED"},
}
APP_SPECS = {
    "clickup": {
        "label": "ClickUp",
        "role": "cockpit GO",
        "non_role": "source canonique",
        "source_doc": "docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/00_INITIAL_PROJECT_DOC.md",
        "related_go_ids": ["GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01"],
        "entrypoint_path": "docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01/execute_clickup.py",
    },
    "repo_kg": {
        "label": "Repo KG",
        "role": "projection repo-first",
        "non_role": "source canonique",
        "source_doc": "docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/01_cadrage_parent.md",
        "related_go_ids": [
            "GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01",
            "GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01",
        ],
        "entrypoint_path": "producer_repo_kg_v1.py",
    },
    "airtable": {
        "label": "Airtable",
        "role": "journal GO_Status",
        "non_role": "DB massive",
        "source_doc": "docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/00_INITIAL_PROJECT_DOC.md",
        "related_go_ids": [
            "GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01",
            "GO_OPT_TRADING_APPS_CHILD_AIRTABLE_RUNTIME_CREDENTIALS_BINDING_01",
        ],
        "entrypoint_path": "",
    },
    "botpress": {
        "label": "Botpress",
        "role": "operateur conversationnel",
        "non_role": "moteur trading",
        "source_doc": "docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/00_cadrage_parent.md",
        "related_go_ids": ["GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01", "GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_IMPL_01"],
        "entrypoint_path": "adapter_botpress_openclaw.py",
    },
}
BUNDLE_VIEWS = [
    {"name": "GO_MAP", "description": "All GO nodes with status"},
    {"name": "DOC_CANON_MAP", "description": "Document nodes by source_kind"},
    {"name": "MODULE_SURFACE_MAP", "description": "Modules with status and scripts"},
    {"name": "MACHINE_RUNTIME_MAP", "description": "Machines"},
    {"name": "BRANCH_WORK_MAP", "description": "Branch nodes"},
    {"name": "RESUME_MAP", "description": "Resume points"},
    {"name": "RISK_GAP_MAP", "description": "GAPs and RISKs"},
    {"name": "PRODUCER_CONSUMER_MAP", "description": "Producer and app surfaces"},
]
GO_TOKEN_RE = re.compile(r"GO_[A-Z0-9_]+")
GO_BRANCH_RE = re.compile(r"(go/GO_[A-Z0-9_]+|GO_[A-Z0-9_]+)")
SAFE_SOURCE_FILENAMES = {".env", ".secrets", ".token", "credentials.json", "id_rsa", "id_ed25519"}
CONFIDENCE_ORDER = {"UNKNOWN": 0, "HYPOTHESIS": 1, "INFERRED": 2, "ESTABLISHED": 3}
GO_STATUS_VALUES = {
    "UNKNOWN",
    "OPEN",
    "ACTIVE",
    "REFERENCE",
    "CLOSED",
    "PASS",
    "PASS_LIMITED",
    "FAIL",
    "PARTIAL",
    "BLOCKED",
}
GO_STATUS_CLASS = {
    "UNKNOWN": 0,
    "OPEN": 1,
    "REFERENCE": 1,
    "ACTIVE": 2,
    "BLOCKED": 2,
    "PARTIAL": 2,
    "CLOSED": 3,
    "PASS": 3,
    "PASS_LIMITED": 3,
    "FAIL": 3,
}
STATUS_CANON_SOURCES = {"GO_INDEX", "GO_CLOSED_INDEX", "REPRISE", "ACTIVE_STREAMS", "NEXT_GO_CANDIDATES"}
GO_STATUS_DOC_FRONTMATTER_VALUES = {"OPEN", "ACTIVE", "REFERENCE", "BLOCKED"}
VERDICT_STATUS_RE = re.compile(r"\b(PASS_LIMITED|PASS LIMITED|PASS|FAIL|PARTIAL|BLOCKED|CLOSED)\b", re.IGNORECASE)


def edge_id(src, tgt, etype):
    digest = hashlib.sha256(f"{src}::{tgt}::{etype}".encode()).hexdigest()[:12]
    return f"edge_{digest}"


def is_safe_path(path):
    text = str(path)
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, text):
            return False
    return True


def safe_json(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if hasattr(obj, "isoformat"):
        return str(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_sha():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore").replace("\ufeff", "")
    except Exception:
        return ""


def scan_files(base_dir, pattern="**/*"):
    results = []
    for path in ROOT.glob(f"{base_dir}/{pattern}"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        if not is_safe_path(path):
            continue
        results.append(path)
    return results


def parse_frontmatter(path):
    try:
        content = read_text(path)
        if not content.startswith("---"):
            return {}
        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}
        import yaml

        frontmatter = yaml.safe_load(parts[1])
        if isinstance(frontmatter, dict):
            return {
                key: (value.isoformat() if isinstance(value, datetime) else value)
                for key, value in frontmatter.items()
            }
        return frontmatter or {}
    except Exception:
        return {}


def split_markdown_row(line):
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def clean_cell(text):
    value = (text or "").replace("<br>", "; ").replace("`", "").strip()
    if value in {"", "-", "—", "â€”", "aucun", "Aucun"}:
        return ""
    return value


def normalize_status(raw, default="UNKNOWN"):
    value = clean_cell(raw).lower()
    if not value:
        return default
    mapping = {
        "open": "OPEN",
        "opened": "OPEN",
        "active": "ACTIVE",
        "reference": "REFERENCE",
        "closed": "CLOSED",
        "pass": "PASS",
        "pass_limited": "PASS_LIMITED",
        "fail": "FAIL",
        "partial": "PARTIAL",
        "blocked": "BLOCKED",
        "keep_active": "KEEP_ACTIVE",
        "keep_reference": "KEEP_REFERENCE",
        "drop_merged": "DROP_MERGED",
        "drop_local_only": "DROP_LOCAL_ONLY",
        "a_verifier": "A_VERIFIER",
        "non": "NON",
    }
    return mapping.get(value, value.upper().replace(" ", "_").replace("-", "_"))


def normalize_go_status(raw, default="UNKNOWN"):
    normalized = normalize_status(raw, default="")
    aliases = {
        "CLOSED_PASS": "PASS",
    }
    normalized = aliases.get(normalized, normalized)
    return normalized if normalized in GO_STATUS_VALUES else default


def normalize_branch_name(raw):
    branch = clean_cell(raw)
    if branch.startswith("remotes/"):
        branch = branch[len("remotes/") :]
    return branch


def extract_go_id_from_branch(branch_name):
    match = re.search(r"(?:^|/)(GO_[A-Z0-9_]+)", normalize_branch_name(branch_name))
    return match.group(1) if match else None


def extract_go_from_rel(rel):
    parts = rel.parts
    if len(parts) >= 3 and parts[0] == "docs" and parts[1] == "chantiers" and parts[2].startswith("GO_"):
        return parts[2]
    if len(parts) >= 4 and parts[0] == "docs" and parts[1] == "index" and parts[2] == "inbox" and rel.stem.startswith("GO_"):
        return rel.stem
    return ""


def extract_go_ids(text):
    return GO_TOKEN_RE.findall(text or "")


def extract_first_go_id(text):
    match = GO_TOKEN_RE.search(text or "")
    return match.group(0) if match else ""


def doc_rank(rel, frontmatter):
    doc_type = str(frontmatter.get("doc_type", "")).lower()
    name = rel.name.lower()
    if "closeout" in doc_type or name.startswith("90_") or name.startswith("99_"):
        return 50
    if "start" in doc_type or name.startswith("00_"):
        return 40
    if "cadrage" in doc_type or name.startswith("01_"):
        return 35
    if "reprise" in doc_type or "session_reprise" in name:
        return 30
    return 10


def extract_machine_mentions(content):
    matches = []
    patterns = [
        re.compile(r"^\s*\*\*Machine:\*\*\s*([a-z0-9\-]+)\s*$", re.IGNORECASE | re.MULTILINE),
        re.compile(r"^\s*-\s*machine(?:\s+cible(?:\s+unique)?)?\s*:\s*`?([a-z0-9\-]+)`?\s*$", re.IGNORECASE | re.MULTILINE),
    ]
    for pattern in patterns:
        for match in pattern.findall(content or ""):
            machine = clean_cell(match)
            if machine in MACHINES_KNOWN and machine not in matches:
                matches.append(machine)
    return matches


def extract_branch_mentions(content):
    matches = []
    patterns = [
        re.compile(r"^\s*-\s*branche(?:\s+source\s+prouvee)?\s*:\s*`?((?:origin/)?(?:go/)?GO_[A-Z0-9_]+)`?\s*$", re.MULTILINE),
        re.compile(r"^\s*\|\s*Branche\s*\|\s*`?((?:origin/)?(?:go/)?GO_[A-Z0-9_]+)`?\s*\|", re.MULTILINE),
    ]
    for pattern in patterns:
        for match in pattern.findall(content or ""):
            branch = normalize_branch_name(match)
            if branch and branch not in matches:
                matches.append(branch)
    return matches


def extract_next_go_block(content):
    lines = (content or "").splitlines()
    for index, line in enumerate(lines):
        if line.strip().upper() != "## NEXT_GO":
            continue
        for offset in range(index + 1, min(index + 8, len(lines))):
            candidate = clean_cell(lines[offset])
            next_go_id = extract_first_go_id(candidate)
            if next_go_id:
                return {"go_id": next_go_id, "raw": candidate}
    return None


def is_closeout_doc(rel, frontmatter):
    doc_type = str(frontmatter.get("doc_type", "")).lower()
    name = rel.name.lower()
    return "closeout" in doc_type or "verdict" in doc_type or name.startswith("90_") or name.startswith("99_")


def extract_closeout_verdict(content):
    lines = (content or "").splitlines()
    in_verdict_section = False
    for line in lines:
        stripped = line.strip()
        lowered = stripped.lower()
        if lowered.startswith("## verdict"):
            in_verdict_section = True
            continue
        if in_verdict_section and stripped.startswith("## "):
            break
        if not in_verdict_section or not stripped:
            continue
        match = VERDICT_STATUS_RE.search(stripped.replace("*", ""))
        if match:
            return normalize_go_status(match.group(1), default="")
    return ""


def derive_go_status_from_doc(frontmatter, rel, content):
    if is_closeout_doc(rel, frontmatter):
        verdict = extract_closeout_verdict(content)
        if verdict:
            return verdict, 70
        return "", 0

    normalized = normalize_go_status(frontmatter.get("status", ""), default="")
    if normalized in GO_STATUS_DOC_FRONTMATTER_VALUES:
        return normalized, doc_rank(rel, frontmatter)
    return "", 0


def is_terminal_self_transition(go_id, next_go_record):
    if not next_go_record or next_go_record.get("go_id") != go_id:
        return False
    return bool(re.search(r"\b(CLOSED|PASS|FAIL|PARTIAL|BLOCKED)\b", next_go_record.get("raw", ""), re.IGNORECASE))


def parse_go_table(path):
    content = read_text(path)
    records = []
    in_table = False
    for line in content.splitlines():
        cells = split_markdown_row(line)
        if cells and cells[:4] == ["PARENT", "CHANTIER", "SOUS_CHANTIER", "STATUT"]:
            in_table = True
            continue
        if in_table and cells and cells[0].startswith("---"):
            continue
        if in_table and cells:
            padded = cells + [""] * 6
            records.append(
                {
                    "parent": clean_cell(padded[0]),
                    "chantier": clean_cell(padded[1]),
                    "sous_chantier": clean_cell(padded[2]),
                    "status": normalize_status(padded[3]),
                    "dossier_present": clean_cell(padded[4]).lower().startswith("oui"),
                    "source_refs": padded[5].strip(),
                    "source_path": str(path.relative_to(ROOT)),
                }
            )
            continue
        if in_table and line.startswith("## "):
            break
        if in_table and not line.strip():
            continue
    return records


def parse_priority_bullets(path):
    content = read_text(path)
    priority_map = {}
    in_priority_section = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("## Priorit") or stripped.startswith("## Priorit"):
            in_priority_section = True
            continue
        if in_priority_section and stripped.startswith("## "):
            break
        if not in_priority_section or not stripped.startswith("- P"):
            continue
        match = re.match(r"-\s*(P\d)\s*:\s*(.*)$", stripped)
        if not match:
            continue
        priority = match.group(1)
        for go_id in extract_go_ids(match.group(2)):
            priority_map[go_id] = priority
    return priority_map


def parse_branch_state():
    path = ROOT / "docs/index/BRANCH_STATE.md"
    content = read_text(path)
    records = []
    in_table = False
    for line in content.splitlines():
        cells = split_markdown_row(line)
        if cells and cells[:3] == ["BRANCH", "SCOPE", "STATUS_VS_SOT_MAINLINE"]:
            in_table = True
            continue
        if in_table and cells and cells[0].startswith("---"):
            continue
        if in_table and cells:
            padded = cells + [""] * 9
            branch_name = normalize_branch_name(padded[0])
            records.append(
                {
                    "branch_name": branch_name,
                    "scope": clean_cell(padded[1]),
                    "status_vs_base": clean_cell(padded[2]),
                    "ahead_by": clean_cell(padded[3]),
                    "behind_by": clean_cell(padded[4]),
                    "canon_status": normalize_status(padded[5], default="ACTIVE"),
                    "action": clean_cell(padded[6]),
                    "justification": clean_cell(padded[7]),
                    "last_review_go": clean_cell(padded[8]),
                    "source_path": str(path.relative_to(ROOT)),
                }
            )
            continue
        if in_table and line.startswith("## "):
            break
    return records


def parse_next_go_candidates():
    path = ROOT / "docs/index/NEXT_GO_CANDIDATES.md"
    content = read_text(path)
    records = []
    in_table = False
    for line in content.splitlines():
        cells = split_markdown_row(line)
        if cells and cells[:4] == ["parent (actif)", "status", "priority", "next GO primaire"]:
            in_table = True
            continue
        if in_table and cells and cells[0].startswith("---"):
            continue
        if in_table and cells:
            padded = cells + [""] * 6
            parent_go = clean_cell(padded[0])
            next_go_text = clean_cell(padded[3])
            records.append(
                {
                    "parent_go": parent_go,
                    "status": normalize_status(padded[1]),
                    "priority": clean_cell(padded[2]),
                    "next_go": extract_first_go_id(next_go_text),
                    "next_action": clean_cell(padded[4]),
                    "refs": clean_cell(padded[5]),
                    "source_path": str(path.relative_to(ROOT)),
                }
            )
            continue
        if in_table and line.startswith("## "):
            break
    return records


def parse_reprise_table():
    path = ROOT / "docs/index/REPRISE.md"
    content = read_text(path)
    records = []
    in_table = False
    for line in content.splitlines():
        cells = split_markdown_row(line)
        if cells and cells[:4] == ["GO", "status", "priority", "repo canonical refs"]:
            in_table = True
            continue
        if in_table and cells and cells[0].startswith("---"):
            continue
        if in_table and cells:
            padded = cells + [""] * 8
            go_id = clean_cell(padded[0])
            records.append(
                {
                    "go_id": go_id,
                    "status": normalize_status(padded[1]),
                    "priority": clean_cell(padded[2]),
                    "repo_refs": clean_cell(padded[3]),
                    "support_refs": clean_cell(padded[4]),
                    "established_state": clean_cell(padded[5]),
                    "gap": clean_cell(padded[6]),
                    "next_action": clean_cell(padded[7]),
                    "source_path": str(path.relative_to(ROOT)),
                }
            )
            continue
        if in_table and line.startswith("## "):
            break
    return records


def parse_active_streams():
    path = ROOT / "docs/index/ACTIVE_STREAMS.md"
    content = read_text(path)
    streams = {}
    current_go = ""
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("### GO_"):
            current_go = stripped[4:].strip()
            streams.setdefault(current_go, {})
            continue
        if not current_go or not stripped.startswith("-"):
            continue
        key, _, value = stripped[1:].partition(":")
        if not value:
            continue
        key = key.strip().lower()
        value = clean_cell(value)
        if key == "statut":
            streams[current_go]["status"] = normalize_status(value)
        elif key == "branche":
            streams[current_go]["branch"] = normalize_branch_name(value)
        elif key == "prochaine action":
            streams[current_go]["next_action"] = value
        elif key == "blocages":
            streams[current_go]["blocking_gap"] = value
    return streams


go_data = {}


def ensure_go(go_id):
    if not go_id:
        return {}
    if go_id not in go_data:
        go_data[go_id] = {
            "go_id": go_id,
            "status": "UNKNOWN",
            "status_rank": 0,
            "status_class": 0,
            "parent_go_id": "",
            "parent_rank": 0,
            "priority": "",
            "priority_rank": 0,
            "has_chantier_folder": (ROOT / f"docs/chantiers/{go_id}").is_dir(),
            "source_tables": set(),
            "resume_point": "",
            "next_go_primary": "",
            "next_go_note": "",
            "next_action": "",
            "repo_refs": "",
            "support_refs": "",
            "gap": "",
            "established_state": "",
            "branches": [],
            "machines": [],
            "resume_entries": [],
            "todo_entries": [],
        }
    return go_data[go_id]


def set_go_status(go_id, status, rank, source_table=""):
    if not go_id or not status:
        return
    record = ensure_go(go_id)
    normalized = normalize_go_status(status, default="")
    if not normalized:
        return
    status_class = GO_STATUS_CLASS.get(normalized, 0)
    if status_class > record["status_class"] or (status_class == record["status_class"] and rank >= record["status_rank"]):
        record["status"] = normalized
        record["status_rank"] = rank
        record["status_class"] = status_class
    if source_table:
        record["source_tables"].add(source_table)


def set_go_parent(go_id, parent_go_id, rank):
    if not go_id or not parent_go_id or go_id == parent_go_id:
        return
    record = ensure_go(go_id)
    if rank >= record["parent_rank"]:
        record["parent_go_id"] = parent_go_id
        record["parent_rank"] = rank


def set_go_priority(go_id, priority, rank):
    if not go_id or not priority:
        return
    record = ensure_go(go_id)
    if rank >= record["priority_rank"]:
        record["priority"] = priority
        record["priority_rank"] = rank


def add_go_branch(go_id, branch_name, source_path, confidence="ESTABLISHED", evidence=""):
    if not go_id or not branch_name:
        return
    branch = normalize_branch_name(branch_name)
    if not branch:
        return
    record = ensure_go(go_id)
    entry = {
        "branch_name": branch,
        "source_path": source_path,
        "confidence": confidence,
        "evidence": evidence,
    }
    if entry not in record["branches"]:
        record["branches"].append(entry)


def add_go_machine(go_id, machine_name, source_path, evidence=""):
    if not go_id or machine_name not in MACHINES_KNOWN:
        return
    record = ensure_go(go_id)
    entry = {"machine": machine_name, "source_path": source_path, "evidence": evidence}
    if entry not in record["machines"]:
        record["machines"].append(entry)


def add_resume_entry(go_id, label, source_path, kind, details=""):
    if not go_id or not label:
        return
    record = ensure_go(go_id)
    entry = {"label": label, "source_path": source_path, "kind": kind, "details": details}
    if entry not in record["resume_entries"]:
        record["resume_entries"].append(entry)
    if not record["resume_point"]:
        record["resume_point"] = source_path


def add_todo_entry(go_id, label, source_path, next_go="", next_action="", priority=""):
    if not go_id or not label:
        return
    record = ensure_go(go_id)
    entry = {
        "label": label,
        "source_path": source_path,
        "next_go": next_go,
        "next_action": next_action,
        "priority": priority,
    }
    if entry not in record["todo_entries"]:
        record["todo_entries"].append(entry)


# --- STEP 1: PARSE CANONICAL GO SOURCES ---
for row in parse_go_table(ROOT / "docs/index/GO_INDEX.md"):
    parent_go = row["parent"] if row["parent"].startswith("GO_") else ""
    chantier_go = row["chantier"] if row["chantier"].startswith("GO_") else ""
    child_go = row["sous_chantier"] if row["sous_chantier"].startswith("GO_") else ""

    if parent_go:
        ensure_go(parent_go)
        go_data[parent_go]["source_tables"].add("GO_INDEX")
    if chantier_go:
        ensure_go(chantier_go)
        go_data[chantier_go]["source_tables"].add("GO_INDEX")
    if child_go:
        ensure_go(child_go)
        go_data[child_go]["source_tables"].add("GO_INDEX")

    target_go = child_go or chantier_go
    set_go_status(target_go, row["status"], 90, "GO_INDEX")

    if child_go:
        set_go_parent(child_go, chantier_go or parent_go, 90)
    elif chantier_go and parent_go and chantier_go != parent_go:
        set_go_parent(chantier_go, parent_go, 90)

for row in parse_go_table(ROOT / "docs/index/GO_CLOSED_INDEX.md"):
    parent_go = row["parent"] if row["parent"].startswith("GO_") else ""
    chantier_go = row["chantier"] if row["chantier"].startswith("GO_") else ""
    child_go = row["sous_chantier"] if row["sous_chantier"].startswith("GO_") else ""

    if parent_go:
        ensure_go(parent_go)
        go_data[parent_go]["source_tables"].add("GO_CLOSED_INDEX")
    if chantier_go:
        ensure_go(chantier_go)
        go_data[chantier_go]["source_tables"].add("GO_CLOSED_INDEX")
    if child_go:
        ensure_go(child_go)
        go_data[child_go]["source_tables"].add("GO_CLOSED_INDEX")

    target_go = child_go or chantier_go
    set_go_status(target_go, row["status"], 100, "GO_CLOSED_INDEX")

    if child_go:
        set_go_parent(child_go, chantier_go or parent_go, 100)
    elif chantier_go and parent_go and chantier_go != parent_go:
        set_go_parent(chantier_go, parent_go, 100)

for directory in ROOT.glob("docs/chantiers/GO_*"):
    ensure_go(directory.name)

for go_id, priority in parse_priority_bullets(ROOT / "docs/index/GO_INDEX.md").items():
    set_go_priority(go_id, priority, 90)
for go_id, priority in parse_priority_bullets(ROOT / "docs/index/ACTIVE_STREAMS.md").items():
    set_go_priority(go_id, priority, 80)
for go_id, priority in parse_priority_bullets(ROOT / "docs/index/NEXT_GO_CANDIDATES.md").items():
    set_go_priority(go_id, priority, 80)

active_streams = parse_active_streams()
for go_id, stream in active_streams.items():
    ensure_go(go_id)
    if stream.get("status"):
        set_go_status(go_id, stream["status"], 93, "ACTIVE_STREAMS")
    if stream.get("branch"):
        add_go_branch(go_id, stream["branch"], "docs/index/ACTIVE_STREAMS.md", "ESTABLISHED", "ACTIVE_STREAMS branch field")
    if stream.get("next_action"):
        go_data[go_id]["next_action"] = stream["next_action"]
    if stream.get("blocking_gap") and not go_data[go_id]["gap"]:
        go_data[go_id]["gap"] = stream["blocking_gap"]

for row in parse_reprise_table():
    go_id = row["go_id"]
    if not go_id.startswith("GO_"):
        continue
    ensure_go(go_id)
    set_go_status(go_id, row["status"], 92, "REPRISE")
    set_go_priority(go_id, row["priority"], 85)
    if row["repo_refs"]:
        go_data[go_id]["repo_refs"] = row["repo_refs"]
    if row["support_refs"]:
        go_data[go_id]["support_refs"] = row["support_refs"]
    if row["established_state"]:
        go_data[go_id]["established_state"] = row["established_state"]
    if row["gap"]:
        go_data[go_id]["gap"] = row["gap"]
    if row["next_action"]:
        go_data[go_id]["next_action"] = row["next_action"]
        add_resume_entry(
            go_id,
            f"REPRISE entry for {go_id}",
            row["source_path"],
            "reprise_table",
            row["next_action"],
        )

for row in parse_next_go_candidates():
    parent_go = row["parent_go"]
    if not parent_go.startswith("GO_"):
        continue
    ensure_go(parent_go)
    set_go_status(parent_go, row["status"], 80, "NEXT_GO_CANDIDATES")
    set_go_priority(parent_go, row["priority"], 80)
    if row["next_go"]:
        go_data[parent_go]["next_go_primary"] = row["next_go"]
    if row["next_action"] and not go_data[parent_go]["next_action"]:
        go_data[parent_go]["next_action"] = row["next_action"]
    add_todo_entry(
        parent_go,
        row["next_go"] or row["next_action"] or f"Next action for {parent_go}",
        row["source_path"],
        next_go=row["next_go"],
        next_action=row["next_action"],
        priority=row["priority"],
    )


# --- STEP 2: PARSE DOC-LEVEL GO EVIDENCE ---
for doc_path in scan_files("docs/chantiers") + scan_files("docs/index/inbox"):
    if doc_path.suffix not in {".md", ".txt"}:
        continue
    rel = doc_path.relative_to(ROOT)
    frontmatter = parse_frontmatter(doc_path)
    content = read_text(doc_path)
    go_id = clean_cell(frontmatter.get("go_id", "")) or extract_go_from_rel(rel)
    if not go_id.startswith("GO_"):
        continue

    record = ensure_go(go_id)
    doc_status, doc_status_rank = derive_go_status_from_doc(frontmatter, rel, content)
    if doc_status and not (record["source_tables"] & STATUS_CANON_SOURCES):
        set_go_status(go_id, doc_status, doc_status_rank, "DOC_FRONTMATTER")

    parent_go = clean_cell(frontmatter.get("parent_go", "")) or clean_cell(frontmatter.get("parent_go_id", ""))
    if parent_go.startswith("GO_"):
        set_go_parent(go_id, parent_go, 60)

    branch = clean_cell(frontmatter.get("branch", ""))
    if branch:
        add_go_branch(go_id, branch, str(rel), "ESTABLISHED", "frontmatter branch")

    machine = clean_cell(frontmatter.get("machine", ""))
    if machine in MACHINES_KNOWN:
        add_go_machine(go_id, machine, str(rel), "frontmatter machine")

    if clean_cell(frontmatter.get("point_de_reprise", "")):
        add_resume_entry(go_id, clean_cell(frontmatter["point_de_reprise"]), str(rel), "frontmatter_resume")

    next_go = extract_next_go_block(content)
    if next_go:
        next_go_id = "" if is_terminal_self_transition(go_id, next_go) else next_go["go_id"]
        if next_go_id and not go_data[go_id]["next_go_primary"]:
            go_data[go_id]["next_go_primary"] = next_go_id
        if next_go["raw"] != next_go_id and not go_data[go_id]["next_go_note"]:
            go_data[go_id]["next_go_note"] = next_go["raw"]
        add_todo_entry(go_id, next_go["raw"], str(rel), next_go=next_go_id, next_action="NEXT_GO")

    for branch_name in extract_branch_mentions(content):
        add_go_branch(go_id, branch_name, str(rel), "ESTABLISHED", "explicit branch line")

    for machine_name in extract_machine_mentions(content):
        add_go_machine(go_id, machine_name, str(rel), "explicit machine line")


# --- STEP 3: BUILD NODES AND EDGES ---
nodes = []
node_records = {}
edges = []
edge_records = {}
doc_nodes_by_path = {}
go_node_ids = {}
branch_node_ids = {}


def add_node(node_id, node_type, label, **props):
    status = props.pop("status", "UNKNOWN")
    source_path = props.pop("source_path", "")
    source_ref = props.pop("source_ref", "sot/mainline")
    confidence = props.pop("confidence", "ESTABLISHED")
    tags = props.pop("tags", [])

    if node_id in node_records:
        node = node_records[node_id]
        if status and node["status"] == "UNKNOWN":
            node["status"] = status
        if source_path and not node["source_path"]:
            node["source_path"] = source_path
        if source_ref and node["source_ref"] == "sot/mainline":
            node["source_ref"] = source_ref
        if CONFIDENCE_ORDER.get(confidence, 0) > CONFIDENCE_ORDER.get(node["confidence"], 0):
            node["confidence"] = confidence
        for key, value in props.items():
            if value not in (None, "", [], {}):
                node["properties"][key] = value
        return node_id

    node = {
        "id": node_id,
        "type": node_type,
        "label": label,
        "status": status,
        "source_path": source_path,
        "source_ref": source_ref,
        "confidence": confidence,
        "tags": tags,
        "properties": {key: value for key, value in props.items() if value not in (None, "", [], {})},
    }
    node_records[node_id] = node
    nodes.append(node)
    return node_id


def add_edge(src, tgt, edge_type, confidence="ESTABLISHED", source_path="", evidence=""):
    edge_key = edge_id(src, tgt, edge_type)
    if edge_key in edge_records:
        existing = edge_records[edge_key]
        if CONFIDENCE_ORDER.get(confidence, 0) > CONFIDENCE_ORDER.get(existing["confidence"], 0):
            existing["confidence"] = confidence
        if source_path and not existing["source_path"]:
            existing["source_path"] = source_path
        if evidence and not existing["evidence"]:
            existing["evidence"] = evidence
        return edge_key

    edge = {
        "id": edge_key,
        "source": src,
        "target": tgt,
        "type": edge_type,
        "confidence": confidence,
        "source_path": source_path,
        "evidence": evidence,
    }
    edge_records[edge_key] = edge
    edges.append(edge)
    return edge_key


repo_id = add_node(
    "repo_opt_trading",
    "REPO",
    "opt-trading",
    repo="opt-trading",
    repository_full_name="magikgmo4-ui/opt-trading",
    base_branch="sot/mainline",
    status="ACTIVE",
)

for file_path in scan_files("docs/governance"):
    frontmatter = parse_frontmatter(file_path)
    rel = file_path.relative_to(ROOT)
    node_id = add_node(
        f"doc_gov_{file_path.stem}",
        "GOVERNANCE",
        file_path.stem.replace("_", " ").title(),
        status="REFERENCE",
        source_path=str(rel),
        doc_id=frontmatter.get("doc_id", ""),
        doc_type=frontmatter.get("doc_type", "governance"),
        source_kind=frontmatter.get("source_kind", "canonical"),
    )
    add_edge(node_id, repo_id, "DOCUMENTS", "ESTABLISHED", str(rel), "governance doc references repo")

for file_path in scan_files("docs/index"):
    frontmatter = parse_frontmatter(file_path)
    if not frontmatter:
        continue
    rel = file_path.relative_to(ROOT)
    node_id = add_node(
        f"doc_idx_{file_path.stem}",
        "INDEX",
        frontmatter.get("doc_id", file_path.stem),
        status=normalize_status(frontmatter.get("status", "REFERENCE"), default="REFERENCE"),
        source_path=str(rel),
        doc_id=frontmatter.get("doc_id", ""),
        doc_type=frontmatter.get("doc_type", "index"),
        source_kind=frontmatter.get("source_kind", "canonical"),
        point_de_reprise=frontmatter.get("point_de_reprise", ""),
    )
    add_edge(node_id, repo_id, "DOCUMENTS", "ESTABLISHED", str(rel), "index doc")

for go_id in sorted(go_data):
    record = ensure_go(go_id)
    node_id = add_node(
        f"go_{go_id}",
        "GO",
        go_id,
        status=record["status"] if record["status"] != "UNKNOWN" else "OPEN",
        source_path=f"docs/chantiers/{go_id}" if record["has_chantier_folder"] else "",
        go_id=go_id,
        parent_go_id=record["parent_go_id"],
        priority=record["priority"],
        has_chantier_folder=record["has_chantier_folder"],
        source_table=",".join(sorted(record["source_tables"])) or "directory_scan",
        resume_point=record["resume_point"],
        next_go_primary=record["next_go_primary"],
        next_go_note=record["next_go_note"],
        next_action=record["next_action"],
        repo_refs=record["repo_refs"],
        support_refs=record["support_refs"],
        gap=record["gap"],
        established_state=record["established_state"],
    )
    go_node_ids[go_id] = node_id

for go_id, node_id in go_node_ids.items():
    parent_go_id = go_data[go_id]["parent_go_id"]
    if parent_go_id and parent_go_id in go_node_ids:
        add_edge(node_id, go_node_ids[parent_go_id], "BELONGS_TO", "ESTABLISHED", "docs/index/GO_INDEX.md")
    else:
        add_edge(node_id, repo_id, "BELONGS_TO", "ESTABLISHED", "docs/index/GO_INDEX.md")

for file_path in ROOT.glob("docs/chantiers/GO_*/**/*"):
    if not file_path.is_file() or file_path.suffix not in {".md", ".txt"}:
        continue
    if any(part in SKIP_DIRS for part in file_path.parts):
        continue
    rel = file_path.relative_to(ROOT)
    frontmatter = parse_frontmatter(file_path)
    parent_go = extract_go_from_rel(rel)
    node_id = add_node(
        f"doc_{rel.stem}_{hashlib.md5(str(rel).encode()).hexdigest()[:6]}",
        "DOC",
        file_path.name,
        status=normalize_status(frontmatter.get("status", "ACTIVE"), default="ACTIVE"),
        source_path=str(rel),
        path=str(rel),
        doc_id=frontmatter.get("doc_id", ""),
        doc_type=frontmatter.get("doc_type", ""),
        go_id=frontmatter.get("go_id", ""),
        source_kind=frontmatter.get("source_kind", "unknown"),
        updated_at=frontmatter.get("updated_at", ""),
    )
    doc_nodes_by_path[str(rel)] = node_id

    if parent_go and parent_go in go_node_ids:
        add_edge(go_node_ids[parent_go], node_id, "HAS_DOC", "ESTABLISHED", str(rel), "doc path under chantier")
        add_edge(node_id, go_node_ids[parent_go], "BELONGS_TO", "ESTABLISHED", str(rel), "doc path under chantier")

    doc_go = clean_cell(frontmatter.get("go_id", ""))
    if doc_go and doc_go in go_node_ids:
        add_edge(node_id, go_node_ids[doc_go], "DOCUMENTS", "ESTABLISHED", str(rel), f"frontmatter go_id={doc_go}")

for directory in sorted(ROOT.glob("modules/*")):
    if not directory.is_dir() or directory.name.startswith("_") or directory.name.startswith("."):
        continue
    rel = directory.relative_to(ROOT)
    module_id = add_node(
        f"mod_{directory.name}",
        "MODULE",
        directory.name,
        status="ACTIVE",
        source_path=str(rel),
        path=str(rel),
        has_cmd=(directory / "cmd.sh").exists(),
        has_menu=(directory / "menu.sh").exists(),
        has_sanity=any((directory / name).exists() for name in ["sanity_check.sh", "sanity_check_reseau_ssh.sh"]),
        has_readme=(directory / "README.md").exists(),
        runtime_role="runtime",
    )
    add_edge(module_id, repo_id, "BELONGS_TO", "ESTABLISHED", str(rel))

    for script in sorted(directory.glob("*.sh")):
        script_id = add_node(
            f"scr_{directory.name}_{script.stem}",
            "SCRIPT",
            script.name,
            status="ACTIVE",
            source_path=str(script.relative_to(ROOT)),
            path=str(script.relative_to(ROOT)),
        )
        add_edge(script_id, module_id, "BELONGS_TO", "ESTABLISHED", str(script.relative_to(ROOT)))
        if "sanity" in script.stem.lower():
            add_edge(script_id, module_id, "VALIDATES", "INFERRED", str(script.relative_to(ROOT)))

branch_inventory = {}
try:
    raw_branches = subprocess.check_output(["git", "branch", "-a"], cwd=ROOT, text=True).splitlines()
    for raw_line in raw_branches:
        line = normalize_branch_name(raw_line.lstrip("*").strip())
        if not line:
            continue
        match = GO_BRANCH_RE.search(line)
        if match:
            branch_name = match.group(1)
        elif line in {"sot/mainline", "main"}:
            branch_name = line
        else:
            continue
        entry = branch_inventory.setdefault(
            branch_name,
            {
                "branch_name": branch_name,
                "status": "ACTIVE",
                "scope": "",
                "status_vs_base": "",
                "ahead_by": "",
                "behind_by": "",
                "canon_status": "",
                "action": "",
                "justification": "",
                "last_review_go": "",
                "has_remote_ref": False,
                "has_local_ref": False,
                "source_path": "",
            },
        )
        if raw_line.strip().startswith("remotes/") or raw_line.strip().startswith("origin/"):
            entry["has_remote_ref"] = True
        else:
            entry["has_local_ref"] = True
except Exception:
    pass

for record in parse_branch_state():
    branch_name = record["branch_name"]
    if not (extract_go_id_from_branch(branch_name) or branch_name in {"sot/mainline", "main"}):
        continue
    entry = branch_inventory.setdefault(
        branch_name,
        {
            "branch_name": branch_name,
            "status": "ACTIVE",
            "scope": "",
            "status_vs_base": "",
            "ahead_by": "",
            "behind_by": "",
            "canon_status": "",
            "action": "",
            "justification": "",
            "last_review_go": "",
            "has_remote_ref": False,
            "has_local_ref": False,
            "source_path": record["source_path"],
        },
    )
    entry.update(record)
    entry["status"] = record["canon_status"] or entry["status"]

for branch_name in sorted(branch_inventory):
    record = branch_inventory[branch_name]
    node_id = add_node(
        f"branch_{branch_name.replace('/', '_')}",
        "BRANCH",
        branch_name,
        status=record["status"],
        source_path=record.get("source_path", ""),
        source_ref=branch_name,
        branch_name=branch_name,
        scope=record.get("scope", ""),
        status_vs_sot_mainline=record.get("status_vs_base", ""),
        ahead_by=record.get("ahead_by", ""),
        behind_by=record.get("behind_by", ""),
        canon_status=record.get("canon_status", ""),
        action=record.get("action", ""),
        justification=record.get("justification", ""),
        last_review_go=record.get("last_review_go", ""),
        has_remote_ref=record.get("has_remote_ref", False),
        has_local_ref=record.get("has_local_ref", False),
    )
    branch_node_ids[branch_name] = node_id
    add_edge(repo_id, node_id, "HAS_BRANCH", "ESTABLISHED", record.get("source_path", "") or branch_name)

for branch_name, node_id in branch_node_ids.items():
    go_id = extract_go_id_from_branch(branch_name)
    if go_id and go_id in go_node_ids:
        add_edge(node_id, go_node_ids[go_id], "REFERENCES", "INFERRED", branch_name, "branch name matches GO id")

for go_id, record in go_data.items():
    for branch_ref in record["branches"]:
        branch_name = normalize_branch_name(branch_ref["branch_name"])
        if branch_name in branch_node_ids:
            add_edge(
                branch_node_ids[branch_name],
                go_node_ids[go_id],
                "REFERENCES",
                branch_ref["confidence"],
                branch_ref["source_path"],
                branch_ref["evidence"],
            )

for machine_name, machine_props in MACHINES_KNOWN.items():
    machine_id = add_node(
        f"machine_{machine_name}",
        "MACHINE",
        machine_name,
        status="ACTIVE",
        confidence=machine_props["confidence"],
        name=machine_name,
        role=machine_props["role"],
    )
    add_edge(machine_id, repo_id, "BELONGS_TO", "ESTABLISHED", "docs/index/GO_INDEX.md")

producer_id = add_node(
    "producer_repo_kg_v1",
    "PRODUCER",
    "Repo KG Producer V1",
    status="ACTIVE",
    source_path="producer_repo_kg_v1.py",
    version=PRODUCER_VERSION,
)

for view in BUNDLE_VIEWS:
    view_id = add_node(
        f"view_{view['name']}",
        "VIEW",
        view["name"],
        status="ACTIVE",
        source_path="graph_bundle.json",
        description=view["description"],
    )
    add_edge(producer_id, view_id, "PRODUCES", "ESTABLISHED", "producer_repo_kg_v1.py", "Producer generates bundle view projection")

producer_go = ensure_go("GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01")
for machine_ref in producer_go["machines"]:
    add_edge(producer_id, f"machine_{machine_ref['machine']}", "RUNS_ON", "ESTABLISHED", machine_ref["source_path"], machine_ref["evidence"])

for app_id, spec in APP_SPECS.items():
    if not (ROOT / spec["source_doc"]).exists():
        continue
    app_node_id = add_node(
        f"app_{app_id}",
        "APP",
        spec["label"],
        status="PASS",
        source_path=spec["source_doc"],
        app_id=app_id,
        role=spec["role"],
        non_role=spec["non_role"],
        entrypoint_path=spec["entrypoint_path"],
        source_doc=spec["source_doc"],
    )
    add_edge(app_node_id, repo_id, "BELONGS_TO", "ESTABLISHED", spec["source_doc"], "app documented in canonical apps closeout")
    source_doc_node = doc_nodes_by_path.get(spec["source_doc"])
    if source_doc_node:
        add_edge(source_doc_node, app_node_id, "DOCUMENTS", "ESTABLISHED", spec["source_doc"], f"{spec['label']} documented in apps canonical state")
    for related_go in spec["related_go_ids"]:
        if related_go in go_node_ids:
            add_edge(app_node_id, go_node_ids[related_go], "REFERENCES", "ESTABLISHED", spec["source_doc"], f"{spec['label']} mapped to {related_go}")
    if app_id == "repo_kg":
        add_edge(app_node_id, producer_id, "DEPENDS_ON", "ESTABLISHED", spec["source_doc"], "Repo KG app uses the local producer")

for file_path in scan_files("docs", "**/SESSION_REPRISE.txt"):
    rel = file_path.relative_to(ROOT)
    go_id = extract_go_from_rel(rel)
    node_id = add_node(
        f"resume_{file_path.stem}_{hashlib.md5(str(rel).encode()).hexdigest()[:6]}",
        "RESUME_POINT",
        str(rel),
        status="ACTIVE",
        source_path=str(rel),
        kind="session_reprise",
    )
    if go_id in go_node_ids:
        add_edge(go_node_ids[go_id], node_id, "RESUMES_AT", "ESTABLISHED", str(rel), "SESSION_REPRISE file")
    else:
        add_edge(repo_id, node_id, "RESUMES_AT", "ESTABLISHED", str(rel), "repo-level SESSION_REPRISE file")

for go_id, record in go_data.items():
    for index, resume_entry in enumerate(record["resume_entries"], start=1):
        node_id = add_node(
            f"resume_{go_id}_{index}_{hashlib.md5((resume_entry['source_path'] + resume_entry['label']).encode()).hexdigest()[:6]}",
            "RESUME_POINT",
            resume_entry["label"],
            status="ACTIVE",
            source_path=resume_entry["source_path"],
            kind=resume_entry["kind"],
            details=resume_entry["details"],
        )
        if go_id in go_node_ids:
            add_edge(go_node_ids[go_id], node_id, "RESUMES_AT", "ESTABLISHED", resume_entry["source_path"], resume_entry["kind"])

for go_id, record in go_data.items():
    for index, todo_entry in enumerate(record["todo_entries"], start=1):
        label = todo_entry["label"]
        node_id = add_node(
            f"todo_{go_id}_{index}_{hashlib.md5((todo_entry['source_path'] + label).encode()).hexdigest()[:6]}",
            "TODO",
            label,
            status="ACTIVE",
            source_path=todo_entry["source_path"],
            next_go_id=todo_entry["next_go"],
            next_action=todo_entry["next_action"],
            priority=todo_entry["priority"],
        )
        if go_id in go_node_ids:
            add_edge(go_node_ids[go_id], node_id, "HAS_TODO", "ESTABLISHED", todo_entry["source_path"], "next go / next action")
        if todo_entry["next_go"] in go_node_ids:
            add_edge(node_id, go_node_ids[todo_entry["next_go"]], "REFERENCES", "ESTABLISHED", todo_entry["source_path"], "TODO references next GO")

gap_pattern = re.compile(r"#+\s*1[5-6]_.*GAP|REMAINING_GAP", re.IGNORECASE)
for file_path in scan_files("docs/chantiers"):
    rel = file_path.relative_to(ROOT)
    content = read_text(file_path)
    if not gap_pattern.search(content):
        continue
    go_id = extract_go_from_rel(rel)
    gap_id = add_node(
        f"gap_{rel.stem}_{hashlib.md5(str(rel).encode()).hexdigest()[:6]}",
        "GAP",
        f"Gap in {file_path.name}",
        status="OPEN",
        source_path=str(rel),
    )
    if go_id in go_node_ids:
        add_edge(go_node_ids[go_id], gap_id, "HAS_GAP", "ESTABLISHED", str(rel), "15_REMAINING_GAP or remaining gap section")

for go_id, record in go_data.items():
    for machine_ref in record["machines"]:
        if go_id in go_node_ids:
            add_edge(
                go_node_ids[go_id],
                f"machine_{machine_ref['machine']}",
                "RUNS_ON",
                "ESTABLISHED",
                machine_ref["source_path"],
                machine_ref["evidence"],
            )


# --- STEP 4: VALIDATE ---
validation_errors = []
node_types = {node["type"] for node in nodes}
allowed_node_types = {
    "REPO",
    "BRANCH",
    "COMMIT",
    "GO",
    "DOC",
    "GOVERNANCE",
    "INDEX",
    "MODULE",
    "SCRIPT",
    "TEST",
    "MACHINE",
    "SERVICE",
    "DECISION",
    "INVARIANT",
    "RESUME_POINT",
    "RISK",
    "GAP",
    "TODO",
    "VIEW",
    "CONSUMER",
    "PRODUCER",
    "APP",
}
if not node_types.issubset(allowed_node_types):
    validation_errors.append(f"Unknown node types: {sorted(node_types - allowed_node_types)}")

allowed_edge_types = {
    "HAS_BRANCH",
    "HAS_GO",
    "HAS_DOC",
    "DOCUMENTS",
    "BELONGS_TO",
    "DEPENDS_ON",
    "IMPLEMENTS",
    "RUNS_ON",
    "VALIDATES",
    "HAS_DECISION",
    "HAS_INVARIANT",
    "HAS_GAP",
    "HAS_TODO",
    "RESUMES_AT",
    "SUPERSEDES",
    "REFERENCES",
    "CONSUMES",
    "PRODUCES",
    "BLOCKS",
    "DERIVED_FROM",
}
edge_types = {edge["type"] for edge in edges}
if not edge_types.issubset(allowed_edge_types):
    validation_errors.append(f"Unknown edge types: {sorted(edge_types - allowed_edge_types)}")

for node in nodes:
    source_path = node.get("source_path", "") or ""
    if not source_path:
        continue
    file_name = Path(source_path).name.lower()
    if file_name in SAFE_SOURCE_FILENAMES:
        validation_errors.append(f"Potential secret in node path: {source_path}")

unexpected_go_statuses = sorted({node["status"] for node in nodes if node["type"] == "GO"} - GO_STATUS_VALUES)
if unexpected_go_statuses:
    validation_errors.append(f"Unexpected GO statuses: {unexpected_go_statuses}")


# --- STEP 5: EXPORT ---
graph_bundle = {
    "schema_version": SCHEMA_VERSION,
    "meta": {
        "repo": "opt-trading",
        "repository_full_name": "magikgmo4-ui/opt-trading",
        "base_branch": "sot/mainline",
        "producer_version": PRODUCER_VERSION,
        "generated_at": now_iso(),
        "source_commit": git_sha(),
        "mode": "read_only",
    },
    "nodes": nodes,
    "edges": edges,
    "views": BUNDLE_VIEWS,
    "validation": {
        "errors": validation_errors,
        "valid": len(validation_errors) == 0,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "go_count": len([node for node in nodes if node["type"] == "GO"]),
        "module_count": len([node for node in nodes if node["type"] == "MODULE"]),
        "branch_count": len([node for node in nodes if node["type"] == "BRANCH"]),
        "app_count": len([node for node in nodes if node["type"] == "APP"]),
    },
    "provenance": {
        "generated_by": "producer_repo_kg_v1.py",
        "generated_at": now_iso(),
        "source_repo": "magikgmo4-ui/opt-trading",
        "source_branch": normalize_branch_name(
            subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
        )
        if (ROOT / ".git").exists()
        else "unknown",
    },
}

output_path = ROOT / "graph_bundle.json"
output_path.write_text(json.dumps(graph_bundle, indent=2, ensure_ascii=False, default=safe_json), encoding="utf-8")

print("graph_bundle.json generated:")
print(f"  Nodes: {len(nodes)}")
print(f"  Edges: {len(edges)}")
print(f"  GOs: {len([node for node in nodes if node['type'] == 'GO'])}")
print(f"  Modules: {len([node for node in nodes if node['type'] == 'MODULE'])}")
print(f"  Branches: {len([node for node in nodes if node['type'] == 'BRANCH'])}")
print(f"  Apps: {len([node for node in nodes if node['type'] == 'APP'])}")
print(f"  Validation errors: {len(validation_errors)}")
print(f"  File: {output_path}")
if validation_errors:
    for error in validation_errors:
        print(f"    ERR: {error}")
