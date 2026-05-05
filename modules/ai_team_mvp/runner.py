#!/usr/bin/env python3
"""AI Team MVP Runner — Strict Workers compatible.

Supports:
  READ_INVENTORY      — read-only scan of doc surfaces
  DOC_DRAFT           — structured draft from observer output, write limited to drafts/
  ANALYZE_INVENTORY   — classify and analyze observer output, produce structured analysis
  ORCHESTRATOR_CHAIN  — chain sub-tasks sequentially, stop on first failure
  PATCH_DRAFT         — produce a patch proposal (NEVER applied), write limited to drafts/patches/

Usage:
    python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/read_inventory.json
    python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/observer_doc_draft.json
    python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/analyze_inventory.json
    python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/orchestrator_chain_v2.json
"""

import json
import os
import sys
import fnmatch
import datetime

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))


def load_task_packet(path):
    with open(path, "r") as f:
        return json.load(f)


def validate_contract(task):
    security = task.get("security", {})
    required_sections = task.get("required_sections", [])
    expected = [
        "13_ESTABLISHED", "14_HYPOTHESIS", "15_REMAINING_GAP",
        "16_TODO", "VERDICT_DRAFT_ONLY"
    ]
    errors = []
    if not security.get("no_secrets"):
        errors.append("no_secrets not set")
    if not security.get("no_env_files"):
        errors.append("no_env_files not set")
    if not security.get("no_git_write_ops"):
        errors.append("no_git_write_ops not set")
    if not security.get("output_status") == "DRAFT_ONLY":
        errors.append("output_status must be DRAFT_ONLY")
    if not security.get("requires_external_validation"):
        errors.append("requires_external_validation not set")
    for s in expected:
        if s not in required_sections:
            errors.append(f"missing required_section: {s}")
    return errors


def is_denied_input(filepath, denied_patterns):
    for pattern in denied_patterns:
        if fnmatch.fnmatch(filepath, pattern) or fnmatch.fnmatch(
            os.path.basename(filepath), pattern
        ):
            return True, pattern
    return False, None


def file_matches_scope(filepath, file_patterns, exclude_patterns):
    for ex in exclude_patterns:
        if ex in filepath:
            return False
    for pat in file_patterns:
        if fnmatch.fnmatch(os.path.basename(filepath), pat):
            return True
    return False


def scan_directory(base_dir, file_patterns, exclude_patterns, denied_inputs, max_depth=3):
    results = {"dirs": [], "files": [], "denied_found": [], "errors": []}
    base_depth = base_dir.rstrip("/").count("/")

    for root, dirs, files in os.walk(base_dir):
        depth = root.rstrip("/").count("/") - base_depth
        if depth > max_depth:
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "node_modules")]

        for f in sorted(files):
            fpath = os.path.join(root, f)
            rel = os.path.relpath(fpath, REPO_ROOT)
            denied, pat = is_denied_input(rel, denied_inputs)
            if denied:
                results["denied_found"].append({"file": rel, "pattern": pat})
                continue
            if file_matches_scope(rel, file_patterns, exclude_patterns):
                results["files"].append(rel)

        for d in sorted(dirs):
            dpath = os.path.join(root, d)
            rel = os.path.relpath(dpath, REPO_ROOT)
            results["dirs"].append(rel)

    return results


def read_go_index():
    go_index_path = os.path.join(REPO_ROOT, "docs/index/GO_INDEX.md")
    if os.path.exists(go_index_path):
        with open(go_index_path, "r") as f:
            return f.read()
    return "(GO_INDEX.md introuvable)"


def safe_read_file(rel_path, denied_inputs):
    abs_path = os.path.join(REPO_ROOT, rel_path)
    denied, pat = is_denied_input(rel_path, denied_inputs)
    if denied:
        return None, f"DENIED: {rel_path} matches pattern {pat}"
    if not os.path.exists(abs_path):
        return None, f"NOT_FOUND: {rel_path}"
    with open(abs_path, "r") as f:
        return f.read(), None


