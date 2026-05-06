#!/usr/bin/env python3
"""Producer Repo KG V1 — lecture seule. Genere graph_bundle.json depuis le repo reel."""

import os, re, json, subprocess, hashlib
from datetime import datetime, date, timezone
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent

# ─── CONFIG ───
SCHEMA_VERSION = "repo_kg.v1"
PRODUCER_VERSION = "0.1.0"
SKIP_DIRS = {".git", "__pycache__", ".mypy_cache", ".pytest_cache", "node_modules",
             "_archive", ".obsidian", "assets", "backups", "cache"}
SKIP_FILES = {".env", ".secrets", ".token", "credentials.json", ".gitignore", "package-lock.json"}
SKIP_PATTERNS = [r"\.env$", r"\.secret", r"secret", r"_archive/legacy"]
MACHINES_KNOWN = {
    "admin-trading": {"name": "admin-trading", "role": "runtime", "confidence": "ESTABLISHED"},
    "student":       {"name": "student",       "role": "dev",     "confidence": "ESTABLISHED"},
    "db-layer":      {"name": "db-layer",      "role": "db",      "confidence": "ESTABLISHED"},
    "cursor-ai":     {"name": "cursor-ai",     "role": "windows_gui", "confidence": "ESTABLISHED"},
    "fantome":       {"name": "fantome",       "role": "dev",     "confidence": "ESTABLISHED"},
}

def stable_id(*parts):
    h = hashlib.sha256("::".join(parts).encode()).hexdigest()[:12]
    return f"node_{h}"

def edge_id(src, tgt, etype):
    h = hashlib.sha256(f"{src}::{tgt}::{etype}".encode()).hexdigest()[:12]
    return f"edge_{h}"

def is_safe_path(path):
    s = str(path)
    for p in SKIP_PATTERNS:
        if re.search(p, s):
            return False
    return True

def safe_json(o):
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    if hasattr(o, 'isoformat'):
        return str(o)
    raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def git_sha():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"

# ─── STEP 1: SCAN ───
def scan_files(base_dir, pattern="**/*"):
    results = []
    for p in ROOT.glob(f"{base_dir}/{pattern}"):
        if not p.is_file():
            continue
        if any(d in p.parts for d in SKIP_DIRS):
            continue
        if p.name in SKIP_FILES:
            continue
        if not is_safe_path(str(p)):
            continue
        results.append(p)
    return results

# ─── STEP 2: PARSE FRONTMATTER ───
def parse_frontmatter(path):
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
        if not content.startswith("---"):
            return {}
        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}
        import yaml
        fm = yaml.safe_load(parts[1])
        if isinstance(fm, dict):
            fm = {k: (v.isoformat() if isinstance(v, datetime) else v) for k, v in fm.items()}
        return fm or {}
    except Exception:
        return {}

# ─── STEP 3: PARSE GO_INDEX ───
def parse_go_index():
    go_index_path = ROOT / "docs/index/GO_INDEX.md"
    if not go_index_path.exists():
        return []
    content = go_index_path.read_text(encoding="utf-8", errors="ignore")
    gos = []
    in_table = False
    for line in content.split("\n"):
        if "Tableau canonique des chantiers" in line:
            in_table = True
            continue
        if in_table and line.startswith("##") and "Tableau" not in line:
            in_table = False
            continue
        if in_table and line.startswith("|") and "---" not in line and "STATUT" not in line:
            parts = [c.strip() for c in line.split("|") if c.strip()]
            if len(parts) >= 5:
                go_id = parts[2] if len(parts) >= 4 else parts[1] if len(parts) >= 2 else ""
                if go_id.startswith("GO_"):
                    gos.append({
                        "go_id": go_id,
                        "status": parts[4] if len(parts) >= 6 else (parts[3] if len(parts) >= 5 else "UNKNOWN"),
                        "chantier_present": "oui" in line.lower() if len(parts) >= 6 else None,
                        "source_refs": parts[6] if len(parts) >= 7 else "",
                    })
    return gos

# ─── STEP 4: PARSE BRANCH_STATE ───
def parse_branch_state():
    bp = ROOT / "docs/index/BRANCH_STATE.md"
    if not bp.exists():
        return []
    content = bp.read_text(encoding="utf-8", errors="ignore")
    branches = []
    in_table = False
    for line in content.split("\n"):
        if line.startswith("|") and "BRANCH" in line and "STATUT" in line:
            in_table = True
            continue
        if in_table and line.startswith("|") and "---" not in line:
            parts = [c.strip() for c in line.split("|") if c.strip()]
            if len(parts) >= 3:
                branches.append({
                    "name": parts[0].replace("go/", "").replace("origin/", ""),
                    "full_name": parts[0],
                    "presence": parts[1] if len(parts) > 1 else "unknown",
                    "status": parts[2] if len(parts) > 2 else "unknown",
                })
        elif in_table and not line.startswith("|"):
            in_table = False
    return branches

