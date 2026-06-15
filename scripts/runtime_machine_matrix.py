import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAP_PATH = PROJECT_ROOT / "config" / "machine_runtime_map.yml"
SYSTEMD_DIR = PROJECT_ROOT / "deploy" / "systemd"


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise RuntimeError(f"YAML root must be a mapping: {path}")
    return data


def _stringify_items(items: list[Any], key: str | None = None) -> list[str]:
    out: list[str] = []
    for item in items or []:
        if isinstance(item, str):
            out.append(item)
            continue
        if isinstance(item, dict):
            if key and item.get(key):
                out.append(str(item[key]))
                continue
            label = item.get("label") or item.get("path") or item.get("host") or item.get("port")
            if label is not None:
                out.append(str(label))
    return out


def _port_labels(items: list[dict[str, Any]]) -> list[str]:
    out: list[str] = []
    for item in items or []:
        if not isinstance(item, dict):
            continue
        label = item.get("label", "port")
        host = item.get("host", "127.0.0.1")
        port = item.get("port", "?")
        out.append(f"{label}:{host}:{port}")
    return out


def _unit_paths(unit_names: list[str]) -> list[str]:
    out: list[str] = []
    for name in unit_names:
        path = SYSTEMD_DIR / name
        if path.exists():
            out.append(path.relative_to(PROJECT_ROOT).as_posix())
    return out


def _activation_surfaces(machine: str, scope: dict[str, Any]) -> list[str]:
    surfaces = ["config/machine_runtime_map.yml", "modules/runtime_health/machine_map.py"]
    os_family = str(scope.get("os_family", "linux")).lower()
    unit_names = [
        *scope.get("required_services", []),
        *scope.get("optional_services", []),
        *scope.get("required_timers", []),
        *scope.get("optional_timers", []),
    ]
    surfaces.extend(_unit_paths([str(name) for name in unit_names]))

    if os_family == "windows":
        windows_helpers = [
            PROJECT_ROOT / "scripts" / "runtime_healthcheck.ps1",
            PROJECT_ROOT / "scripts" / "install_windows_runtime_health_task.ps1",
        ]
        if machine == "cursor-ai":
            windows_helpers.extend([
                PROJECT_ROOT / "modules" / "tradingview_observer" / "cmd.ps1",
                PROJECT_ROOT / "modules" / "tradingview_observer" / "agent" / "tv_agent.ps1",
            ])
        for path in windows_helpers:
            if path.exists():
                surfaces.append(path.relative_to(PROJECT_ROOT).as_posix())
    return sorted(dict.fromkeys(surfaces))


def build_records(map_path: Path) -> list[dict[str, Any]]:
    data = _read_yaml(map_path)
    machines = data.get("machines", {})
    if not isinstance(machines, dict):
        raise RuntimeError("machines must be a mapping")

    records: list[dict[str, Any]] = []
    for machine, scope in machines.items():
        if not isinstance(scope, dict):
            continue
        os_family = str(scope.get("os_family", "linux")).lower()
        required_services = [str(x) for x in scope.get("required_services", [])]
        optional_services = [str(x) for x in scope.get("optional_services", [])]
        required_timers = [str(x) for x in scope.get("required_timers", [])]
        optional_timers = [str(x) for x in scope.get("optional_timers", [])]
        record = {
            "machine": machine,
            "role": scope.get("role", "unknown"),
            "os_family": os_family,
            "description": scope.get("description", ""),
            "activation_model": "windows_task" if os_family == "windows" else "systemd_or_manual",
            "required_services": required_services,
            "optional_services": optional_services,
            "required_timers": required_timers,
            "optional_timers": optional_timers,
            "required_ports": _port_labels(scope.get("required_ports", [])),
            "optional_ports": _port_labels(scope.get("optional_ports", [])),
            "required_paths": _stringify_items(scope.get("required_paths", []), key="path"),
            "optional_paths": _stringify_items(scope.get("optional_paths", []), key="path"),
            "required_venvs": _stringify_items(scope.get("required_venvs", []), key="path"),
            "required_venvs_windows": [str(x) for x in scope.get("required_venvs_windows", [])],
            "required_env": [str(x) for x in scope.get("required_env", [])],
            "optional_env": [str(x) for x in scope.get("optional_env", [])],
            "forbidden_services": [str(x) for x in scope.get("forbidden_services", [])],
            "activation_surfaces": _activation_surfaces(machine, scope),
        }
        records.append(record)
    return records


def render_markdown(records: list[dict[str, Any]]) -> str:
    lines = [
        "# Runtime Machine Matrix",
        "",
        "| Machine | Role | OS | Required runtimes | Optional runtimes | Ports | Activation surfaces |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for record in records:
        required = record["required_services"] + record["required_timers"]
        optional = record["optional_services"] + record["optional_timers"]
        ports = record["required_ports"] + record["optional_ports"]
        surfaces = record["activation_surfaces"]
        lines.append(
            "| {machine} | {role} | {os_family} | {required} | {optional} | {ports} | {surfaces} |".format(
                machine=record["machine"],
                role=record["role"],
                os_family=record["os_family"],
                required="<br>".join(required) or "-",
                optional="<br>".join(optional) or "-",
                ports="<br>".join(ports) or "-",
                surfaces="<br>".join(surfaces) or "-",
            )
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read the canonical machine runtime map and render a machine/runtime matrix."
    )
    parser.add_argument("--map", dest="map_path", default=str(DEFAULT_MAP_PATH))
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--machine", action="append", default=[])
    args = parser.parse_args()

    records = build_records(Path(args.map_path))
    if args.machine:
        wanted = set(args.machine)
        records = [record for record in records if record["machine"] in wanted]

    if args.format == "json":
        json.dump(records, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(render_markdown(records))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