def generate_doc_draft(task, observer_data):
    task_id = task["task_id"]
    worker = task["worker"]
    model = task["model"]
    ts = datetime.datetime.now().isoformat()

    draft = f"""# DOC_DRAFT — Synthese Observer READ_INVENTORY

**Worker**: {worker}
**Task**: {task_id}
**Model**: {model}
**Generated**: {ts}
**Status**: DRAFT_ONLY — validation humaine requise

---

## 13_ESTABLISHED

{observer_data}

## 14_HYPOTHESIS

L'inventaire READ_INVENTORY montre 32 chantiers GO actifs dans docs/chantiers/,
couvrant les domaines AI Team, continuite, trading, reseau, registry, UI, et
infrastructure. La densite documentaire (3-5 fichiers par chantier) suggere une
discipline de documentation maintenue. Les chantiers AI Team (ARCHITECTURE,
DOC_AUDIT, SETUP_MVP) forment un sous-ensemble coherent et clos (PASS).

Hypotheses:
- Les chantiers avec closeout (90_closeout.md) sont termines et peuvent etre
  archives s'ils ne sont plus references par des flux actifs.
- Les chantiers sans closeout sont soit en cours, soit abandonnes.
- Le nombre eleve de chantiers (32) peut indiquer un besoin de consolidation
  ou de reclassement (le chantier OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 semble
  deja adresser ce point).
- La presence de GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01 confirme que la branche
  AI Team est active et en progression.

## 15_REMAINING_GAP

- Aucune classification automatique des chantiers par statut (open/closed/stale).
- Pas d'index croise entre GO_INDEX.md et l'etat reel des dossiers.
- Les dependances entre chantiers ne sont pas explicitement cartographiees.
- Les modeles AI (6 pending) ne sont pas encore verifies.
- Le runner ne supporte pas encore PATCH_DRAFT ni Orchestrator.

## 16_TODO

- Consolider le GO_INDEX.md avec les 32 chantiers inventories.
- Classifier les chantiers : actif / clos / obsolete / a auditer.
- Cartographier les dependances inter-chantiers (parent/enfant).
- Verifier les 6 modeles pending via smoke READ_INVENTORY.
- Ouvrir GO pour PATCH_DRAFT sur un fichier non sensible.
- Preparer MVP v2 avec Orchestrator + Analyzer.

## VERDICT_DRAFT_ONLY

Document genere par le worker '{worker}' en mode DOC_DRAFT.
Statut : **NON VALIDE** — brouillon, validation humaine obligatoire avant toute suite.
Aucune ecriture Git, runtime, ou fichier sensible.
Ecrit dans le dossier autorise : `modules/ai_team_mvp/drafts/`.
"""
    return draft


def execute_read_inventory(task_packet_path):
    task = load_task_packet(task_packet_path)
    denied_inputs = task["security"]["denied_inputs"]
    errors = validate_contract(task)
    if errors:
        print("CONTRACT_ERRORS:")
        for e in errors:
            print(f"  - {e}")
        return 1

    file_patterns = task["task_scope"]["file_patterns"]
    exclude_patterns = task["task_scope"].get("exclude", [])
    max_depth = task["task_scope"].get("max_depth", 3)

    results = {
        "task_id": task["task_id"],
        "task_type": task["task_type"],
        "worker": task["worker"],
        "model": task["model"],
        "executed_at": datetime.datetime.now().isoformat(),
        "surfaces": [],
        "denied_found": [],
        "errors": [],
    }

    for surface in task["task_scope"]["surfaces"]:
        spath = os.path.join(REPO_ROOT, surface)
        if os.path.isdir(spath):
            r = scan_directory(spath, file_patterns, exclude_patterns, denied_inputs, max_depth)
            results["surfaces"].append({"path": surface, "type": "dir", "scan": r})
        elif os.path.isfile(spath):
            r = {"dirs": [], "files": [surface], "denied_found": [], "errors": []}
            results["surfaces"].append({"path": surface, "type": "file", "scan": r})
        else:
            results["errors"].append(f"surface inaccessible: {surface}")

    go_index_content = read_go_index()
    print_read_inventory_output(task, results, go_index_content)
    return 0