# ─── STEP 5: BUILD NODES ───
nodes = []
node_ids = {}  # key -> id for dedup
edges = []

def add_node(nid, ntype, label, **props):
    if nid in node_ids:
        return node_ids[nid]
    node = {
        "id": nid,
        "type": ntype,
        "label": label,
        "status": props.pop("status", "UNKNOWN"),
        "source_path": props.pop("source_path", ""),
        "source_ref": props.pop("source_ref", "sot/mainline"),
        "confidence": props.pop("confidence", "ESTABLISHED"),
        "tags": props.pop("tags", []),
        "properties": props,
    }
    node_ids[nid] = nid
    nodes.append(node)
    return nid

def add_edge(src, tgt, etype, confidence="ESTABLISHED", source_path="", evidence=""):
    eid = edge_id(src, tgt, etype)
    edges.append({
        "id": eid,
        "source": src,
        "target": tgt,
        "type": etype,
        "confidence": confidence,
        "source_path": source_path,
        "evidence": evidence,
    })
    return eid

# ─── REPO node ───
repo_id = add_node("repo_opt_trading", "REPO", "opt-trading",
    repo="opt-trading", repository_full_name="magikgmo4-ui/opt-trading",
    base_branch="sot/mainline", status="ACTIVE")

# ─── GOVERNANCE nodes ───
for f in scan_files("docs/governance"):
    fm = parse_frontmatter(f)
    rel = f.relative_to(ROOT)
    nid = add_node(f"doc_gov_{f.stem}", "GOVERNANCE", f.stem.replace("_", " ").title(),
        status="REFERENCE", source_path=str(rel),
        doc_id=fm.get("doc_id", ""), doc_type=fm.get("doc_type", "governance"),
        source_kind=fm.get("source_kind", "canonical"))
    add_edge(nid, repo_id, "DOCUMENTS", "ESTABLISHED", str(rel), "governance doc references repo")

# ─── INDEX nodes ───
for f in scan_files("docs/index"):
    fm = parse_frontmatter(f)
    if not fm:
        continue
    rel = f.relative_to(ROOT)
    nid = add_node(f"doc_idx_{f.stem}", "INDEX", fm.get("doc_id", f.stem),
        status=fm.get("status", "REFERENCE"), source_path=str(rel),
        doc_id=fm.get("doc_id", ""), doc_type=fm.get("doc_type", "index"),
        source_kind=fm.get("source_kind", "canonical"))
    add_edge(nid, repo_id, "DOCUMENTS", "ESTABLISHED", str(rel), "index doc")

# ─── GO nodes from GO_INDEX ───
go_index_entries = parse_go_index()
go_nodes = defaultdict(dict)
for entry in go_index_entries:
    gid = entry["go_id"]
    chantier_dir = ROOT / f"docs/chantiers/{gid}"
    exists = chantier_dir.is_dir()
    nid = add_node(f"go_{gid}", "GO", gid,
        status=entry["status"].upper(), source_path=f"docs/chantiers/{gid}" if exists else "",
        go_id=gid, parent_go_id=None, priority=None,
        has_chantier_folder=exists, source_table="GO_INDEX",
        resume_point=None)
    add_edge(nid, repo_id, "BELONGS_TO", "ESTABLISHED", "docs/index/GO_INDEX.md")
    go_nodes[gid] = {"nid": nid, "exists": exists, "status": entry["status"]}

# ─── GO nodes from chantier directories (supplement) ───
for d in ROOT.glob("docs/chantiers/GO_*"):
    gid = d.name
    if gid not in go_nodes:
        nid = add_node(f"go_{gid}", "GO", gid,
            status="OPEN", source_path=str(d.relative_to(ROOT)),
            go_id=gid, parent_go_id=None, has_chantier_folder=True,
            source_table="directory_scan", resume_point=None)
        go_nodes[gid] = {"nid": nid, "exists": True, "status": "OPEN"}

