#!/usr/bin/env python3
"""
machine_map.py — load machine_runtime_map.yml and resolve scope for current host.

Usage:
    from modules.runtime_health.machine_map import MachineMap
    mm = MachineMap.load()
    scope = mm.scope_for("db-layer")
"""

import os
import socket
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml as _yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_MAP_PATH = _REPO_ROOT / "config" / "machine_runtime_map.yml"

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"


class MachineMap:
    def __init__(self, data: Dict[str, Any], map_path: str = ""):
        self._data = data
        self.map_path = map_path
        self.version: int = data.get("version", 1)
        self.project: str = data.get("project", "opt-trading")
        self.data_dir: str = data.get("data_dir", "/opt/trading/data/runtime_health")
        self._machines: Dict[str, Dict] = data.get("machines", {})

    @classmethod
    def load(cls, path: Optional[str] = None) -> "MachineMap":
        resolved = Path(path) if path else _DEFAULT_MAP_PATH
        if not resolved.exists():
            return cls(_EMPTY_MAP, map_path=str(resolved))
        if not _HAS_YAML:
            return cls(_EMPTY_MAP, map_path=str(resolved))
        try:
            with open(resolved, encoding="utf-8") as f:
                data = _yaml.safe_load(f)
            if isinstance(data, dict):
                return cls(data, map_path=str(resolved))
        except Exception:
            pass
        return cls(_EMPTY_MAP, map_path=str(resolved))

    def known_machines(self) -> List[str]:
        return list(self._machines.keys())

    def scope_for(self, machine: str) -> Optional[Dict[str, Any]]:
        return self._machines.get(machine)

    def scope_for_current_host(self) -> tuple:
        """Return (hostname, machine_name, scope_dict).
        machine_name may differ from hostname (e.g. MACHINE_ROLE env override).
        """
        override = os.environ.get("MACHINE_ROLE", "").strip()
        hostname = socket.gethostname()
        machine_name = override if override else hostname
        scope = self.scope_for(machine_name)
        if scope is None and machine_name != hostname:
            scope = self.scope_for(hostname)
            machine_name = hostname
        return hostname, machine_name, scope

    def check_forbidden_services(self, scope: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Return check results for forbidden services that are currently active."""
        from modules.runtime_health.healthcheck import _run
        forbidden = scope.get("forbidden_services", [])
        results = []
        for name in forbidden:
            rc, active, _ = _run(["systemctl", "is-active", name])
            is_active = active == "active"
            results.append({
                "check": f"forbidden_service:{name}",
                "service": name,
                "active": active,
                "forbidden": True,
                "status": FAIL if is_active else PASS,
                "detail": "FORBIDDEN service is active" if is_active else "ok (not running)",
            })
        return results

    def build_config_from_scope(self, scope: Dict[str, Any], base_cfg: Dict[str, Any]) -> Dict[str, Any]:
        """Merge machine scope into healthcheck base config."""
        cfg = dict(base_cfg)

        # Services
        cfg["services"] = {
            "required": scope.get("required_services", []),
            "optional": scope.get("optional_services", []),
        }

        # Timers
        cfg["timers"] = {
            "required": scope.get("required_timers", []),
            "optional": scope.get("optional_timers", []),
        }

        # Venvs: convert list of {path, label, required} dicts
        raw_venvs = scope.get("required_venvs", [])
        cfg["venvs"] = []
        for v in raw_venvs:
            if isinstance(v, str):
                cfg["venvs"].append({"path": v, "label": v, "required": True})
            else:
                cfg["venvs"].append({
                    "path": v.get("path", ""),
                    "label": v.get("label", v.get("path", "")),
                    "required": v.get("required", True),
                })

        # Ports
        cfg["ports"] = {
            "required": scope.get("required_ports", []),
            "optional": scope.get("optional_ports", []),
        }

        # Paths
        cfg["paths"] = {
            "required": scope.get("required_paths", []),
            "optional": scope.get("optional_paths", []),
        }

        # Env
        cfg["env"] = {
            "required": scope.get("required_env", []),
            "optional": scope.get("optional_env", []),
        }

        # Logs: keep journal_units from scope
        log_units = scope.get("log_units", [])
        cfg["logs"] = dict(base_cfg.get("logs", {}))
        cfg["logs"]["journal_units"] = log_units

        # HTTP checks — override when explicitly set in scope
        if "optional_http_checks" in scope or "required_http_checks" in scope:
            cfg["http"] = {
                "required": scope.get("required_http_checks", []),
                "optional": scope.get("optional_http_checks", []),
            }

        # Artifacts — override when explicitly set in scope
        if "optional_artifact_paths" in scope:
            cfg["artifacts"] = {
                "optional": scope.get("optional_artifact_paths", []),
            }

        # Log files — override when explicitly set in scope
        if "optional_log_files" in scope:
            cfg["logs"]["log_files"] = {
                "optional": scope.get("optional_log_files", []),
            }

        # Orchestrator tmux sessions — override when explicitly set in scope
        if "optional_tmux_sessions" in scope:
            cfg["orchestrator"] = {
                "tmux_sessions": {
                    "optional": scope.get("optional_tmux_sessions", []),
                }
            }

        return cfg


_EMPTY_MAP: Dict[str, Any] = {
    "version": 1,
    "project": "opt-trading",
    "data_dir": "/opt/trading/data/runtime_health",
    "machines": {},
}


def check_machine_identity(
    hostname: str,
    machine_name: str,
    scope: Optional[Dict],
    map_version: int,
    map_path: str,
) -> Dict[str, Any]:
    """Produce the MACHINE_IDENTITY check block."""
    known = scope is not None
    return {
        "check": "machine_identity",
        "hostname": hostname,
        "machine_name": machine_name,
        "role": scope.get("role", "unknown") if scope else "unknown",
        "description": scope.get("description", "") if scope else "",
        "scope_loaded": known,
        "map_version": map_version,
        "map_path": map_path,
        "status": PASS if known else WARN,
        "detail": "scope found in machine_runtime_map" if known else f"machine '{machine_name}' not in map",
    }