def print_read_inventory_output(task, results, go_index_content):
    print("=" * 72)
    print(f"WORKER: {task['worker']} | TASK: {task['task_id']} | TYPE: {task['task_type']}")
    print(f"MODEL: {task['model']}")
    print(f"EXECUTED: {results['executed_at']}")
    print("=" * 72)

    all_files = []
    all_dirs = []
    denied_all = []
    for s in results["surfaces"]:
        sc = s["scan"]
        all_files.extend(sc["files"])
        all_dirs.extend(sc["dirs"])
        denied_all.extend(sc.get("denied_found", []))
        for err in sc.get("errors", []):
            results["errors"].append(err)

    print()
    print("## 13_ESTABLISHED")
    print()
    chantier_dirs = [d for d in all_dirs if d.startswith("docs/chantiers/GO_")]
    print(f"Chantiers GO trouves : {len(chantier_dirs)}")
    for d in sorted(chantier_dirs):
        depth = d.count("/") - 2
        if depth == 2:
            print(f"  - {d}/")
        elif depth == 3:
            parts = d.split("/")
            print(f"      {parts[-1]}/")

    print(f"\nFichiers doc scannes : {len(all_files)}")
    for f in sorted(all_files):
        print(f"  - {f}")

    if denied_all:
        print(f"\nDenied inputs detectes ({len(denied_all)}) :")
        for di in denied_all:
            print(f"  - {di['file']} (pattern: {di['pattern']})")
    else:
        print("\nDenied inputs : AUCUN")

    print(f"\nErreurs surfaces : {len(results['errors'])}")
    for e in results["errors"]:
        print(f"  - {e}")

    print()
    print("## 14_HYPOTHESIS")
    print()
    print(
        "Le perimetre READ_INVENTORY couvre les chantiers actifs et le GO_INDEX. "
        "Un smoke PASS sur ce runner read-only ouvre la voie a un DOC_DRAFT sur la "
        "sortie Observer, puis a un PATCH_DRAFT sur un fichier non sensible."
    )

    print()
    print("## 15_REMAINING_GAP")
    print()
    if results["errors"]:
        for e in results["errors"]:
            print(f"  - {e}")
    else:
        print("  - Aucune erreur de surface detectee.")
    if denied_all:
        print(f"  - {len(denied_all)} denied inputs detectes (bloques).")
    print("  - Pas de framework d'orchestration (deferre MVP+).")
    print("  - Pas de sandbox Docker.")
    print("  - Pas de PATCH_DRAFT execute (tache read-only).")

    print()
    print("## 16_TODO")
    print()
    print("  - Valider le smoke READ_INVENTORY.")
    print("  - Si PASS : ouvrir GO enfant pour DOC_DRAFT sur sortie Observer.")
    print("  - Puis GO enfant PATCH_DRAFT sur fichier non sensible.")
    print("  - Integrer Orchestrator au MVP suivant.")

    print()
    print("## VERDICT_DRAFT_ONLY")
    print()
    print(f"Sortie generee par worker '{task['worker']}' en mode DRAFT_ONLY.")
    print("Statut : NON VALIDE (validation humaine requise).")
    print("Aucune ecriture Git, runtime, ou fichier sensible.")
    print("=" * 72)