# ─── DOC nodes from chantiers ───
for d in ROOT.glob("docs/chantiers/GO_*/**/*"):
    if not d.is_file():
        continue
    if not d.suffix in (".md", ".txt"):
        continue
    if any(skip in d.parts for skip in SKIP_DIRS):
        continue
    rel = d.relative_to(ROOT)
    fm = parse_frontmatter(d)
    parent_go = d.parts[1] if len(d.parts) > 1 and d.parts[1].startswith("GO_") else None
    nid = add_node(f"doc_{rel.stem}_{hashlib.md5(str(rel).encode()).hexdigest()[:6]}",
        "DOC", d.name,
        status="ACTIVE", source_path=str(rel),
        path=str(rel), doc_id=fm.get("doc_id", ""), doc_type=fm.get("doc_type", ""),
        go_id=fm.get("go_id", ""), source_kind=fm.get("source_kind", "unknown"),
        updated_at=fm.get("updated_at", ""))

    # Edge: DOC -> parent GO
    if parent_go and parent_go in go_nodes:
        add_edge(nid, go_nodes[parent_go]["nid"], "BELONGS_TO", "INFERRED", str(rel))
    # Edge: DOC -> GO from frontmatter
    doc_go = fm.get("go_id", "")
    if doc_go and doc_go in go_nodes:
        add_edge(nid, go_nodes[doc_go]["nid"], "DOCUMENTS", "INFERRED", str(rel), f"frontmatter go_id={doc_go}")

# ─── MODULE nodes ───
for d in sorted(ROOT.glob("modules/*")):
    if not d.is_dir():
        continue
    if d.name.startswith("_") or d.name.startswith("."):
        continue
    rel = d.relative_to(ROOT)
    nid = add_node(f"mod_{d.name}", "MODULE", d.name,
        status="ACTIVE", source_path=str(rel),
        path=str(rel), has_cmd=(d / "cmd.sh").exists(),
        has_menu=(d / "menu.sh").exists(),
        has_sanity=any((d / f).exists() for f in ["sanity_check.sh", "sanity_check_reseau_ssh.sh"]),
        has_readme=(d / "README.md").exists(),
        runtime_role="runtime")
    add_edge(nid, repo_id, "BELONGS_TO", "ESTABLISHED", str(rel))

    # Edge: MODULE -> SCRIPTs
    for script in sorted(d.glob("*.sh")):
        sid = add_node(f"scr_{d.name}_{script.stem}", "SCRIPT", script.name,
            status="ACTIVE", source_path=str(script.relative_to(ROOT)),
            path=str(script.relative_to(ROOT)))
        add_edge(sid, nid, "BELONGS_TO", "ESTABLISHED", str(script.relative_to(ROOT)))
        if "sanity" in script.stem.lower():
            add_edge(sid, nid, "VALIDATES", "INFERRED", str(script.relative_to(ROOT)))

# ─── BRANCH nodes ───
try:
    branches_raw = subprocess.check_output(["git", "branch", "-a"], cwd=ROOT, text=True).split("\n")
    go_branch_re = re.compile(r"go/[A-Z_]+\d+")
    for line in branches_raw:
        line = line.strip().lstrip("*").strip()
        match = go_branch_re.search(line)
        if match:
            bn = match.group()
            nid = add_node(f"branch_{bn.replace('/', '_')}", "BRANCH", bn,
                status="ACTIVE", source_ref=bn, branch_name=bn, is_remote="remote" in line)
            add_edge(nid, repo_id, "HAS_BRANCH", "ESTABLISHED", bn)
except Exception:
    pass

# ─── BRANCH_STATE nodes (complément) ───
for bs in parse_branch_state():
    bn = bs["full_name"]
    nid_key = f"branch_{bn.replace('/', '_')}"
    if nid_key not in node_ids:
        nid = add_node(nid_key, "BRANCH", bn,
            status=bs["status"].upper(), source_path="docs/index/BRANCH_STATE.md",
            branch_name=bn)
        add_edge(nid, repo_id, "HAS_BRANCH", "ESTABLISHED", "docs/index/BRANCH_STATE.md")

# ─── MACHINE nodes ───
for mn, mp in MACHINES_KNOWN.items():
    nid = add_node(f"machine_{mn}", "MACHINE", mn,
        status="ACTIVE", confidence=mp["confidence"],
        name=mn, role=mp["role"])
    add_edge(nid, repo_id, "BELONGS_TO", "INFERRED", "docs/chantiers/REPRISE.md")

# ─── PRODUCER node ───
producer_id = add_node("producer_repo_kg_v1", "PRODUCER", "Repo KG Producer V1",
    status="ACTIVE", source_path="modules/repo_knowledge_graph/", version=PRODUCER_VERSION)
add_edge(producer_id, repo_id, "PRODUCES", "ESTABLISHED", "", "Producer generates graph_bundle.json")

# ─── RESUME_POINT nodes ───
for f in scan_files("docs", "**/SESSION_REPRISE.txt"):
    rel = f.relative_to(ROOT)
    parent_go = f.parts[2] if len(f.parts) > 2 and f.parts[2].startswith("GO_") else "repo"
    nid = add_node(f"resume_{f.stem}_{hashlib.md5(str(rel).encode()).hexdigest()[:6]}",
        "RESUME_POINT", str(rel),
        status="ACTIVE", source_path=str(rel))
    if parent_go == "repo":
        add_edge(nid, repo_id, "RESUMES_AT", "ESTABLISHED", str(rel))
    elif parent_go in go_nodes:
        add_edge(nid, go_nodes[parent_go]["nid"], "RESUMES_AT", "ESTABLISHED", str(rel))

