#!/usr/bin/env python3
from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import os
import re
import shlex
import socket
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

DEFAULT_BRANCH = "origin/sot/mainline"
DEFAULT_REPO_PATH = "/opt/trading"

ARTEFACT_PATTERNS = [
    re.compile(r"(^|/)(__pycache__|\.pytest_cache|\.mypy_cache|tmp|logs)(/|$)"),
    re.compile(r"\.(pyc|pyo|tmp|log|swp|swo|sqlite-shm|sqlite-wal|db-shm|db-wal)$"),
    re.compile(r"\.bak(_.*)?$"),
    re.compile(r"(^|/)\.DS_Store$"),
]
USEFUL_PATTERNS = [
    re.compile(r"(^|/)(modules|docs|scripts|config|journal)(/|$)"),
    re.compile(r"\.(py|sh|md|txt|json|ya?ml|toml|ini|cfg)$"),
]


@dataclasses.dataclass
class Machine:
    name: str
    ssh_target: str
    repo_path: str = DEFAULT_REPO_PATH
    local_names: Tuple[str, ...] = ()

    def is_local(self) -> bool:
        current = {
            socket.gethostname(),
            socket.getfqdn(),
            os.environ.get("HOSTNAME", ""),
            "localhost",
            "127.0.0.1",
            "local",
        }
        current = {x for x in current if x}
        current.update(self.local_names)
        return self.name in current or self.ssh_target in current


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def default_module_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_reports_dir(module_root: Path) -> Path:
    return module_root / "reports"


def load_config(path: Optional[Path]) -> Dict[str, Any]:
    if path and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    module_root = default_module_root()
    cfg = module_root / "config" / "machines.default.json"
    if cfg.exists():
        return json.loads(cfg.read_text(encoding="utf-8"))
    return {"machines": []}


def normalize_machine(spec: Dict[str, Any]) -> Machine:
    return Machine(
        name=spec["name"],
        ssh_target=spec.get("ssh_target", spec["name"]),
        repo_path=spec.get("repo_path", DEFAULT_REPO_PATH),
        local_names=tuple(spec.get("local_names", [])),
    )


def resolve_machines(config: Dict[str, Any], raw: Optional[str]) -> List[Machine]:
    machines = [normalize_machine(x) for x in config.get("machines", [])]
    by_name = {m.name: m for m in machines}
    if not raw:
        return machines
    result: List[Machine] = []
    for token in [x.strip() for x in raw.split(",") if x.strip()]:
        if token in by_name:
            result.append(by_name[token])
        else:
            result.append(Machine(name=token, ssh_target=token))
    return result