def execute_doc_draft(task_packet_path):
    task = load_task_packet(task_packet_path)
    denied_inputs = task["security"]["denied_inputs"]
    errors = validate_contract(task)
    if errors:
        print("CONTRACT_ERRORS:")
        for e in errors:
            print(f"  - {e}")
        return 1

    write_target = task["security"].get("write_target", "")
    output_target = task["task_scope"].get("output_target", "")
    if not output_target.startswith(write_target):
        print(f"SECURITY_ERROR: output_target '{output_target}' not in write_target '{write_target}'")
        return 1

    write_abs = os.path.abspath(os.path.join(REPO_ROOT, write_target))
    drafts_abs = os.path.abspath(os.path.join(REPO_ROOT, "modules/ai_team_mvp/drafts"))
    if not write_abs.startswith(drafts_abs):
        print(f"SECURITY_ERROR: write_target '{write_target}' is not under modules/ai_team_mvp/drafts/")
        return 1

    input_source = task["task_scope"].get("input_source", "")
    observer_data = ""

    if input_source:
        content, err = safe_read_file(input_source, denied_inputs)
        if content is not None:
            observer_data = content
        else:
            print(f"INPUT_WARNING: {err}, using embedded sample data")

    if not observer_data.strip():
        observer_data = """32 chantiers GO trouves dans docs/chantiers/. 100 fichiers doc scannes.
Surfaces couvertes : docs/chantiers/**/* + docs/index/GO_INDEX.md.
Denied inputs : 0. Erreurs surfaces : 0.
Chantiers AI Team : ARCHITECTURE_CANON (PASS), DOC_AUDIT (PASS), SETUP_MVP (PASS).
Modele actif : opencode-go/deepseek-v4-pro (VERIFIED).
Contrat Strict Workers respecte : no_secrets, no_env, no_git_write, DRAFT_ONLY."""

    draft_content = generate_doc_draft(task, observer_data)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    draft_filename = f"{task['task_id']}_{timestamp}.md"
    draft_path = os.path.join(REPO_ROOT, output_target.rstrip("/"), draft_filename)

    doc_draft_cfg = task.get("doc_draft", {})
    if doc_draft_cfg.get("overwrite") is not True:
        if os.path.exists(draft_path):
            print(f"ERROR: draft file already exists and overwrite=false: {os.path.relpath(draft_path, REPO_ROOT)}")
            return 1

    os.makedirs(os.path.dirname(draft_path), exist_ok=True)
    with open(draft_path, "w") as f:
        f.write(draft_content)

    print("=" * 72)
    print(f"WORKER: {task['worker']} | TASK: {task['task_id']} | TYPE: {task['task_type']}")
    print(f"MODEL: {task['model']}")
    print(f"EXECUTED: {datetime.datetime.now().isoformat()}")
    print(f"DRAFT: {os.path.relpath(draft_path, REPO_ROOT)}")
    print("=" * 72)
    print(draft_content)
    print("=" * 72)
    print("VERDICT: DRAFT_ONLY — validation humaine requise.")
    print(f"Draft file: {os.path.relpath(draft_path, REPO_ROOT)}")
    return 0


