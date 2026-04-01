#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


REGISTRY_FILES = {
    "machines": "machines_registry.yaml",
    "modules": "modules_registry.yaml",
}
DEFAULT_REGISTRY_ROOT = "/opt/trading/registry"
DEFAULT_INSTALL_ROOT = "/opt/trading"
MODULE_NAME = "deploy_module_multi_machine"
SUPPORTED_REMOTE_OS = {"linux", "debian", "ubuntu", "posix", "unix"}


@dataclass
class Machine:
    alias: str
    ssh_target: str
    hostname: Optional[str] = None
    role: Optional[str] = None
    os_family: str = "linux"
    lan_ip: Optional[str] = None
    wireguard_ip: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModuleEntry:
    name: str
    install_path: Optional[str] = None
    targets: List[str] = field(default_factory=list)
    sanity_relpath: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DeployPlan:
    module_name: str
    source_dir: Path
    install_path: str
    targets: List[Machine]
    sanity_relpath: Optional[str]


class DeployError(RuntimeError):
    pass


class RegistryView:
    def __init__(self, registry_root: Path, fallback_config: Optional[Path] = None) -> None:
        self.registry_root = registry_root
        self.fallback_config = fallback_config
        self.machine_entries = self._load_yaml_file(REGISTRY_FILES["machines"])
        self.module_entries = self._load_yaml_file(REGISTRY_FILES["modules"])
        self.fallback_hosts = self._load_fallback_hosts(fallback_config)

    def _load_yaml_file(self, filename: str) -> Any:
        path = self.registry_root / filename
        if not path.exists():
            return None
        if yaml is None:
            raise DeployError(
                f"Le fichier registry {path} existe mais PyYAML n'est pas disponible. "
                "Installer pyyaml dans le venv ou utiliser --targets/--source-dir explicitement."
            )
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle) or {}

    def _load_fallback_hosts(self, path: Optional[Path]) -> Dict[str, Any]:
        if not path or not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        hosts = data.get("machines", {})
        if isinstance(hosts, dict):
            return hosts
        return {}

    def has_registry(self) -> bool:
        return any((self.registry_root / f).exists() for f in REGISTRY_FILES.values())

    def registry_status(self) -> Dict[str, Any]:
        return {
            "registry_root": str(self.registry_root),
            "machines_registry": (self.registry_root / REGISTRY_FILES["machines"]).exists(),
            "modules_registry": (self.registry_root / REGISTRY_FILES["modules"]).exists(),
            "pyyaml_available": yaml is not None,
            "fallback_hosts": sorted(self.fallback_hosts.keys()),
        }

    def get_machine(self, alias: str) -> Machine:
        normalized = alias.strip()
        if not normalized:
            raise DeployError("Alias machine vide.")

        machine = self._find_machine_in_registry(normalized)
        if machine:
            return machine

        fallback = self.fallback_hosts.get(normalized)
        if fallback:
            return Machine(
                alias=normalized,
                ssh_target=fallback.get("ssh_target") or normalized,
                hostname=fallback.get("hostname") or normalized,
                role=fallback.get("role"),
                os_family=(fallback.get("os_family") or "linux").lower(),
                lan_ip=fallback.get("lan_ip"),
                wireguard_ip=fallback.get("wireguard_ip"),
                raw=fallback,
            )

        return Machine(alias=normalized, ssh_target=normalized, hostname=normalized, raw={"source": "cli"})

    def get_module_entry(self, module_name: str) -> Optional[ModuleEntry]:
        if not self.module_entries:
            return None

        found = self._find_module_entry(module_name)
        if not found:
            return None

        return ModuleEntry(
            name=module_name,
            install_path=self._extract_first(found, [
                "install_path", "runtime_path", "deploy_path", "path", "target_path"
            ]),
            targets=self._normalize_string_list(
                self._extract_first(found, [
                    "targets", "target_hosts", "target_machines", "machines", "hosts"
                ], default=[])
            ),
            sanity_relpath=self._extract_first(found, [
                "sanity_relpath", "sanity_script", "sanity_path"
            ]),
            raw=found,
        )

    def _find_machine_in_registry(self, alias: str) -> Optional[Machine]:
        entries = self._iter_entries(self.machine_entries)
        for entry in entries:
            names = {
                str(entry.get(k)).strip()
                for k in ("alias", "name", "id", "hostname", "machine")
                if entry.get(k)
            }
            if alias in names:
                ssh_target = self._extract_first(entry, [
                    "ssh_alias", "ssh_target", "host_alias", "alias", "hostname", "name"
                ]) or alias
                return Machine(
                    alias=alias,
                    ssh_target=str(ssh_target),
                    hostname=self._extract_first(entry, ["hostname", "name", "alias"]),
                    role=self._extract_first(entry, ["role", "type", "purpose"]),
                    os_family=(self._extract_first(entry, ["os", "os_family", "platform"], default="linux") or "linux").lower(),
                    lan_ip=self._extract_first(entry, ["lan_ip", "ip", "ipv4"]),
                    wireguard_ip=self._extract_first(entry, ["wireguard_ip", "wg_ip", "vpn_ip"]),
                    raw=entry,
                )
        return None

    def _find_module_entry(self, module_name: str) -> Optional[Dict[str, Any]]:
        data = self.module_entries
        if isinstance(data, dict):
            if module_name in data and isinstance(data[module_name], dict):
                entry = dict(data[module_name])
                entry.setdefault("name", module_name)
                return entry
            for key, value in data.items():
                if isinstance(value, dict):
                    names = {
                        str(value.get(k)).strip()
                        for k in ("name", "module", "id", "slug")
                        if value.get(k)
                    }
                    names.add(str(key).strip())
                    if module_name in names:
                        value = dict(value)
                        value.setdefault("name", module_name)
                        return value
        for entry in self._iter_entries(data):
            names = {
                str(entry.get(k)).strip()
                for k in ("name", "module", "id", "slug")
                if entry.get(k)
            }
            if module_name in names:
                return entry
        return None

    def _iter_entries(self, data: Any) -> Iterable[Dict[str, Any]]:
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    yield item
        elif isinstance(data, dict):
            if isinstance(data.get("entries"), list):
                for item in data["entries"]:
                    if isinstance(item, dict):
                        yield item
            else:
                for key, value in data.items():
                    if isinstance(value, dict):
                        copy = dict(value)
                        copy.setdefault("_key", key)
                        yield copy

    def _extract_first(self, data: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
        for key in keys:
            if key in data and data[key] not in (None, ""):
                return data[key]
        return default

    def _normalize_string_list(self, value: Any) -> List[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [v.strip() for v in value.split(",") if v.strip()]
        if isinstance(value, list):
            out: List[str] = []
            for item in value:
                if isinstance(item, str) and item.strip():
                    out.append(item.strip())
            return out
        return []


class Deployer:
    def __init__(self, registry: RegistryView, args: argparse.Namespace) -> None:
        self.registry = registry
        self.args = args

    def build_plan(self) -> DeployPlan:
        module_name = self.args.module_name
        source_dir = Path(self.args.source_dir).expanduser().resolve() if self.args.source_dir else None
        if not source_dir or not source_dir.exists() or not source_dir.is_dir():
            raise DeployError("--source-dir doit pointer vers un répertoire module existant.")

        module_entry = self.registry.get_module_entry(module_name)
        install_path = self.args.install_path or (module_entry.install_path if module_entry else None)
        if not install_path:
            install_path = f"{DEFAULT_INSTALL_ROOT}/{module_name}"

        target_names = parse_csv(self.args.targets)
        if not target_names and module_entry and module_entry.targets:
            target_names = module_entry.targets
        if not target_names:
            raise DeployError(
                "Aucune cible résolue. Fournir --targets ou ajouter une liste de machines dans modules_registry.yaml."
            )

        targets: List[Machine] = []
        for target_name in target_names:
            machine = self.registry.get_machine(target_name)
            if machine.os_family.lower() not in SUPPORTED_REMOTE_OS:
                raise DeployError(
                    f"La machine {target_name} est déclarée comme {machine.os_family}. "
                    "Ce module déploie uniquement vers des hôtes POSIX avec /opt/trading."
                )
            targets.append(machine)

        sanity_relpath = self.args.sanity_relpath or (module_entry.sanity_relpath if module_entry else None)
        if not sanity_relpath:
            sanity_relpath = auto_detect_sanity_relpath(source_dir, module_name)

        return DeployPlan(
            module_name=module_name,
            source_dir=source_dir,
            install_path=install_path,
            targets=targets,
            sanity_relpath=sanity_relpath,
        )

    def show_status(self) -> int:
        payload = self.registry.registry_status()
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    def show_plan(self) -> int:
        plan = self.build_plan()
        payload = {
            "module_name": plan.module_name,
            "source_dir": str(plan.source_dir),
            "install_path": plan.install_path,
            "targets": [machine.__dict__ for machine in plan.targets],
            "sanity_relpath": plan.sanity_relpath,
            "dry_run": bool(self.args.dry_run),
            "post_install_requested": bool(self.args.post_install),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    def run_deploy(self) -> int:
        plan = self.build_plan()
        bundle = build_bundle(plan.source_dir)
        timestamp = utc_stamp()

        results: List[Dict[str, Any]] = []
        for machine in plan.targets:
            result = self._deploy_one(plan, machine, bundle, timestamp)
            results.append(result)

        print(json.dumps({"results": results}, indent=2, ensure_ascii=False))
        failed = [r for r in results if r.get("status") != "ok"]
        return 1 if failed else 0

    def run_remote_sanity(self) -> int:
        plan = self.build_plan()
        if not plan.sanity_relpath:
            raise DeployError("Impossible de déterminer le script de sanity distant.")

        results: List[Dict[str, Any]] = []
        for machine in plan.targets:
            remote_sanity = posix_join(plan.install_path, plan.sanity_relpath)
            cmd = build_ssh_command(machine.ssh_target, [
                "bash", "-lc", f"cd {shell_quote(plan.install_path)} && {shell_quote(remote_sanity)}"
            ])
            result = run_subprocess(cmd, dry_run=self.args.dry_run)
            results.append({
                "machine": machine.alias,
                "ssh_target": machine.ssh_target,
                "sanity_command": " ".join(cmd),
                "status": "ok" if result.returncode == 0 else "error",
                "returncode": result.returncode,
            })

        print(json.dumps({"results": results}, indent=2, ensure_ascii=False))
        failed = [r for r in results if r.get("status") != "ok"]
        return 1 if failed else 0

    def _deploy_one(self, plan: DeployPlan, machine: Machine, bundle: Path, timestamp: str) -> Dict[str, Any]:
        remote_tmp = f"/tmp/{plan.module_name}_{timestamp}.tar.gz"
        backup_dir = f"{plan.install_path}.bak/{timestamp}"
        remote_install = plan.install_path
        remote_sanity = posix_join(remote_install, plan.sanity_relpath) if plan.sanity_relpath else None
        post_install_script = posix_join(remote_install, "scripts/install_module.sh")
        post_install: Dict[str, Any] = {
            "requested": bool(self.args.post_install),
            "status": "disabled" if not self.args.post_install else "pending",
            "script_path": post_install_script,
            "script_found": None,
            "executed": False,
            "returncode": None,
            "stdout": "",
            "stderr": "",
        }

        scp_cmd = ["scp", str(bundle), f"{machine.ssh_target}:{remote_tmp}"]
        upload = run_subprocess(scp_cmd, dry_run=self.args.dry_run)
        if upload.returncode != 0:
            if self.args.post_install:
                post_install["status"] = "not_run"
            return {
                "machine": machine.alias,
                "ssh_target": machine.ssh_target,
                "status": "error",
                "stage": "upload",
                "returncode": upload.returncode,
                "deploy_returncode": None,
                "post_install": post_install,
            }

        remote_script = self._build_remote_install_script(
            remote_install=remote_install,
            remote_tmp=remote_tmp,
            backup_dir=backup_dir,
            sanity_cmd=remote_sanity,
            keep_tmp=bool(self.args.keep_tmp),
            no_backup=bool(self.args.no_backup),
        )
        ssh_cmd = build_ssh_command(machine.ssh_target, ["bash", "-lc", remote_script])
        deploy = run_subprocess(ssh_cmd, dry_run=self.args.dry_run)

        status = "ok" if deploy.returncode == 0 else "error"
        stage = "deploy"
        result_returncode = deploy.returncode

        if deploy.returncode == 0 and self.args.post_install:
            post_install = self._run_remote_post_install(machine, remote_install, post_install_script)
            if post_install.get("status") == "error":
                status = "partial"
                stage = "post_install"
                result_returncode = post_install.get("returncode") or deploy.returncode
        elif deploy.returncode != 0 and self.args.post_install:
            post_install["status"] = "not_run"

        return {
            "machine": machine.alias,
            "ssh_target": machine.ssh_target,
            "status": status,
            "stage": stage,
            "returncode": result_returncode,
            "deploy_returncode": deploy.returncode,
            "install_path": remote_install,
            "backup_dir": backup_dir,
            "sanity_relpath": plan.sanity_relpath,
            "post_install": post_install,
        }

    def _run_remote_post_install(
        self,
        machine: Machine,
        remote_install: str,
        post_install_script: str,
    ) -> Dict[str, Any]:
        remote_script = self._build_remote_post_install_script(
            remote_install=remote_install,
            post_install_script=post_install_script,
        )
        ssh_cmd = build_ssh_command(machine.ssh_target, ["bash", "-lc", remote_script])
        result = run_subprocess(ssh_cmd, dry_run=self.args.dry_run, capture_output=True)
        payload: Dict[str, Any] = {
            "requested": True,
            "status": "dry_run" if self.args.dry_run else "error",
            "script_path": post_install_script,
            "script_found": None,
            "executed": False,
            "returncode": result.returncode,
            "stdout": truncate_output(result.stdout or ""),
            "stderr": truncate_output(result.stderr or ""),
        }
        if self.args.dry_run:
            return payload

        marker_line = None
        for line in (result.stdout or "").splitlines():
            if line.startswith("__POST_INSTALL__ "):
                marker_line = line.strip()
                break

        marker_fields: Dict[str, str] = {}
        if marker_line:
            for chunk in marker_line.split()[1:]:
                if "=" not in chunk:
                    continue
                key, value = chunk.split("=", 1)
                marker_fields[key] = value
            payload["script_found"] = marker_fields.get("found") == "1"
            payload["executed"] = marker_fields.get("executed") == "1"
            if marker_fields.get("status") == "skipped":
                payload["status"] = "skipped"
                return payload

        payload["status"] = "ok" if result.returncode == 0 else "error"
        if payload["script_found"] is None:
            payload["script_found"] = result.returncode == 0
        if payload["status"] == "ok":
            payload["executed"] = True
        return payload

    def _build_remote_post_install_script(
        self,
        *,
        remote_install: str,
        post_install_script: str,
    ) -> str:
        lines = [
            "set -euo pipefail",
            f"REMOTE_INSTALL={shell_quote(remote_install)}",
            f"POST_INSTALL_SCRIPT={shell_quote(post_install_script)}",
            'if [ ! -f "$POST_INSTALL_SCRIPT" ]; then',
            '  printf "__POST_INSTALL__ status=skipped found=0 executed=0 path=%s\n" "$POST_INSTALL_SCRIPT"',
            '  exit 0',
            'fi',
            'chmod +x "$POST_INSTALL_SCRIPT" || true',
            'printf "__POST_INSTALL__ status=running found=1 executed=1 path=%s\n" "$POST_INSTALL_SCRIPT"',
            'cd "$REMOTE_INSTALL"',
            '"$POST_INSTALL_SCRIPT"',
        ]
        script = "\n".join(lines)
        validate_shell_script(script)
        return script

    def _build_remote_install_script(
        self,
        *,
        remote_install: str,
        remote_tmp: str,
        backup_dir: str,
        sanity_cmd: Optional[str],
        keep_tmp: bool,
        no_backup: bool,
    ) -> str:
        lines = [
            "set -euo pipefail",
            f"REMOTE_INSTALL={shell_quote(remote_install)}",
            f"REMOTE_TMP={shell_quote(remote_tmp)}",
            f"BACKUP_DIR={shell_quote(backup_dir)}",
            'STAGE_DIR=$(mktemp -d "/tmp/deploy_stage.XXXXXX")',
            'cleanup() { if [ -n "${STAGE_DIR:-}" ] && [ -d "$STAGE_DIR" ]; then rm -rf "$STAGE_DIR"; fi; }',
            'trap cleanup EXIT',
            'mkdir -p "$STAGE_DIR"',
            'tar -xzf "$REMOTE_TMP" -C "$STAGE_DIR"',
        ]
        if not no_backup:
            lines.extend([
                'if [ -d "$REMOTE_INSTALL" ]; then',
                '  mkdir -p "$(dirname "$BACKUP_DIR")"',
                '  rm -rf "$BACKUP_DIR"',
                '  mv "$REMOTE_INSTALL" "$BACKUP_DIR"',
                'fi',
            ])
        else:
            lines.extend([
                'if [ -d "$REMOTE_INSTALL" ]; then',
                '  rm -rf "$REMOTE_INSTALL"',
                'fi',
            ])
        lines.extend([
            'mkdir -p "$(dirname "$REMOTE_INSTALL")"',
            'mv "$STAGE_DIR" "$REMOTE_INSTALL"',
            'STAGE_DIR=""',
        ])
        if sanity_cmd:
            lines.append(f"{shell_quote(sanity_cmd)}")
        if not keep_tmp:
            lines.append('rm -f "$REMOTE_TMP"')
        script = "\n".join(lines)
        validate_shell_script(script)
        return script


def build_bundle(source_dir: Path) -> Path:
    temp_dir = Path(tempfile.mkdtemp(prefix="deploy_bundle_"))
    bundle_path = temp_dir / f"{source_dir.name}.tar.gz"
    subprocess.run([
        "tar", "-czf", str(bundle_path), "-C", str(source_dir), "."
    ], check=True)
    return bundle_path


def auto_detect_sanity_relpath(source_dir: Path, module_name: str) -> Optional[str]:
    candidates = [
        f"scripts/{module_name}_sanity_check.sh",
        "scripts/sanity_check.sh",
        f"{module_name}_sanity_check.sh",
    ]
    for candidate in candidates:
        if (source_dir / candidate).exists():
            return candidate
    return None


def build_ssh_command(target: str, remote_args: List[str]) -> List[str]:
    remote_command = " ".join(shell_quote(arg) for arg in remote_args)
    return ["ssh", target, remote_command]


def validate_shell_script(script: str) -> None:
    result = subprocess.run(
        ["bash", "-n"],
        input=script,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode == 0:
        return
    stderr = (result.stderr or result.stdout or "").strip()
    raise DeployError(f"Script shell distant invalide: {stderr or 'bash -n failed.'}")


def run_subprocess(
    cmd: List[str],
    dry_run: bool = False,
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:
    if dry_run:
        print(json.dumps({"dry_run": True, "command": cmd}, ensure_ascii=False))
        return subprocess.CompletedProcess(cmd, 0, "", "")
    return subprocess.run(cmd, check=False, text=True, capture_output=capture_output)


def truncate_output(value: str, limit: int = 2000) -> str:
    if len(value) <= limit:
        return value
    return value[:limit] + "\n...[truncated]..."


def parse_csv(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def posix_join(base: str, rel: Optional[str]) -> str:
    if not rel:
        return base
    return f"{base.rstrip('/')}/{rel.lstrip('/')}"


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def shell_quote(value: str) -> str:
    return shlex.quote(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Déploiement multi-machines de modules via SSH.")
    parser.add_argument("command", choices=["status", "plan", "deploy", "sanity"], help="Action à exécuter")
    parser.add_argument("--registry-root", default=DEFAULT_REGISTRY_ROOT, help="Chemin vers /opt/trading/registry")
    parser.add_argument(
        "--fallback-config",
        default=str(Path(__file__).resolve().parents[1] / "config" / "hosts_fallback.json"),
        help="Inventaire de secours JSON si le registry n'est pas lisible",
    )
    parser.add_argument("--module-name", help="Nom logique du module à déployer")
    parser.add_argument("--source-dir", help="Répertoire source local du module à empaqueter")
    parser.add_argument("--install-path", help="Chemin distant cible, ex: /opt/trading/validated_prompt_factory")
    parser.add_argument("--targets", help="Liste CSV des aliases SSH cibles")
    parser.add_argument("--sanity-relpath", help="Chemin relatif du sanity sur l'hôte distant")
    parser.add_argument("--dry-run", action="store_true", help="Afficher les commandes sans exécuter SSH/SCP")
    parser.add_argument("--keep-tmp", action="store_true", help="Conserver le bundle temporaire distant sous /tmp")
    parser.add_argument("--no-backup", action="store_true", help="Remplacer sans backup préalable")
    parser.add_argument("--post-install", action="store_true", help="Executer scripts/install_module.sh sur la cible si present")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    registry = RegistryView(
        registry_root=Path(args.registry_root).expanduser().resolve(),
        fallback_config=Path(args.fallback_config).expanduser().resolve() if args.fallback_config else None,
    )
    deployer = Deployer(registry, args)

    if args.command == "status":
        return deployer.show_status()
    if args.command == "plan":
        if not args.module_name:
            raise DeployError("--module-name est requis pour plan.")
        return deployer.show_plan()
    if args.command == "deploy":
        if not args.module_name or not args.source_dir:
            raise DeployError("--module-name et --source-dir sont requis pour deploy.")
        return deployer.run_deploy()
    if args.command == "sanity":
        if not args.module_name or not args.source_dir:
            raise DeployError("--module-name et --source-dir sont requis pour sanity.")
        return deployer.run_remote_sanity()
    raise DeployError(f"Commande non supportée: {args.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DeployError as exc:
        print(f"ERREUR: {exc}", file=sys.stderr)
        raise SystemExit(1)
