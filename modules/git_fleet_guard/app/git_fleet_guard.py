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
    result: Dict[str, Any] = {
        "machine": machine.name,
        "ssh_target": machine.ssh_target,
        "repo_path": machine.repo_path,
        "mode": "local" if machine.is_local() else "ssh",
        "reachable": False,
        "repo_exists": False,
        "fetch_attempted": do_fetch,
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

    result["classification"] = classify_changes(result["status_short"])

    reasons: List[str] = []
    if outputs["toplevel"].returncode != 0:
        reasons.append("not_a_git_repo")
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
        report["results"].append(inspect_machine(machine, args.remote_branch, do_fetch=not args.no_fetch))
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
    audit.add_argument("--no-fetch", action="store_true", help="Do not refresh origin refs before audit")
    audit.set_defaults(func=cmd_audit)

    report = sub.add_parser("report")
    report.add_argument("--reports-dir")
    report.add_argument("--path")
    report.add_argument("--format", choices=["json", "md"], default="md")
    report.set_defaults(func=cmd_report)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