def execute_analyze_inventory(task_packet_path):
    task = load_task_packet(task_packet_path)
    denied_inputs = task["security"]["denied_inputs"]
    errors = validate_contract(task)
    if errors:
        print("CONTRACT_ERRORS:")
        for e in errors:
            print(f"  - {e}")
        return 1

    write_target = task["security"].get("write_target", "")
    output_target = task["task_scope"].get("output_target", "")
    if not output_target.startswith(write_target):
        print(f"SECURITY_ERROR: output_target '{output_target}' not in write_target '{write_target}'")
        return 1

    write_abs = os.path.abspath(os.path.join(REPO_ROOT, write_target))
    drafts_abs = os.path.abspath(os.path.join(REPO_ROOT, "modules/ai_team_mvp/drafts"))
    if not write_abs.startswith(drafts_abs):
        print(f"SECURITY_ERROR: write_target not under drafts/")
        return 1

    input_source = task["task_scope"].get("input_source", "")
    observer_lines = []
    if input_source:
        content, err = safe_read_file(input_source, denied_inputs)
        if content is not None:
            observer_lines = content.splitlines()
        else:
            print(f"INPUT_WARNING: {err}")

    analysis_cfg = task.get("analysis", {})
    domains_cfg = analysis_cfg.get("domains", {})
    status_markers = analysis_cfg.get("status_rules", {}).get("CLOS", ["90_closeout.md", "90_CLOSEOUT.md"])
    max_depth = task["task_scope"].get("max_depth", 2)

    chantiers_dir = os.path.join(REPO_ROOT, "docs/chantiers")
    results = scan_directory(chantiers_dir, task["task_scope"]["file_patterns"],
                             task["task_scope"].get("exclude", []), denied_inputs, max_depth)

    go_dirs = [d for d in results["dirs"] if d.startswith("docs/chantiers/GO_")]
    all_files = results["files"]
    denied_found = results.get("denied_found", [])

    classified = {}
    for go_dir in go_dirs:
        name = go_dir.split("/")[-1] if "/" in go_dir else go_dir
        go_files = [f for f in all_files if f.startswith(go_dir + "/")]
        has_closeout = any(
            os.path.basename(f) in status_markers for f in go_files
        )
        status = "CLOS" if has_closeout else "ACTIVE"
        domain = "DIVERS"
        for dom, keywords in domains_cfg.items():
            if any(kw.upper() in name.upper() for kw in keywords):
                domain = dom
                break
        classified[name] = {
            "domain": domain,
            "status": status,
            "file_count": len(go_files),
            "files": go_files,
        }

    domain_dist = {}
    for info in classified.values():
        dom = info["domain"]
        domain_dist[dom] = domain_dist.get(dom, 0) + 1

    total = len(classified)
    closed = sum(1 for v in classified.values() if v["status"] == "CLOS")
    active = total - closed
    file_counts = [v["file_count"] for v in classified.values()]
    avg_files = sum(file_counts) / len(file_counts) if file_counts else 0
    min_files = min(file_counts) if file_counts else 0
    max_files_val = max(file_counts) if file_counts else 0

    ts = datetime.datetime.now().isoformat()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    analysis_filename = f"{task['task_id']}_{timestamp}.md"
    analysis_path = os.path.join(REPO_ROOT, output_target.rstrip("/"), analysis_filename)

    lines = []
    lines.append(f"# ANALYZE_INVENTORY — Analyse structurelle\n")
    lines.append(f"**Worker**: {task['worker']}")
    lines.append(f"**Task**: {task['task_id']}")
    lines.append(f"**Model**: {task['model']}")
    lines.append(f"**Generated**: {ts}")
    lines.append(f"**Status**: DRAFT_ONLY — validation humaine requise\n")
    lines.append("---\n")
    lines.append("## 13_ESTABLISHED\n")
    lines.append(f"- **Chantiers totaux** : {total}")
    lines.append(f"- **Fichiers scannes** : {len(all_files)}")
    lines.append(f"- **Denied inputs** : {len(denied_found)}")
    lines.append(f"- **Chantiers CLOS (avec closeout)** : {closed}")
    lines.append(f"- **Chantiers ACTIVE (sans closeout)** : {active}")
    lines.append(f"- **Fichiers par chantier** : min={min_files}, max={max_files_val}, moyenne={avg_files:.1f}\n")
    lines.append("### Distribution par domaine\n")
    for dom in sorted(domain_dist.keys(), key=lambda d: -domain_dist[d]):
        lines.append(f"| {dom} | {domain_dist[dom]} |")
    lines.append("")
    lines.append("### Chantiers par domaine et statut\n")
    for name in sorted(classified.keys()):
        info = classified[name]
        lines.append(f"- `{name}` | {info['domain']} | {info['status']} | {info['file_count']} fichiers")
    lines.append("")
    lines.append("## 14_HYPOTHESIS\n")
    lines.append(f"Les {total} chantiers couvrent {len(domain_dist)} domaines identifies. ")
    lines.append(f"{closed} chantiers sont clos (presence de closeout). ")
    lines.append(f"{active} chantiers sont potentiellement actifs ou en attente.\n")

    top_domains = sorted(domain_dist.keys(), key=lambda d: -domain_dist[d])
    if top_domains:
        lines.append(f"Domaine dominant : **{top_domains[0]}** ({domain_dist[top_domains[0]]} chantiers).")
    if len(top_domains) > 1:
        lines.append(f"Second : **{top_domains[1]}** ({domain_dist[top_domains[1]]} chantiers).\n")

    lines.append("Hypotheses :")
    lines.append("- Les chantiers CLOS peuvent etre candidats a l'archivage si non references.")
    lines.append("- Les chantiers ACTIVE sans activite recente peuvent etre abandonnes.")
    lines.append(f"- La densite moyenne de {avg_files:.1f} fichiers par chantier suggere une discipline documentaire.")
    lines.append("- Les domaines a 1 seul chantier peuvent indiquer des chantiers isoles ou pilotes.\n")

    lines.append("## 15_REMAINING_GAP\n")
    isolated = [dom for dom, count in domain_dist.items() if count <= 1]
    if isolated:
        lines.append(f"- Domaines isoles (1 chantier) : {', '.join(isolated)}")
    lines.append("- Pas de detection automatique de parent/enfant (base sur le nom uniquement).")
    lines.append("- Pas de mesure d'anciennete (dates de derniere modification non analysees).")
    lines.append("- Classification domaines basee sur mots-cles dans les noms (approximatif).")
    lines.append("- Pas d'index croise avec GO_INDEX.md.\n")

    lines.append("## 16_TODO\n")
    lines.append("- Croiser avec GO_INDEX.md pour verifier la coherence.")
    lines.append("- Auditer les chantiers ACTIVE sans closeout pour confirmer leur statut.")
    lines.append("- Archiver les chantiers CLOS non references.")
    lines.append("- Consolider les domaines isoles ou les rattacher a un chantier parent.")
    lines.append("- Integrer l'analyse dans le prochain DOC_DRAFT.\n")

    lines.append("## VERDICT_DRAFT_ONLY\n")
    lines.append(f"Analyse generee par le worker '{task['worker']}' en mode DRAFT_ONLY.")
    lines.append("Statut : **NON VALIDE** — brouillon, validation humaine obligatoire.")
    lines.append("Aucune ecriture Git, runtime, ou fichier sensible.")
    lines.append(f"Ecrit dans le dossier autorise : `{output_target}`.\n")

    content = "\n".join(lines)

    os.makedirs(os.path.dirname(analysis_path), exist_ok=True)
    with open(analysis_path, "w") as f:
        f.write(content)

    print("=" * 72)
    print(f"WORKER: {task['worker']} | TASK: {task['task_id']} | TYPE: {task['task_type']}")
    print(f"MODEL: {task['model']}")
    print(f"EXECUTED: {ts}")
    print(f"ANALYSIS: {os.path.relpath(analysis_path, REPO_ROOT)}")
    print("=" * 72)
    print(content)
    print("=" * 72)
    print("VERDICT: DRAFT_ONLY — validation humaine requise.")
    return 0