def run_local(cmd: List[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)


def run_remote(ssh_target: str, remote_cmd: str) -> subprocess.CompletedProcess[str]:
    cmd = [
        "ssh",
        "-o", "BatchMode=yes",
        "-o", "ConnectTimeout=5",
        "-o", "StrictHostKeyChecking=accept-new",
        ssh_target,
        remote_cmd,
    ]
    return subprocess.run(cmd, text=True, capture_output=True)


def shell_join(parts: Iterable[str]) -> str:
    return " ".join(shlex.quote(p) for p in parts)


def git_cmd(repo_path: str, args: List[str]) -> str:
    return f"cd {shlex.quote(repo_path)} && {shell_join(['git', *args])}"


def parse_porcelain(output: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for raw in output.splitlines():
        if not raw.strip():
            continue
        status = raw[:2]
        path = raw[3:]
        if " -> " in path:
            _, path = path.split(" -> ", 1)
        rows.append({"status": status, "path": path})
    return rows


def classify_path(path: str) -> str:
    for pat in ARTEFACT_PATTERNS:
        if pat.search(path):
            return "artefact_probable"
    for pat in USEFUL_PATTERNS:
        if pat.search(path):
            return "utile_probable"
    return "ambigu"


def classify_changes(rows: List[Dict[str, str]]) -> Dict[str, List[str]]:
    out = {
        "utile_probable": [],
        "artefact_probable": [],
        "ambigu": [],
        "propre": [],
    }
    if not rows:
        out["propre"] = ["working_tree_clean"]
        return out
    for row in rows:
        out[classify_path(row["path"])].append(f'{row["status"]} {row["path"]}')
    return out


def inspect_machine(machine: Machine, remote_branch: str, do_fetch: bool) -> Dict[str, Any]:
    branch_name_expected = remote_branch.split("/", 1)[1] if "/" in remote_branch else remote_branch
    result: Dict[str, Any] = {
        "machine": machine.name,
        "ssh_target": machine.ssh_target,
        "repo_path": machine.repo_path,
        "mode": "local" if machine.is_local() else "ssh",
        "reachable": False,
        "repo_exists": False,
        "fetch_attempted": do_fetch,
        "remote_branch_expected": remote_branch,
        "branch_name_expected": branch_name_expected,
    }

    if machine.is_local():
        probe = run_local(["bash", "-lc", f'test -d {shlex.quote(machine.repo_path)}'])
    else:
        probe = run_remote(machine.ssh_target, f'test -d {shlex.quote(machine.repo_path)}')
    result["reachable"] = probe.returncode == 0
    if probe.returncode != 0:
        result["status"] = "inaccessible"
        result["reasons"] = ["repo_or_host_inaccessible"]
        result["probe_stderr"] = probe.stderr.strip()
        return result

    result["repo_exists"] = True

    def do(cmd: str) -> subprocess.CompletedProcess[str]:
        if machine.is_local():
            return run_local(["bash", "-lc", cmd])
        return run_remote(machine.ssh_target, cmd)

    cmds = {
        "toplevel": git_cmd(machine.repo_path, ["rev-parse", "--show-toplevel"]),
        "branch": git_cmd(machine.repo_path, ["branch", "--show-current"]),
        "remote": git_cmd(machine.repo_path, ["remote", "-v"]),
        "status_short": git_cmd(machine.repo_path, ["status", "--short"]),
        "status_sb": git_cmd(machine.repo_path, ["status", "-sb"]),
        "stash": git_cmd(machine.repo_path, ["stash", "list"]),
        "left_right": git_cmd(machine.repo_path, ["rev-list", "--left-right", "--count", f"HEAD...{remote_branch}"]),
        "left_right_log": git_cmd(machine.repo_path, ["log", "--oneline", "--decorate", "--left-right", f"HEAD...{remote_branch}", "-n", "20"]),
    }
    if do_fetch:
        fetch_res = do(git_cmd(machine.repo_path, ["fetch", "origin"]))
        result["fetch"] = {
            "returncode": fetch_res.returncode,
            "stdout": fetch_res.stdout.strip(),
            "stderr": fetch_res.stderr.strip(),
        }
    else:
        result["fetch"] = {"returncode": None, "stdout": "", "stderr": "", "skipped": True}

    outputs = {name: do(cmd) for name, cmd in cmds.items()}
    result["commands"] = {
        name: {"returncode": cp.returncode, "stdout": cp.stdout.strip(), "stderr": cp.stderr.strip()}
        for name, cp in outputs.items()
    }

    result["repo_top"] = outputs["toplevel"].stdout.strip() if outputs["toplevel"].returncode == 0 else None
    result["branch"] = outputs["branch"].stdout.strip()
    result["remote_v"] = outputs["remote"].stdout.strip().splitlines()
    result["status_short"] = parse_porcelain(outputs["status_short"].stdout)
    result["status_sb"] = outputs["status_sb"].stdout.strip()
    result["stash"] = [line for line in outputs["stash"].stdout.strip().splitlines() if line.strip()]
    result["left_right_log"] = [line for line in outputs["left_right_log"].stdout.strip().splitlines() if line.strip()]

    counts = outputs["left_right"].stdout.strip().split()
    if len(counts) == 2 and all(x.isdigit() for x in counts):
        result["ahead_of_remote"], result["behind_remote"] = [int(x) for x in counts]
    else:
        result["ahead_of_remote"] = None
        result["behind_remote"] = None

    origin_fetch_urls: List[str] = []
    origin_push_urls: List[str] = []
    for line in result["remote_v"]:
        parts = line.split()
        if len(parts) >= 3 and parts[0] == "origin":
            if parts[2] == "(fetch)":
                origin_fetch_urls.append(parts[1])
            elif parts[2] == "(push)":
                origin_push_urls.append(parts[1])
    result["origin_fetch_urls"] = origin_fetch_urls
    result["origin_push_urls"] = origin_push_urls
    result["remote_origin_present"] = bool(origin_fetch_urls or origin_push_urls)
    result["remote_origin_consistent"] = bool(origin_fetch_urls) and bool(origin_push_urls) and origin_fetch_urls == origin_push_urls
    result["branch_matches_target"] = result["branch"] == branch_name_expected
    result["remote_branch_accessible"] = outputs["left_right"].returncode == 0

    result["classification"] = classify_changes(result["status_short"])

    reasons: List[str] = []
    if outputs["toplevel"].returncode != 0:
        reasons.append("not_a_git_repo")
    if not result["remote_origin_present"]:
        reasons.append("remote_origin_missing")
    elif not result["remote_origin_consistent"]:
        reasons.append("remote_origin_inconsistent")
    if result["branch"] and not result["branch_matches_target"]:
        reasons.append("branch_differs_from_target")
    if not result["remote_branch_accessible"]:
        reasons.append("remote_branch_missing_or_unreachable")
    if result["stash"]:
        reasons.append("stash_present")
    if result["status_short"]:
        reasons.append("working_tree_dirty")
    if (result.get("ahead_of_remote") or 0) > 0:
        reasons.append("local_commits_ahead")
    if (result.get("behind_remote") or 0) > 0:
        reasons.append("behind_remote")

    if reasons:
        result["status"] = "review_required"
    else:
        result["status"] = "clean"
        result["classification"]["propre"] = ["working_tree_clean_and_synced"]
    result["reasons"] = reasons
    return result


def load_report(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def render_command_block(commands: List[str]) -> List[str]:
    lines = ["```bash"]
    lines.extend(commands)
    lines.append("```")
    return lines


def build_remediation(item: Dict[str, Any], remote_branch: str) -> Dict[str, Any]:
    machine = item["machine"]
    repo_path = item.get("repo_path") or DEFAULT_REPO_PATH
    branch = item.get("branch") or "(unknown)"
    reasons = item.get("reasons") or []
    ahead = item.get("ahead_of_remote")
    behind = item.get("behind_of_remote")
    if behind is None:
        behind = item.get("behind_remote")
    ssh_target = item.get("ssh_target", machine)

    status = item.get("status", "unknown")
    risk = "low"
    diagnostics: List[str] = []
    warnings: List[str] = []
    commands: List[str] = []
    expected: List[str] = []

    def add_cmd(cmd: str) -> None:
        remote_cmd = f"cd {shlex.quote(repo_path)} && {cmd}"
        if item.get("mode") == "local":
            commands.append(remote_cmd)
        else:
            commands.append(f"ssh {shlex.quote(ssh_target)} {shlex.quote(remote_cmd)}")

    if status == "inaccessible":
        risk = "high"
        diagnostics.append("machine ou repo inaccessible depuis ce run")
        warnings.append("aucune remédiation Git distante n'est possible tant que l'accès SSH ou le chemin repo n'est pas rétabli")
        expected.append("l'audit suivant doit passer de inaccessible a clean ou review_required")
        return {
            "machine": machine,
            "status": status,
            "risk": risk,
            "diagnostics": diagnostics,
            "commands": commands,
            "warnings": warnings,
            "expected": expected,
        }

    if "remote_origin_missing" in reasons:
        risk = "high"
        diagnostics.append("remote origin absent")
        warnings.append("ne pas ajouter ou modifier un remote sans preuve du depot canonique attendu")
        add_cmd("git remote -v")
        add_cmd(f"git remote add origin $(git remote get-url origin 2>/dev/null || printf '%s' 'https://github.com/magikgmo4-ui/opt-trading.git')")
        expected.append("origin doit apparaitre en fetch et push vers le depot canonique")

    if "remote_origin_inconsistent" in reasons:
        risk = "high"
        diagnostics.append("remote origin incoherent entre fetch et push")
        warnings.append("verifier les deux URLs avant toute correction manuelle")
        add_cmd("git remote -v")
        add_cmd("git remote set-url origin <URL_FETCH_VALIDEE>")
        add_cmd("git remote set-url --push origin <URL_PUSH_VALIDEE>")
        expected.append("fetch et push doivent pointer vers la meme cible si c'est l'intention operateur")

    if "branch_differs_from_target" in reasons:
        risk = "medium" if risk == "low" else risk
        diagnostics.append(f"branche courante differente de la cible attendue ({branch} vs {item.get('branch_name_expected')})")
        warnings.append("ne pas changer de branche sans verifier d'abord l'etat local et les travaux en cours")
        add_cmd("git branch --show-current")
        add_cmd("git status --short")
        add_cmd(f"git switch {shlex.quote(item.get('branch_name_expected') or 'sot/mainline')}")
        expected.append("la branche courante doit correspondre a la branche cible de l'audit")

    if "remote_branch_missing_or_unreachable" in reasons:
        risk = "high"
        diagnostics.append(f"branche distante {remote_branch} absente ou inaccessible")
        warnings.append("verifier d'abord la connectivite et l'existence de la branche distante avant tout pull/rebase")
        add_cmd("git remote -v")
        add_cmd("git branch -r")
        add_cmd("git ls-remote --heads origin")
        expected.append(f"{remote_branch} doit etre resoluble avant toute comparaison ahead/behind fiable")

    if "stash_present" in reasons:
        risk = "medium" if risk == "low" else risk
        diagnostics.append("stash present")
        warnings.append("ne pas pop/apply/drop un stash sans identifier son contenu et son contexte")
        add_cmd("git stash list")
        add_cmd("git stash show --stat stash@{0}")
        add_cmd("git stash show -p stash@{0}")
        expected.append("l'operateur decide explicitement si le stash doit etre conserve, applique ou exporter")

    if "working_tree_dirty" in reasons:
        risk = "medium" if risk == "low" else risk
        diagnostics.append("working tree sale")
        warnings.append("documenter les modifications avant toute action Git plus intrusive")
        add_cmd("git status --short")
        add_cmd("git diff --stat")
        add_cmd("git diff")
        expected.append("les changements locaux sont qualifies avant commit, restauration manuelle ou archivage")

    if ahead and behind:
        risk = "high"
        diagnostics.append("branche diverged")
        warnings.append("ne pas pull/rebase a l'aveugle; inspecter d'abord les deux cotes de la divergence")
        add_cmd(f"git log --oneline --left-right {shlex.quote('HEAD...'+remote_branch)} -n 20")
        add_cmd(f"git diff --stat {shlex.quote(remote_branch)}...HEAD")
        expected.append("un plan manuel de reconciliation est choisi apres inspection detaillee")
    else:
        if ahead:
            risk = "medium" if risk == "low" else risk
            diagnostics.append(f"ahead only ({ahead} commit(s))")
            warnings.append("verifier l'historique local avant push manuel")
            add_cmd("git log --oneline -n 10")
            add_cmd(f"git log --oneline {shlex.quote(remote_branch)}..HEAD")
            add_cmd(f"git push origin {shlex.quote(branch)}")
            expected.append("le remote doit rattraper les commits locaux si l'operateur confirme le push")
        if behind:
            risk = "medium" if risk == "low" else risk
            diagnostics.append(f"behind only ({behind} commit(s))")
            warnings.append("choisir explicitement entre merge et rebase selon le contexte local")
            add_cmd("git fetch origin")
            add_cmd(f"git log --oneline HEAD..{shlex.quote(remote_branch)}")
            add_cmd(f"git pull --ff-only origin {shlex.quote(item.get('branch_name_expected') or 'sot/mainline')}")
            expected.append("la branche locale doit revenir synchronisee si un fast-forward est possible")

    if not diagnostics:
        diagnostics.append("aucune remédiation nécessaire")
        expected.append("aucune action operateur requise")

    return {
        "machine": machine,
        "status": status,
        "risk": risk,
        "diagnostics": diagnostics,
        "commands": commands,
        "warnings": warnings,
        "expected": expected,
    }


def render_remediation_markdown(report: Dict[str, Any], actions: List[Dict[str, Any]]) -> str:
    lines = []
    lines.append("# git_fleet_guard guided remediation")
    lines.append("")
    lines.append(f"- Source report: `{report['generated_at_utc']}`")
    lines.append(f"- Branche cible: `{report['remote_branch']}`")
    lines.append("- Mode: `guided only` (aucune commande Git n'est executee automatiquement)")
    lines.append("")
    for item in actions:
        lines.append(f"## {item['machine']}")
        lines.append("")
        lines.append(f"- Statut: `{item['status']}`")
        lines.append(f"- Risque: `{item['risk']}`")
        lines.append(f"- Diagnostic: `{'; '.join(item['diagnostics'])}`")
        lines.append("")
        lines.append("### Commandes recommandées")
        lines.append("")
        if item["commands"]:
            lines.extend(render_command_block(item["commands"]))
        else:
            lines.append("_Aucune commande recommandee depuis ce run._")
        lines.append("")
        lines.append("### Avertissements")
        lines.append("")
        if item["warnings"]:
            for warning in item["warnings"]:
                lines.append(f"- {warning}")
        else:
            lines.append("- aucun")
        lines.append("")
        lines.append("### Résultat attendu")
        lines.append("")
        for value in item["expected"]:
            lines.append(f"- {value}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def cmd_remediate(args: argparse.Namespace) -> int:
    module_root = default_module_root()
    reports_dir = Path(args.reports_dir) if args.reports_dir else default_reports_dir(module_root)
    path = Path(args.path) if args.path else reports_dir / "latest.json"
    if not path.exists():
        print(f"Report not found: {path}", file=sys.stderr)
        return 2
    report = load_report(path)
    items = report.get("results", [])
    if args.machine:
        wanted = {x.strip() for x in args.machine.split(",") if x.strip()}
        items = [x for x in items if x.get("machine") in wanted]
    actions = [build_remediation(item, report.get("remote_branch", DEFAULT_BRANCH)) for item in items]
    payload = {
        "source_report": str(path),
        "generated_at_utc": now_utc().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "remote_branch": report.get("remote_branch", DEFAULT_BRANCH),
        "actions": actions,
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(render_remediation_markdown(report, actions))
    return 0


def render_markdown(report: Dict[str, Any]) -> str:
    lines = []
    lines.append("# git_fleet_guard audit")
    lines.append("")
    lines.append(f"- Timestamp UTC: `{report['generated_at_utc']}`")
    lines.append(f"- Repo branch cible: `{report['remote_branch']}`")
    lines.append(f"- Machines inspectées: `{', '.join(x['machine'] for x in report['results'])}`")
    lines.append("")
    for item in report["results"]:
        lines.append(f"## {item['machine']}")
        lines.append("")
        lines.append(f"- Mode: `{item.get('mode')}`")
        lines.append(f"- Cible SSH: `{item.get('ssh_target')}`")
        lines.append(f"- Repo: `{item.get('repo_path')}`")
        lines.append(f"- Statut: `{item.get('status')}`")
        reasons = item.get("reasons") or []
        lines.append(f"- Raisons: `{', '.join(reasons) if reasons else 'aucune'}`")
        if item.get("branch"):
            lines.append(f"- Branche: `{item['branch']}`")
        if item.get("ahead_of_remote") is not None or item.get("behind_remote") is not None:
            lines.append(f"- Ahead/Behind: `{item.get('ahead_of_remote')}/{item.get('behind_remote')}`")
        lines.append(f"- Stashs: `{len(item.get('stash', []))}`")
        lines.append("")
        lines.append("### Classification des écarts")
        lines.append("")
        cls = item.get("classification", {})
        for bucket in ["utile_probable", "artefact_probable", "ambigu", "propre"]:
            values = cls.get(bucket, [])
            lines.append(f"- **{bucket}**")
            if values:
                for value in values:
                    lines.append(f"  - `{value}`")
            else:
                lines.append("  - _aucun_")
        lines.append("")
        lines.append("### Git status")
        lines.append("")
        lines.append("```text")
        lines.append(item.get("status_sb", "") or "(vide)")
        lines.append("```")
        if item.get("left_right_log"):
            lines.append("")
            lines.append("### Divergence détaillée")
            lines.append("")
            lines.append("```text")
            lines.extend(item["left_right_log"])
            lines.append("```")
        if item.get("stash"):
            lines.append("")
            lines.append("### Stash")
            lines.append("")
            lines.append("```text")
            lines.extend(item["stash"])
            lines.append("```")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_report(report: Dict[str, Any], reports_dir: Path) -> Dict[str, str]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = report["generated_at_utc"].replace(":", "").replace("-", "")
    json_path = reports_dir / f"git_fleet_guard_audit_{stamp}.json"
    md_path = reports_dir / f"git_fleet_guard_audit_{stamp}.md"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    (reports_dir / "latest.json").write_text(json_path.read_text(encoding="utf-8"), encoding="utf-8")
    (reports_dir / "latest.md").write_text(md_path.read_text(encoding="utf-8"), encoding="utf-8")
    return {
        "json": str(json_path),
        "markdown": str(md_path),
        "latest_json": str(reports_dir / "latest.json"),
        "latest_md": str(reports_dir / "latest.md"),
    }


def cmd_status(args: argparse.Namespace) -> int:
    module_root = default_module_root()
    reports_dir = Path(args.reports_dir) if args.reports_dir else default_reports_dir(module_root)
    config_path = Path(args.config) if args.config else module_root / "config" / "machines.default.json"
    data = {
        "module_root": str(module_root),
        "reports_dir": str(reports_dir),
        "config_path": str(config_path),
        "current_host": socket.gethostname(),
        "config_exists": config_path.exists(),
        "reports_dir_exists": reports_dir.exists(),
        "remote_branch_default": DEFAULT_BRANCH,
    }
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    module_root = default_module_root()
    config = load_config(Path(args.config) if args.config else None)
    machines = resolve_machines(config, args.machines)
    if not machines:
        print("No machines resolved.", file=sys.stderr)
        return 2
    report = {
        "generated_at_utc": now_utc().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "remote_branch": args.remote_branch,
        "repo_path_default": args.repo_path,
        "results": [],
    }
    for machine in machines:
        if args.repo_path:
            machine.repo_path = args.repo_path
        report["results"].append(inspect_machine(machine, args.remote_branch, do_fetch=getattr(args, "fetch", False)))
    reports_dir = Path(args.reports_dir) if args.reports_dir else default_reports_dir(module_root)
    paths = write_report(report, reports_dir)
    summary = {
        "generated_at_utc": report["generated_at_utc"],
        "machines": [x["machine"] for x in report["results"]],
        "report_paths": paths,
        "statuses": {x["machine"]: x["status"] for x in report["results"]},
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    module_root = default_module_root()
    reports_dir = Path(args.reports_dir) if args.reports_dir else default_reports_dir(module_root)
    if args.path:
        path = Path(args.path)
    else:
        path = reports_dir / ("latest.json" if args.format == "json" else "latest.md")
    if not path.exists():
        print(f"Report not found: {path}", file=sys.stderr)
        return 2
    print(path.read_text(encoding="utf-8"))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="git_fleet_guard")
    sub = p.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status")
    status.add_argument("--config")
    status.add_argument("--reports-dir")
    status.set_defaults(func=cmd_status)

    audit = sub.add_parser("audit")
    audit.add_argument("--config")
    audit.add_argument("--machines", help="CSV of machine names or ssh targets")
    audit.add_argument("--repo-path", default=DEFAULT_REPO_PATH)
    audit.add_argument("--reports-dir")
    audit.add_argument("--remote-branch", default=DEFAULT_BRANCH)
    audit.add_argument("--fetch", dest="fetch", action="store_true", help="Refresh origin refs before audit (opt-in)")
    audit.add_argument("--no-fetch", dest="fetch", action="store_false", help="Do not refresh origin refs before audit")
    audit.set_defaults(fetch=False)
    audit.set_defaults(func=cmd_audit)

    report = sub.add_parser("report")
    report.add_argument("--reports-dir")
    report.add_argument("--path")
    report.add_argument("--format", choices=["json", "md"], default="md")
    report.set_defaults(func=cmd_report)

    remediate = sub.add_parser("remediate")
    remediate.add_argument("--reports-dir")
    remediate.add_argument("--path")
    remediate.add_argument("--machine", help="CSV of machine names to filter")
    remediate.add_argument("--format", choices=["json", "md"], default="md")
    remediate.set_defaults(func=cmd_remediate)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