# ─── GAP nodes (from docs with 15_REMAINING_GAP) ───
gap_re = re.compile(r'#+\s*1[5-6]_.*GAP|REMAINING_GAP', re.IGNORECASE)
for f in scan_files("docs/chantiers"):
    rel = f.relative_to(ROOT)
    content = ""
    try:
        content = f.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    if gap_re.search(content):
        parent_go = f.parts[1] if len(f.parts) > 1 and f.parts[1].startswith("GO_") else None
        nid = add_node(f"gap_{f.stem}_{hashlib.md5(str(rel).encode()).hexdigest()[:6]}",
            "GAP", f"Gap in {f.name}",
            status="OPEN", source_path=str(rel))
        if parent_go and parent_go in go_nodes:
            add_edge(nid, go_nodes[parent_go]["nid"], "HAS_GAP", "INFERRED", str(rel))

# ─── STEP 7: VALIDATE ───
validation_errors = []
node_types = {n["type"] for n in nodes}
allowed_node_types = {"REPO", "BRANCH", "COMMIT", "GO", "DOC", "GOVERNANCE", "INDEX",
    "MODULE", "SCRIPT", "TEST", "MACHINE", "SERVICE", "DECISION", "INVARIANT",
    "RESUME_POINT", "RISK", "GAP", "TODO", "VIEW", "CONSUMER", "PRODUCER"}
if not node_types.issubset(allowed_node_types):
    unknown = node_types - allowed_node_types
    validation_errors.append(f"Unknown node types: {unknown}")

allowed_edge_types = {"HAS_BRANCH", "HAS_GO", "HAS_DOC", "DOCUMENTS", "BELONGS_TO",
    "DEPENDS_ON", "IMPLEMENTS", "RUNS_ON", "VALIDATES", "HAS_DECISION", "HAS_INVARIANT",
    "HAS_GAP", "HAS_TODO", "RESUMES_AT", "SUPERSEDES", "REFERENCES", "CONSUMES",
    "PRODUCES", "BLOCKS", "DERIVED_FROM"}
edge_types_in = {e["type"] for e in edges}
if not edge_types_in.issubset(allowed_edge_types):
    unknown = edge_types_in - allowed_edge_types
    validation_errors.append(f"Unknown edge types: {unknown}")

# Check no secrets in source_paths
for n in nodes:
    sp = n.get("source_path", "") or ""
    if any(x in sp.lower() for x in [".env", "secret", "token", "credential", "password"]):
        validation_errors.append(f"Potential secret in node path: {sp}")

# ─── STEP 8: EXPORT ───
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
    "views": [
        {"name": "GO_MAP", "description": "All GO nodes with status"},
        {"name": "DOC_CANON_MAP", "description": "Document nodes by source_kind"},
        {"name": "MODULE_SURFACE_MAP", "description": "Modules with status and scripts"},
        {"name": "MACHINE_RUNTIME_MAP", "description": "Machines"},
        {"name": "BRANCH_WORK_MAP", "description": "Branch nodes"},
        {"name": "RESUME_MAP", "description": "Resume points"},
        {"name": "RISK_GAP_MAP", "description": "GAPs and RISKs"},
        {"name": "PRODUCER_CONSUMER_MAP", "description": "Producer -> graph bundle"},
    ],
    "validation": {
        "errors": validation_errors,
        "valid": len(validation_errors) == 0,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "go_count": len(go_nodes),
        "module_count": len([n for n in nodes if n["type"] == "MODULE"]),
        "branch_count": len([n for n in nodes if n["type"] == "BRANCH"]),
    },
    "provenance": {
        "generated_by": "producer_repo_kg_v1.py",
        "generated_at": now_iso(),
        "source_repo": "magikgmo4-ui/opt-trading",
        "source_branch": "go/GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01",
    },
}

output_path = ROOT / "graph_bundle.json"
output_path.write_text(json.dumps(graph_bundle, indent=2, ensure_ascii=False, default=safe_json))

print(f"graph_bundle.json generated:")
print(f"  Nodes: {len(nodes)}")
print(f"  Edges: {len(edges)}")
print(f"  GOs: {len(go_nodes)}")
print(f"  Modules: {len([n for n in nodes if n['type']=='MODULE'])}")
print(f"  Branches: {len([n for n in nodes if n['type']=='BRANCH'])}")
print(f"  Validation errors: {len(validation_errors)}")
print(f"  File: {output_path}")
if validation_errors:
    for e in validation_errors:
        print(f"    ERR: {e}")