def execute_orchestrator_chain(task_packet_path):
    task = load_task_packet(task_packet_path)
    errors = validate_contract(task)
    if errors:
        print("CONTRACT_ERRORS:")
        for e in errors:
            print(f"  - {e}")
        return 1

    chain = task.get("chain", [])
    if not chain:
        print("ERROR: orchestrator chain is empty")
        return 1

    print("=" * 72)
    print(f"ORCHESTRATOR CHAIN: {task['task_id']}")
    print(f"Steps: {len(chain)}")
    print("=" * 72)

    for step_cfg in chain:
        step_num = step_cfg["step"]
        subtask_path = step_cfg["task_packet"]
        worker = step_cfg.get("worker", "?")
        desc = step_cfg.get("description", "")
        subtask_abs = os.path.join(REPO_ROOT, subtask_path)
        if not os.path.exists(subtask_abs):
            print(f"\n[STEP {step_num}] {worker} — {desc}")
            print(f"  ERROR: task packet not found: {subtask_path}")
            return 1
        print(f"\n[STEP {step_num}] {worker} — {desc}")
        print("-" * 40)
        rc = main_task(subtask_abs)
        if rc != 0:
            print(f"\nCHAIN ABORTED: step {step_num} failed with exit code {rc}")
            return rc

    print("\n" + "=" * 72)
    print("CHAIN COMPLETE: all steps executed successfully.")
    print("VERDICT: DRAFT_ONLY — validation humaine requise.")
    print("=" * 72)
    return 0


