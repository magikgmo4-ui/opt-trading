#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import uuid
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
DEFAULT_LOCK_STALE_AFTER_SECONDS = 3600


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

    def run_preflight(self) -> int:
        plan = self.build_plan()
        source_post_install = plan.source_dir / "scripts" / "install_module.sh"
        source_post_install_exists = source_post_install.is_file()
        source_post_install_uses_sudo = False
        if source_post_install_exists:
            source_post_install_uses_sudo = "sudo" in source_post_install.read_text(
                encoding="utf-8",
                errors="replace",
            )

        results: List[Dict[str, Any]] = []
        for machine in plan.targets:
            result = self._probe_one(
                plan,
                machine,
                source_post_install_exists=source_post_install_exists,
                source_post_install_uses_sudo=source_post_install_uses_sudo,
            )
            results.append(result)

        payload = {
            "module_name": plan.module_name,
            "source_dir": str(plan.source_dir),
            "install_path": plan.install_path,
            "post_install_requested": bool(self.args.post_install),
            "results": results,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        failed = [r for r in results if r.get("status") != "ok"]
        return 1 if failed else 0

    def run_deploy(self) -> int:
        plan = self.build_plan()
        run_id = make_run_id()
        bundle = build_bundle(plan.source_dir, run_id)

        results: List[Dict[str, Any]] = []
        for machine in plan.targets:
            result = self._deploy_one(plan, machine, bundle, run_id)
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

    def _probe_one(
        self,
        plan: DeployPlan,
        machine: Machine,
        *,
        source_post_install_exists: bool,
        source_post_install_uses_sudo: bool,
    ) -> Dict[str, Any]:
        remote_install = plan.install_path
        remote_post_install = posix_join(remote_install, "scripts/install_module.sh")
        lock_path = make_remote_lock_path(remote_install)
        probe_cmd = build_ssh_command(
            machine.ssh_target,
            ["sh", "-lc", self._build_remote_preflight_script()],
            batch_mode=True,
            connect_timeout=5,
        )
        probe = run_subprocess(probe_cmd, capture_output=True)
        payload: Dict[str, Any] = {
            "machine": machine.alias,
            "ssh_target": machine.ssh_target,
            "status": "blocked",
            "reasons": [],
            "ssh_reachable": False,
            "effective_user": None,
            "bash_present": False,
            "tar_present": False,
            "python3_present": False,
            "opt_trading_exists": False,
            "opt_trading_accessible": False,
            "tmp_writable": False,
            "sudo_present": False,
            "sudo_noninteractive": False,
            "returncode": probe.returncode,
            "stdout": truncate_output(probe.stdout or ""),
            "stderr": truncate_output(probe.stderr or ""),
            "post_install": self._predict_post_install(
                requested=bool(self.args.post_install),
                runtime_script_path=remote_post_install,
                source_script_exists=source_post_install_exists,
                source_script_uses_sudo=source_post_install_uses_sudo,
                reachable=False,
                sudo_present=False,
                sudo_noninteractive=False,
                bash_present=False,
                tar_present=False,
                opt_trading_accessible=False,
                tmp_writable=False,
            ),
            "lock": self._inspect_remote_lock(
                machine,
                lock_path,
                int(self.args.lock_stale_after_seconds),
            ),
        }
        if probe.returncode != 0:
            payload["reasons"] = [f"ssh probe failed (returncode={probe.returncode})"]
            return payload

        marker_line = None
        for line in (probe.stdout or "").splitlines():
            if line.startswith("__PREFLIGHT__ "):
                marker_line = line.strip()
                break
        if not marker_line:
            payload["reasons"] = ["missing preflight marker in stdout"]
            return payload

        marker_fields: Dict[str, str] = {}
        for chunk in marker_line.split()[1:]:
            if "=" not in chunk:
                continue
            key, value = chunk.split("=", 1)
            marker_fields[key] = value

        payload["ssh_reachable"] = marker_fields.get("reachable") == "1"
        payload["effective_user"] = marker_fields.get("effective_user")
        payload["bash_present"] = marker_fields.get("bash_present") == "1"
        payload["tar_present"] = marker_fields.get("tar_present") == "1"
        payload["python3_present"] = marker_fields.get("python3_present") == "1"
        payload["opt_trading_exists"] = marker_fields.get("opt_trading_exists") == "1"
        payload["opt_trading_accessible"] = marker_fields.get("opt_trading_accessible") == "1"
        payload["tmp_writable"] = marker_fields.get("tmp_writable") == "1"
        payload["sudo_present"] = marker_fields.get("sudo_present") == "1"
        payload["sudo_noninteractive"] = marker_fields.get("sudo_noninteractive") == "1"

        payload["post_install"] = self._predict_post_install(
            requested=bool(self.args.post_install),
            runtime_script_path=remote_post_install,
            source_script_exists=source_post_install_exists,
            source_script_uses_sudo=source_post_install_uses_sudo,
            reachable=payload["ssh_reachable"],
            sudo_present=payload["sudo_present"],
            sudo_noninteractive=payload["sudo_noninteractive"],
            bash_present=payload["bash_present"],
            tar_present=payload["tar_present"],
            opt_trading_accessible=payload["opt_trading_accessible"],
            tmp_writable=payload["tmp_writable"],
        )

        reasons: List[str] = []
        if not payload["ssh_reachable"]:
            reasons.append("ssh unreachable")
        if not payload["bash_present"]:
            reasons.append("bash missing")
        if not payload["tar_present"]:
            reasons.append("tar missing")
        if not payload["opt_trading_exists"]:
            reasons.append("/opt/trading missing")
        elif not payload["opt_trading_accessible"]:
            reasons.append("/opt/trading not accessible")
        if not payload["tmp_writable"]:
            reasons.append("/tmp not writable")

        if reasons:
            payload["status"] = "blocked"
            payload["reasons"] = reasons
            return payload

        warning_reasons: List[str] = []
        if not payload["python3_present"]:
            warning_reasons.append("python3 missing")
        prediction = payload["post_install"]["prediction"]
        if prediction == "will_require_password":
            warning_reasons.append("post-install will likely require sudo password")
        elif prediction == "blocked":
            payload["status"] = "blocked"
            payload["reasons"] = [payload["post_install"]["reason"]]
            return payload

        lock_info = payload["lock"]
        if lock_info.get("exists"):
            payload["status"] = "blocked"
            if lock_info.get("stale"):
                payload["reasons"] = ["stale lock detected"]
            else:
                payload["reasons"] = ["lock currently held"]
            return payload

        payload["status"] = "warning" if warning_reasons else "ok"
        payload["reasons"] = warning_reasons
        return payload

    def _predict_post_install(
        self,
        *,
        requested: bool,
        runtime_script_path: str,
        source_script_exists: bool,
        source_script_uses_sudo: bool,
        reachable: bool,
        sudo_present: bool,
        sudo_noninteractive: bool,
        bash_present: bool,
        tar_present: bool,
        opt_trading_accessible: bool,
        tmp_writable: bool,
    ) -> Dict[str, Any]:
        payload = {
            "requested": requested,
            "runtime_script_path": runtime_script_path,
            "source_script_exists": source_script_exists,
            "source_script_uses_sudo": source_script_uses_sudo if source_script_exists else None,
            "sudo_noninteractive": sudo_noninteractive if requested else None,
            "prediction": "disabled",
            "reason": "post-install not requested",
        }
        if not requested:
            return payload

        if not source_script_exists:
            payload["prediction"] = "skipped"
            payload["reason"] = "scripts/install_module.sh absent from source runtime"
            return payload

        if not reachable:
            payload["prediction"] = "blocked"
            payload["reason"] = "ssh unreachable"
            return payload

        if not bash_present:
            payload["prediction"] = "blocked"
            payload["reason"] = "bash missing on target"
            return payload

        if not tar_present:
            payload["prediction"] = "blocked"
            payload["reason"] = "tar missing on target"
            return payload

        if not opt_trading_accessible:
            payload["prediction"] = "blocked"
            payload["reason"] = "/opt/trading not accessible on target"
            return payload

        if not tmp_writable:
            payload["prediction"] = "blocked"
            payload["reason"] = "/tmp not writable on target"
            return payload

        if source_script_uses_sudo and not sudo_present:
            payload["prediction"] = "blocked"
            payload["reason"] = "install_module.sh uses sudo but sudo is unavailable"
            return payload

        if source_script_uses_sudo and not sudo_noninteractive:
            payload["prediction"] = "will_require_password"
            payload["reason"] = "install_module.sh uses sudo but sudo -n is unavailable"
            return payload

        payload["prediction"] = "ok"
        payload["reason"] = "preflight checks passed"
        return payload

    def _build_remote_preflight_script(self) -> str:
        lines = [
            "set -eu",
            'has_cmd() { command -v "$1" >/dev/null 2>&1 && printf 1 || printf 0; }',
            'bash_present=$(has_cmd bash)',
            'tar_present=$(has_cmd tar)',
            'python3_present=$(has_cmd python3)',
            'sudo_present=$(has_cmd sudo)',
            'sudo_noninteractive=0',
            'if [ "$sudo_present" = "1" ] && sudo -n true >/dev/null 2>&1; then sudo_noninteractive=1; fi',
            'opt_trading_exists=0',
            'opt_trading_accessible=0',
            'if [ -d "/opt/trading" ]; then opt_trading_exists=1; fi',
            'if [ -d "/opt/trading" ] && [ -x "/opt/trading" ]; then opt_trading_accessible=1; fi',
            'tmp_writable=0',
            'tmp_probe=""',
            'if tmp_probe=$(mktemp /tmp/deploy_preflight.XXXXXX 2>/dev/null); then tmp_writable=1; rm -f "$tmp_probe"; fi',
            'effective_user=$(whoami 2>/dev/null || id -un 2>/dev/null || printf unknown)',
            'printf "__PREFLIGHT__ reachable=1 effective_user=%s bash_present=%s tar_present=%s python3_present=%s opt_trading_exists=%s opt_trading_accessible=%s tmp_writable=%s sudo_present=%s sudo_noninteractive=%s\n" "$effective_user" "$bash_present" "$tar_present" "$python3_present" "$opt_trading_exists" "$opt_trading_accessible" "$tmp_writable" "$sudo_present" "$sudo_noninteractive"',
        ]
        script = "\n".join(lines)
        validate_shell_script(script)
        return script

    def _deploy_one(self, plan: DeployPlan, machine: Machine, bundle: Path, run_id: str) -> Dict[str, Any]:
        remote_tmp = f"/tmp/{plan.module_name}_{run_id}.tar.gz"
        backup_dir = f"{plan.install_path}.bak/{run_id}"
        remote_install = plan.install_path
        remote_sanity = posix_join(remote_install, plan.sanity_relpath) if plan.sanity_relpath else None
        post_install_script = posix_join(remote_install, "scripts/install_module.sh")
        lock_path = make_remote_lock_path(remote_install)
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
        lock: Dict[str, Any] = {
            "path": lock_path,
            "status": "dry_run" if self.args.dry_run else "pending",
            "acquired": False,
            "reason": "dry-run" if self.args.dry_run else "pending",
            "owner_run_id": run_id,
            "returncode": 0 if self.args.dry_run else None,
        }

        remote_script = self._build_remote_install_script(
            run_id=run_id,
            remote_install=remote_install,
            remote_tmp=remote_tmp,
            backup_dir=backup_dir,
            sanity_cmd=remote_sanity,
            keep_tmp=bool(self.args.keep_tmp),
            no_backup=bool(self.args.no_backup),
        )

        if not self.args.dry_run:
            lock = self._acquire_remote_lock(machine, lock_path, run_id)
            if not lock.get("acquired"):
                inspection = self._inspect_remote_lock(
                    machine,
                    lock_path,
                    int(self.args.lock_stale_after_seconds),
                )
                lock.update({k: v for k, v in inspection.items() if k not in {"path"}})
                cleanup_details: Dict[str, Any] = {}
                if (not lock.get("acquired")) and bool(self.args.cleanup_stale_lock) and lock.get("stale"):
                    cleanup = self._cleanup_remote_stale_lock(
                        machine,
                        lock_path,
                        int(self.args.lock_stale_after_seconds),
                    )
                    cleanup_details = {
                        "cleanup_attempted": True,
                        "cleanup_status": cleanup.get("status"),
                        "cleanup_reason": cleanup.get("reason"),
                        "cleanup_returncode": cleanup.get("returncode"),
                        "cleanup_stdout": cleanup.get("stdout"),
                        "cleanup_stderr": cleanup.get("stderr"),
                        "cleaned": cleanup.get("cleaned"),
                    }
                    if cleanup.get("owner_run_id"):
                        cleanup_details["owner_run_id"] = cleanup.get("owner_run_id")
                    lock.update(cleanup_details)
                    if cleanup.get("cleaned"):
                        reacquired = self._acquire_remote_lock(machine, lock_path, run_id)
                        lock = reacquired
                        lock.update(cleanup_details)
                        if not lock.get("acquired"):
                            inspection = self._inspect_remote_lock(
                                machine,
                                lock_path,
                                int(self.args.lock_stale_after_seconds),
                            )
                            lock.update({k: v for k, v in inspection.items() if k not in {"path"}})
                if not lock.get("acquired"):
                    if self.args.post_install:
                        post_install["status"] = "not_run"
                    return {
                        "machine": machine.alias,
                        "ssh_target": machine.ssh_target,
                        "status": "blocked",
                        "stage": "lock",
                        "returncode": lock.get("returncode") or 1,
                        "deploy_returncode": None,
                        "run_id": run_id,
                        "install_path": remote_install,
                        "backup_dir": backup_dir,
                        "sanity_relpath": plan.sanity_relpath,
                        "lock": lock,
                        "post_install": post_install,
                    }

        status = "ok"
        stage = "deploy"
        result_returncode = 0
        deploy_returncode: Optional[int] = None

        try:
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
                    "run_id": run_id,
                    "install_path": remote_install,
                    "backup_dir": backup_dir,
                    "sanity_relpath": plan.sanity_relpath,
                    "lock": lock,
                    "post_install": post_install,
                }

            ssh_cmd = build_ssh_command(machine.ssh_target, ["bash", "-lc", remote_script])
            deploy = run_subprocess(ssh_cmd, dry_run=self.args.dry_run)
            deploy_returncode = deploy.returncode

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
        finally:
            if lock.get("acquired"):
                release = self._release_remote_lock(machine, lock_path, run_id)
                lock["release_status"] = release.get("status")
                lock["release_reason"] = release.get("reason")
                lock["released"] = release.get("released")
                lock["release_returncode"] = release.get("returncode")
                if release.get("owner_run_id"):
                    lock["owner_run_id"] = release.get("owner_run_id")
                if release.get("status") == "released":
                    lock["status"] = "released"
                    lock["reason"] = "released"
                else:
                    lock["status"] = "release_error"
                    lock["reason"] = release.get("reason") or "release failed"
                    if status == "ok":
                        status = "partial"
                        stage = "unlock"
                        result_returncode = release.get("returncode") or 1

        return {
            "machine": machine.alias,
            "ssh_target": machine.ssh_target,
            "status": status,
            "stage": stage,
            "returncode": result_returncode,
            "deploy_returncode": deploy_returncode,
            "run_id": run_id,
            "install_path": remote_install,
            "backup_dir": backup_dir,
            "sanity_relpath": plan.sanity_relpath,
            "lock": lock,
            "post_install": post_install,
        }

    def _acquire_remote_lock(self, machine: Machine, lock_path: str, run_id: str) -> Dict[str, Any]:
        remote_script = self._build_remote_lock_acquire_script(lock_path=lock_path, run_id=run_id)
        ssh_cmd = build_ssh_command(machine.ssh_target, ["bash", "-lc", remote_script])
        result = run_subprocess(ssh_cmd, capture_output=True)
        payload: Dict[str, Any] = {
            "path": lock_path,
            "status": "error",
            "acquired": False,
            "reason": "lock acquire failed",
            "owner_run_id": run_id,
            "returncode": result.returncode,
            "stdout": truncate_output(result.stdout or ""),
            "stderr": truncate_output(result.stderr or ""),
        }
        marker = self._parse_lock_marker(result.stdout or "")
        if marker:
            payload["status"] = marker.get("status") or payload["status"]
            payload["acquired"] = marker.get("acquired") == "1"
            payload["reason"] = marker.get("reason") or payload["reason"]
            payload["path"] = marker.get("path") or lock_path
            if marker.get("owner"):
                payload["owner_run_id"] = marker.get("owner")
        if payload["acquired"]:
            payload["returncode"] = 0
        if payload["acquired"] and result.returncode == 0:
            return payload
        if payload["status"] == "error" and result.returncode == 42:
            payload["status"] = "busy"
            payload["reason"] = payload.get("reason") or "lock already held"
        return payload

    def _release_remote_lock(self, machine: Machine, lock_path: str, run_id: str) -> Dict[str, Any]:
        remote_script = self._build_remote_lock_release_script(lock_path=lock_path, run_id=run_id)
        ssh_cmd = build_ssh_command(machine.ssh_target, ["bash", "-lc", remote_script])
        result = run_subprocess(ssh_cmd, capture_output=True)
        payload: Dict[str, Any] = {
            "path": lock_path,
            "status": "error",
            "released": False,
            "reason": "lock release failed",
            "owner_run_id": run_id,
            "returncode": result.returncode,
            "stdout": truncate_output(result.stdout or ""),
            "stderr": truncate_output(result.stderr or ""),
        }
        marker = self._parse_lock_marker(result.stdout or "")
        if marker:
            payload["status"] = marker.get("status") or payload["status"]
            payload["released"] = marker.get("released") == "1"
            payload["reason"] = marker.get("reason") or payload["reason"]
            payload["path"] = marker.get("path") or lock_path
            if marker.get("owner"):
                payload["owner_run_id"] = marker.get("owner")
        if payload["released"]:
            payload["returncode"] = 0
        return payload

    def _build_remote_lock_acquire_script(self, *, lock_path: str, run_id: str) -> str:
        lines = [
            "set -euo pipefail",
            f"LOCK_PATH={shell_quote(lock_path)}",
            f"RUN_ID={shell_quote(run_id)}",
            'LOCK_ROOT=$(dirname "$LOCK_PATH")',
            'mkdir -p "$LOCK_ROOT"',
            'if mkdir "$LOCK_PATH" 2>/dev/null; then',
            '  printf "%s\n" "$RUN_ID" > "$LOCK_PATH/owner.run_id"',
            '  date -u +%s > "$LOCK_PATH/created_at_epoch"',
            '  date -u +%Y-%m-%dT%H:%M:%SZ > "$LOCK_PATH/created_at_utc"',
            '  printf "__LOCK__ status=acquired acquired=1 path=%s reason=acquired owner=%s\n" "$LOCK_PATH" "$RUN_ID"',
            '  exit 0',
            'fi',
            'OWNER="unknown"',
            'if [ -f "$LOCK_PATH/owner.run_id" ]; then OWNER=$(tr -d "\\n" < "$LOCK_PATH/owner.run_id" 2>/dev/null || printf unknown); fi',
            'printf "__LOCK__ status=busy acquired=0 path=%s reason=lock_exists owner=%s\n" "$LOCK_PATH" "$OWNER"',
            'exit 42',
        ]
        script = "\n".join(lines)
        validate_shell_script(script)
        return script

    def _build_remote_lock_release_script(self, *, lock_path: str, run_id: str) -> str:
        lines = [
            "set -euo pipefail",
            f"LOCK_PATH={shell_quote(lock_path)}",
            f"RUN_ID={shell_quote(run_id)}",
            'if [ ! -d "$LOCK_PATH" ]; then',
            '  printf "__LOCK__ status=released released=1 path=%s reason=already_absent owner=%s\n" "$LOCK_PATH" "$RUN_ID"',
            '  exit 0',
            'fi',
            'OWNER="unknown"',
            'if [ -f "$LOCK_PATH/owner.run_id" ]; then OWNER=$(tr -d "\\n" < "$LOCK_PATH/owner.run_id" 2>/dev/null || printf unknown); fi',
            'if [ "$OWNER" != "$RUN_ID" ]; then',
            '  printf "__LOCK__ status=not_owner released=0 path=%s reason=owner_mismatch owner=%s\n" "$LOCK_PATH" "$OWNER"',
            '  exit 43',
            'fi',
            'rm -rf "$LOCK_PATH"',
            'printf "__LOCK__ status=released released=1 path=%s reason=released owner=%s\n" "$LOCK_PATH" "$RUN_ID"',
        ]
        script = "\n".join(lines)
        validate_shell_script(script)
        return script

    def _parse_lock_marker(self, output: str) -> Optional[Dict[str, str]]:
        for line in output.splitlines():
            if not line.startswith("__LOCK__ "):
                continue
            marker: Dict[str, str] = {}
            for chunk in line.split()[1:]:
                if "=" not in chunk:
                    continue
                key, value = chunk.split("=", 1)
                marker[key] = value
            return marker
        return None

    def _inspect_remote_lock(
        self,
        machine: Machine,
        lock_path: str,
        stale_after_seconds: int,
    ) -> Dict[str, Any]:
        remote_script = self._build_remote_lock_inspect_script(
            lock_path=lock_path,
            stale_after_seconds=stale_after_seconds,
        )
        ssh_cmd = build_ssh_command(machine.ssh_target, ["bash", "-lc", remote_script])
        result = run_subprocess(ssh_cmd, capture_output=True)
        payload: Dict[str, Any] = {
            "path": lock_path,
            "exists": False,
            "status": "error",
            "reason": "lock inspect failed",
            "owner_run_id": None,
            "created_at_epoch": None,
            "created_at_utc": None,
            "age_seconds": None,
            "stale": False,
            "stale_after_seconds": stale_after_seconds,
            "returncode": result.returncode,
            "stdout": truncate_output(result.stdout or ""),
            "stderr": truncate_output(result.stderr or ""),
        }
        marker = self._parse_named_marker(result.stdout or "", "__LOCK_INFO__")
        if marker:
            payload["exists"] = marker.get("exists") == "1"
            payload["status"] = marker.get("status") or payload["status"]
            payload["reason"] = marker.get("reason") or payload["reason"]
            payload["path"] = marker.get("path") or lock_path
            payload["owner_run_id"] = marker.get("owner")
            payload["created_at_epoch"] = parse_int(marker.get("created_at_epoch"))
            payload["created_at_utc"] = marker.get("created_at_utc")
            payload["age_seconds"] = parse_int(marker.get("age_seconds"))
            payload["stale"] = marker.get("stale") == "1"
            payload["stale_after_seconds"] = parse_int(marker.get("stale_after_seconds")) or stale_after_seconds
            if payload["exists"] or payload["status"] == "absent":
                payload["returncode"] = 0
        return payload

    def _cleanup_remote_stale_lock(
        self,
        machine: Machine,
        lock_path: str,
        stale_after_seconds: int,
    ) -> Dict[str, Any]:
        remote_script = self._build_remote_lock_cleanup_script(
            lock_path=lock_path,
            stale_after_seconds=stale_after_seconds,
        )
        ssh_cmd = build_ssh_command(machine.ssh_target, ["bash", "-lc", remote_script])
        result = run_subprocess(ssh_cmd, capture_output=True)
        payload: Dict[str, Any] = {
            "path": lock_path,
            "status": "error",
            "cleaned": False,
            "reason": "stale lock cleanup failed",
            "owner_run_id": None,
            "created_at_epoch": None,
            "created_at_utc": None,
            "age_seconds": None,
            "stale": None,
            "stale_after_seconds": stale_after_seconds,
            "returncode": result.returncode,
            "stdout": truncate_output(result.stdout or ""),
            "stderr": truncate_output(result.stderr or ""),
        }
        marker = self._parse_named_marker(result.stdout or "", "__LOCK_CLEANUP__")
        if marker:
            payload["status"] = marker.get("status") or payload["status"]
            payload["cleaned"] = marker.get("cleaned") == "1"
            payload["reason"] = marker.get("reason") or payload["reason"]
            payload["path"] = marker.get("path") or lock_path
            payload["owner_run_id"] = marker.get("owner")
            payload["created_at_epoch"] = parse_int(marker.get("created_at_epoch"))
            payload["created_at_utc"] = marker.get("created_at_utc")
            payload["age_seconds"] = parse_int(marker.get("age_seconds"))
            stale_value = marker.get("stale")
            payload["stale"] = None if stale_value is None else stale_value == "1"
            payload["stale_after_seconds"] = parse_int(marker.get("stale_after_seconds")) or stale_after_seconds
            if payload["cleaned"] or payload["status"] == "absent":
                payload["returncode"] = 0
        return payload

    def _build_remote_lock_inspect_script(self, *, lock_path: str, stale_after_seconds: int) -> str:
        lines = [
            "set -euo pipefail",
            f"LOCK_PATH={shell_quote(lock_path)}",
            f"STALE_AFTER_SECONDS={int(stale_after_seconds)}",
            'if [ ! -d "$LOCK_PATH" ]; then',
            '  printf "__LOCK_INFO__ status=absent exists=0 path=%s reason=lock_absent stale=0 stale_after_seconds=%s\n" "$LOCK_PATH" "$STALE_AFTER_SECONDS"',
            '  exit 0',
            'fi',
            'OWNER="unknown"',
            'if [ -f "$LOCK_PATH/owner.run_id" ]; then OWNER=$(tr -d "\\n" < "$LOCK_PATH/owner.run_id" 2>/dev/null || printf unknown); fi',
            'CREATED_EPOCH=""',
            'if [ -f "$LOCK_PATH/created_at_epoch" ]; then CREATED_EPOCH=$(tr -d "\\n" < "$LOCK_PATH/created_at_epoch" 2>/dev/null || printf ""); fi',
            'if [ -z "$CREATED_EPOCH" ]; then CREATED_EPOCH=$(stat -c %Y "$LOCK_PATH" 2>/dev/null || printf 0); fi',
            'CREATED_UTC=""',
            'if [ -f "$LOCK_PATH/created_at_utc" ]; then CREATED_UTC=$(tr -d "\\n" < "$LOCK_PATH/created_at_utc" 2>/dev/null || printf ""); fi',
            'NOW_EPOCH=$(date -u +%s 2>/dev/null || printf 0)',
            'AGE_SECONDS=-1',
            'STALE=0',
            'if [[ "$CREATED_EPOCH" =~ ^[0-9]+$ ]] && [[ "$NOW_EPOCH" =~ ^[0-9]+$ ]] && [ "$NOW_EPOCH" -ge "$CREATED_EPOCH" ]; then',
            '  AGE_SECONDS=$((NOW_EPOCH - CREATED_EPOCH))',
            '  if [ "$AGE_SECONDS" -ge "$STALE_AFTER_SECONDS" ]; then STALE=1; fi',
            'fi',
            'printf "__LOCK_INFO__ status=present exists=1 path=%s reason=lock_present owner=%s created_at_epoch=%s created_at_utc=%s age_seconds=%s stale=%s stale_after_seconds=%s\n" "$LOCK_PATH" "$OWNER" "$CREATED_EPOCH" "$CREATED_UTC" "$AGE_SECONDS" "$STALE" "$STALE_AFTER_SECONDS"',
        ]
        script = "\n".join(lines)
        validate_shell_script(script)
        return script

    def _build_remote_lock_cleanup_script(self, *, lock_path: str, stale_after_seconds: int) -> str:
        lines = [
            "set -euo pipefail",
            f"LOCK_PATH={shell_quote(lock_path)}",
            f"STALE_AFTER_SECONDS={int(stale_after_seconds)}",
            'if [ ! -d "$LOCK_PATH" ]; then',
            '  printf "__LOCK_CLEANUP__ status=absent cleaned=0 path=%s reason=lock_absent stale=0 stale_after_seconds=%s\n" "$LOCK_PATH" "$STALE_AFTER_SECONDS"',
            '  exit 0',
            'fi',
            'OWNER="unknown"',
            'if [ -f "$LOCK_PATH/owner.run_id" ]; then OWNER=$(tr -d "\\n" < "$LOCK_PATH/owner.run_id" 2>/dev/null || printf unknown); fi',
            'CREATED_EPOCH=""',
            'if [ -f "$LOCK_PATH/created_at_epoch" ]; then CREATED_EPOCH=$(tr -d "\\n" < "$LOCK_PATH/created_at_epoch" 2>/dev/null || printf ""); fi',
            'if [ -z "$CREATED_EPOCH" ]; then CREATED_EPOCH=$(stat -c %Y "$LOCK_PATH" 2>/dev/null || printf 0); fi',
            'CREATED_UTC=""',
            'if [ -f "$LOCK_PATH/created_at_utc" ]; then CREATED_UTC=$(tr -d "\\n" < "$LOCK_PATH/created_at_utc" 2>/dev/null || printf ""); fi',
            'NOW_EPOCH=$(date -u +%s 2>/dev/null || printf 0)',
            'AGE_SECONDS=-1',
            'STALE=0',
            'if [[ "$CREATED_EPOCH" =~ ^[0-9]+$ ]] && [[ "$NOW_EPOCH" =~ ^[0-9]+$ ]] && [ "$NOW_EPOCH" -ge "$CREATED_EPOCH" ]; then',
            '  AGE_SECONDS=$((NOW_EPOCH - CREATED_EPOCH))',
            '  if [ "$AGE_SECONDS" -ge "$STALE_AFTER_SECONDS" ]; then STALE=1; fi',
            'fi',
            'if [ "$STALE" != "1" ]; then',
            '  printf "__LOCK_CLEANUP__ status=not_stale cleaned=0 path=%s reason=not_stale owner=%s created_at_epoch=%s created_at_utc=%s age_seconds=%s stale=%s stale_after_seconds=%s\n" "$LOCK_PATH" "$OWNER" "$CREATED_EPOCH" "$CREATED_UTC" "$AGE_SECONDS" "$STALE" "$STALE_AFTER_SECONDS"',
            '  exit 44',
            'fi',
            'rm -rf "$LOCK_PATH"',
            'printf "__LOCK_CLEANUP__ status=cleaned cleaned=1 path=%s reason=stale_removed owner=%s created_at_epoch=%s created_at_utc=%s age_seconds=%s stale=%s stale_after_seconds=%s\n" "$LOCK_PATH" "$OWNER" "$CREATED_EPOCH" "$CREATED_UTC" "$AGE_SECONDS" "$STALE" "$STALE_AFTER_SECONDS"',
        ]
        script = "\n".join(lines)
        validate_shell_script(script)
        return script

    def _parse_named_marker(self, output: str, prefix: str) -> Optional[Dict[str, str]]:
        for line in output.splitlines():
            if not line.startswith(prefix + " "):
                continue
            marker: Dict[str, str] = {}
            for chunk in line.split()[1:]:
                if "=" not in chunk:
                    continue
                key, value = chunk.split("=", 1)
                marker[key] = value
            return marker
        return None

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
                payload["returncode"] = 0
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
        run_id: str,
        remote_install: str,
        remote_tmp: str,
        backup_dir: str,
        sanity_cmd: Optional[str],
        keep_tmp: bool,
        no_backup: bool,
    ) -> str:
        lines = [
            "set -euo pipefail",
            f"RUN_ID={shell_quote(run_id)}",
            f"REMOTE_INSTALL={shell_quote(remote_install)}",
            f"REMOTE_TMP={shell_quote(remote_tmp)}",
            f"BACKUP_DIR={shell_quote(backup_dir)}",
            'STAGE_DIR=$(mktemp -d "/tmp/deploy_stage.${RUN_ID}.XXXXXX")',
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


def build_bundle(source_dir: Path, run_id: str) -> Path:
    temp_dir = Path(tempfile.mkdtemp(prefix=f"deploy_bundle_{run_id}_"))
    bundle_path = temp_dir / f"{source_dir.name}_{run_id}.tar.gz"
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


def build_ssh_command(
    target: str,
    remote_args: List[str],
    *,
    batch_mode: bool = False,
    connect_timeout: Optional[int] = None,
) -> List[str]:
    remote_command = " ".join(shell_quote(arg) for arg in remote_args)
    cmd = ["ssh"]
    if batch_mode:
        cmd.extend(["-o", "BatchMode=yes"])
    if connect_timeout is not None:
        cmd.extend(["-o", f"ConnectTimeout={connect_timeout}"])
    cmd.extend([target, remote_command])
    return cmd


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


def parse_int(value: Optional[str]) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except Exception:
        return None


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


def make_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "_" + uuid.uuid4().hex[:8]


def make_remote_lock_path(install_path: str) -> str:
    leaf = Path(install_path).name or "root"
    safe_leaf = "".join(ch if ch.isalnum() else "_" for ch in leaf).strip("_") or "path"
    digest = hashlib.sha256(install_path.encode("utf-8")).hexdigest()[:12]
    return f"/tmp/deploy_module_multi_machine_locks/{safe_leaf}.{digest}.lock"


def shell_quote(value: str) -> str:
    return shlex.quote(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Déploiement multi-machines de modules via SSH.")
    parser.add_argument("command", choices=["status", "plan", "preflight", "deploy", "sanity"], help="Action à exécuter")
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
    parser.add_argument(
        "--lock-stale-after-seconds",
        type=int,
        default=DEFAULT_LOCK_STALE_AFTER_SECONDS,
        help="Seuil stale lock en secondes (défaut: 3600)",
    )
    parser.add_argument(
        "--cleanup-stale-lock",
        action="store_true",
        help="Tenter un cleanup d'un lock stale avant le deploy si le lock cible est stale",
    )
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
    if args.command == "preflight":
        if not args.module_name or not args.source_dir:
            raise DeployError("--module-name et --source-dir sont requis pour preflight.")
        return deployer.run_preflight()
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