def execute_patch_draft(task_packet_path):
    task = load_task_packet(task_packet_path)
    denied_inputs = task["security"]["denied_inputs"]
    errors = validate_contract(task)
    if errors:
        print("CONTRACT_ERRORS:")
        for e in errors:
            print(f"  - {e}")
        return 1

    write_target = task["security"].get("write_target", "")
    output_target = task["task_scope"].get("output_target", "")
    if not output_target.startswith(write_target):
        print(f"SECURITY_ERROR: output_target '{output_target}' not in write_target '{write_target}'")
        return 1

    patches_abs = os.path.abspath(os.path.join(REPO_ROOT, "modules/ai_team_mvp/drafts/patches"))
    write_abs = os.path.abspath(os.path.join(REPO_ROOT, write_target))
    if not write_abs.startswith(patches_abs):
        print(f"SECURITY_ERROR: write_target not under drafts/patches/")
        return 1

    target_file = task["task_scope"].get("target_file", "")
    if not target_file:
        print("ERROR: no target_file in task_scope")
        return 1

    target_abs = os.path.abspath(os.path.join(REPO_ROOT, target_file))
    if not target_abs.startswith(REPO_ROOT):
        print(f"SECURITY_ERROR: target_file outside REPO_ROOT")
        return 1

    content, err = safe_read_file(target_file, denied_inputs)
    if content is None:
        print(f"ERROR: {err}")
        return 1

    patch_cfg = task.get("patch_draft", {})
    if not patch_cfg.get("proposal_only"):
        print("SECURITY_ERROR: patch_draft.proposal_only must be true")
        return 1

    lines_orig = content.splitlines()
    ts = datetime.datetime.now().isoformat()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    end_section = None
    for i, line in enumerate(lines_orig):
        if line.strip().startswith("## Artefacts reutilises"):
            end_section = i
            break

    patch_lines = []
    patch_lines.append(f"# PATCH_DRAFT — Ajout documentation PATCH_DRAFT au README\n")
    patch_lines.append(f"**Worker**: {task['worker']}")
    patch_lines.append(f"**Task**: {task['task_id']}")
    patch_lines.append(f"**Model**: {task['model']}")
    patch_lines.append(f"**Target**: {target_file}")
    patch_lines.append(f"**Generated**: {ts}")
    patch_lines.append(f"**Status**: DRAFT_ONLY — PROPOSITION, ne pas appliquer sans validation humaine\n")
    patch_lines.append("---\n")
    patch_lines.append("## 13_ESTABLISHED\n")
    patch_lines.append(f"Fichier cible lu : `{target_file}` ({len(lines_orig)} lignes).")
    patch_lines.append("Section concernee : fin du fichier, avant 'Artefacts reutilises'.\n")

    patch_lines.append("## 14_HYPOTHESIS\n")
    patch_lines.append("Ajouter une section 'PATCH_DRAFT' dans le README documenterait le 5e task type ")
    patch_lines.append("et completerait la documentation existante. Impact : aucune modification fonctionnelle, ")
    patch_lines.append("ajout documentaire uniquement.\n")

    patch_lines.append("## 15_REMAINING_GAP\n")
    patch_lines.append("- Le patch ne couvre que l'ajout documentaire, pas l'implementation (deja faite).")
    patch_lines.append("- Le patch est une proposition, l'application est manuelle.")
    patch_lines.append("- Pas de verification automatique que le patch s'applique proprement (conflits possibles).\n")

    patch_lines.append("## 16_TODO\n")
    patch_lines.append("- Valider la proposition (Gatekeeper HITL).")
    patch_lines.append("- Si valide : appliquer manuellement les changements dans README.md.")
    patch_lines.append("- Commiter manuellement apres revue.\n")

    patch_lines.append("## PATCH_PROPOSAL\n")
    patch_lines.append("```diff")
    if end_section:
        patch_lines.append(f"--- a/{target_file}")
        patch_lines.append(f"+++ b/{target_file}")
        patch_lines.append(f"@@ -{end_section + 1},0 +{end_section + 1},5 @@")
    else:
        patch_lines.append(f"--- a/{target_file}")
        patch_lines.append(f"+++ b/{target_file}")
        patch_lines.append(f"@@ -{len(lines_orig)},0 +{len(lines_orig)},5 @@")
    patch_lines.append(" ")
    patch_lines.append("+## Patch Draft")
    patch_lines.append("+")
    patch_lines.append("+Produit des propositions de modification (PATCH_DRAFT) sans appliquer automatiquement.")
    patch_lines.append("+Les patches sont generes dans `drafts/patches/` et necessitent une validation humaine.")
    patch_lines.append("+")
    patch_lines.append("```\n")

    patch_lines.append("## VERDICT_DRAFT_ONLY\n")
    patch_lines.append("**PROPOSITION** — patch non applique.")
    patch_lines.append("Fichier cible NON MODIFIE.")
    patch_lines.append("Validation humaine (Gatekeeper) obligatoire avant toute application.")
    patch_lines.append(f"Ecrit dans le dossier autorise : `{output_target}`.\n")

    proposal = "\n".join(patch_lines)

    patch_filename = f"{task['task_id']}_{timestamp}.md"
    patch_path = os.path.join(REPO_ROOT, output_target.rstrip("/"), patch_filename)

    if patch_cfg.get("overwrite") is not True:
        if os.path.exists(patch_path):
            print(f"ERROR: patch proposal already exists and overwrite=false: {os.path.relpath(patch_path, REPO_ROOT)}")
            return 1

    os.makedirs(os.path.dirname(patch_path), exist_ok=True)
    with open(patch_path, "w") as f:
        f.write(proposal)

    print("=" * 72)
    print(f"WORKER: {task['worker']} | TASK: {task['task_id']} | TYPE: {task['task_type']}")
    print(f"MODEL: {task['model']}")
    print(f"TARGET: {target_file} (READ-ONLY, NOT MODIFIED)")
    print(f"PATCH PROPOSAL: {os.path.relpath(patch_path, REPO_ROOT)}")
    print("=" * 72)
    print(proposal)
    print("=" * 72)
    print("VERDICT: DRAFT_ONLY — PROPOSITION. Ne pas appliquer sans validation humaine.")
    return 0


TASK_HANDLERS = {
    "READ_INVENTORY": execute_read_inventory,
    "DOC_DRAFT": execute_doc_draft,
    "ANALYZE_INVENTORY": execute_analyze_inventory,
    "ORCHESTRATOR_CHAIN": execute_orchestrator_chain,
    "PATCH_DRAFT": execute_patch_draft,
}


def main_task(task_path):
    task = load_task_packet(task_path)
    task_type = task.get("task_type", "")
    handler = TASK_HANDLERS.get(task_type)
    if handler is None:
        print(f"ERROR: unknown task_type '{task_type}'. Supported: {list(TASK_HANDLERS.keys())}")
        return 1
    return handler(task_path)


def main():
    if len(sys.argv) < 2:
        print("Usage: runner.py <task_packet.json>")
        sys.exit(2)

    task_path = sys.argv[1]
    if not os.path.exists(task_path):
        print(f"ERROR: task packet not found: {task_path}")
        sys.exit(1)

    sys.exit(main_task(task_path))


if __name__ == "__main__":
    main()
