import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]

REGISTRY_PATH = PROJECT_ROOT / "registry" / "runtime_execution_contracts.yaml"
MODULES_REGISTRY_PATH = PROJECT_ROOT / "registry" / "modules_registry.yaml"
WRAPPERS_REGISTRY_PATH = PROJECT_ROOT / "registry" / "wrappers_registry.yaml"
MACHINES_REGISTRY_PATH = PROJECT_ROOT / "registry" / "machines_registry.yaml"
MACHINE_RUNTIME_MAP_PATH = PROJECT_ROOT / "config" / "machine_runtime_map.yml"
CODE_REGISTRY_PATH = PROJECT_ROOT / "docs" / "registry" / "CODE_REGISTRY.md"
JOBS_REGISTRY_PATH = PROJECT_ROOT / "docs" / "registry" / "JOBS_REGISTRY.md"


CONTRACT_ID_RE = re.compile(r"^[a-z0-9_]+$")

ALLOWED_EXECUTION_MODES = {
    "on_demand",
    "scheduled",
    "service",
    "timer",
    "ci",
    "worker",
    "library",
    "diagnostic_only",
}

ALLOWED_SIDE_EFFECTS = {
    "read_only",
    "writes_artifacts",
    "writes_logs",
    "writes_registry",
    "writes_runtime_state",
    "network_call",
    "external_api",
    "requires_secret",
    "no_live_trade",
    "live_trade_possible",
    "service_start_stop",
}

ALLOWED_HEALTHCHECK_TYPES = {"none", "runtime_health", "ci", "custom"}

ALLOWED_RISKS = {"low", "medium", "high", "critical"}
ALLOWED_STATUSES = {"active", "candidate", "experimental", "legacy", "blocked", "deprecated"}


def _fail(errors: List[str]) -> None:
    for err in errors:
        print(f"[FAIL] {err}")
    sys.exit(1)


def _read_yaml(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise RuntimeError(f"Error loading YAML {path}: {e}") from e


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _looks_like_secret(s: str) -> Optional[str]:
    patterns = [
        (r"sk-[A-Za-z0-9]{20,}", "openai_like_key"),
        (r"github_pat_[A-Za-z0-9_]{10,}", "github_pat"),
        (r"ghp_[A-Za-z0-9]{20,}", "github_token"),
        (r"AIza[0-9A-Za-z\-_]{20,}", "google_api_key"),
        (r"xox[baprs]-[A-Za-z0-9\-]{10,}", "slack_token"),
        (r"-----BEGIN [A-Z ]+PRIVATE KEY-----", "private_key_block"),
        (r"AKIA[0-9A-Z]{16}", "aws_access_key_id"),
    ]
    for pat, label in patterns:
        if re.search(pat, s):
            return label
    return None


def _is_absolute_path_like(p: str) -> bool:
    if not p:
        return False
    if p.startswith("/"):
        return True
    if re.match(r"^[A-Za-z]:[\\/]", p):
        return True
    if p.startswith("~"):
        return True
    return False


def _collect_modules(modules_registry: Any) -> Set[str]:
    if not isinstance(modules_registry, list):
        return set()
    out: Set[str] = set()
    for item in modules_registry:
        if isinstance(item, dict) and isinstance(item.get("module_name"), str):
            out.add(item["module_name"])
    return out


def _collect_wrappers(wrappers_registry: Any) -> Set[str]:
    if not isinstance(wrappers_registry, list):
        return set()
    out: Set[str] = set()
    for item in wrappers_registry:
        if isinstance(item, dict) and isinstance(item.get("wrapper_name"), str):
            out.add(item["wrapper_name"])
    return out


def _collect_machines(machines_registry: Any) -> Set[str]:
    if not isinstance(machines_registry, list):
        return set()
    out: Set[str] = set()
    for item in machines_registry:
        if isinstance(item, dict) and isinstance(item.get("machine_id"), str):
            out.add(item["machine_id"])
    return out


def _collect_runtime_map_keys(machine_runtime_map: Any) -> Set[str]:
    if not isinstance(machine_runtime_map, dict):
        return set()
    machines = machine_runtime_map.get("machines")
    if not isinstance(machines, dict):
        return set()
    return {k for k in machines.keys() if isinstance(k, str)}


def _collect_ids_from_markdown_table(md: str) -> Set[str]:
    ids: Set[str] = set()
    for line in md.splitlines():
        if "`" not in line or "|" not in line:
            continue
        for token in re.findall(r"`([^`]+)`", line):
            token = token.strip()
            if CONTRACT_ID_RE.match(token):
                ids.add(token)
    return ids


def validate() -> None:
    errors: List[str] = []

    for p in [
        REGISTRY_PATH,
        MODULES_REGISTRY_PATH,
        WRAPPERS_REGISTRY_PATH,
        MACHINES_REGISTRY_PATH,
        MACHINE_RUNTIME_MAP_PATH,
        CODE_REGISTRY_PATH,
        JOBS_REGISTRY_PATH,
    ]:
        if not p.exists():
            errors.append(f"Missing required file: {p.as_posix()}")
    if errors:
        _fail(errors)

    try:
        registry = _read_yaml(REGISTRY_PATH)
        modules_registry = _read_yaml(MODULES_REGISTRY_PATH)
        wrappers_registry = _read_yaml(WRAPPERS_REGISTRY_PATH)
        machines_registry = _read_yaml(MACHINES_REGISTRY_PATH)
        machine_runtime_map = _read_yaml(MACHINE_RUNTIME_MAP_PATH)
        code_registry_md = _read_text(CODE_REGISTRY_PATH)
        jobs_registry_md = _read_text(JOBS_REGISTRY_PATH)
    except Exception as e:
        _fail([str(e)])
        return

    if not isinstance(registry, dict):
        _fail(["runtime_execution_contracts registry must be a YAML mapping at root"])
        return

    schema_version = registry.get("schema_version")
    if not isinstance(schema_version, str) or not schema_version.strip():
        errors.append("root.schema_version must be a non-empty string")

    contracts = registry.get("contracts")
    if not isinstance(contracts, list) or not contracts:
        errors.append("root.contracts must be a non-empty list")
        _fail(errors)
        return

    module_names = _collect_modules(modules_registry)
    wrapper_names = _collect_wrappers(wrappers_registry)
    machine_ids = _collect_machines(machines_registry)
    runtime_map_keys = _collect_runtime_map_keys(machine_runtime_map)
    code_ids = _collect_ids_from_markdown_table(code_registry_md)
    job_ids = _collect_ids_from_markdown_table(jobs_registry_md)

    seen_contract_ids: Set[str] = set()

    for i, c in enumerate(contracts):
        if not isinstance(c, dict):
            errors.append(f"contracts[{i}] must be a mapping")
            continue

        def req_str(field: str) -> Optional[str]:
            v = c.get(field)
            if not isinstance(v, str) or not v.strip():
                errors.append(f"contracts[{i}].{field} must be a non-empty string")
                return None
            return v

        contract_id = req_str("contract_id")
        module_name = req_str("module_name")
        machine_target = req_str("machine_target")
        execution_mode = req_str("execution_mode")
        risk = req_str("risk")
        status = req_str("status")

        if contract_id:
            if not CONTRACT_ID_RE.match(contract_id):
                errors.append(
                    f"contracts[{i}].contract_id must match {CONTRACT_ID_RE.pattern}: {contract_id}"
                )
            if contract_id in seen_contract_ids:
                errors.append(f"Duplicate contract_id: {contract_id}")
            seen_contract_ids.add(contract_id)

        code_id = c.get("code_id")
        if code_id is not None:
            if not isinstance(code_id, str) or not code_id.strip():
                errors.append(f"contracts[{i}].code_id must be null or non-empty string")
            elif code_id not in code_ids:
                errors.append(f"contracts[{i}].code_id not found in CODE_REGISTRY.md: {code_id}")

        job_id = c.get("job_id")
        if job_id is not None:
            if not isinstance(job_id, str) or not job_id.strip():
                errors.append(f"contracts[{i}].job_id must be null or non-empty string")
            elif job_id not in job_ids:
                errors.append(f"contracts[{i}].job_id not found in JOBS_REGISTRY.md: {job_id}")

        wrapper_ids = c.get("wrapper_ids")
        if not isinstance(wrapper_ids, list) or not wrapper_ids:
            errors.append(f"contracts[{i}].wrapper_ids must be a non-empty list")
        else:
            for w in wrapper_ids:
                if not isinstance(w, str) or not w.strip():
                    errors.append(f"contracts[{i}].wrapper_ids contains invalid value")
                    continue
                if w not in wrapper_names:
                    errors.append(f"contracts[{i}].wrapper_id not found in wrappers_registry: {w}")

        runtime_map_key = c.get("runtime_map_key")
        if runtime_map_key is not None:
            if not isinstance(runtime_map_key, str) or not runtime_map_key.strip():
                errors.append(f"contracts[{i}].runtime_map_key must be null or non-empty string")
            elif runtime_map_key not in runtime_map_keys:
                errors.append(
                    f"contracts[{i}].runtime_map_key not found in config/machine_runtime_map.yml: {runtime_map_key}"
                )

        if module_name and module_name not in module_names:
            errors.append(f"contracts[{i}].module_name not found in modules_registry: {module_name}")

        if machine_target and machine_target not in machine_ids:
            errors.append(f"contracts[{i}].machine_target not found in machines_registry: {machine_target}")

        if execution_mode and execution_mode not in ALLOWED_EXECUTION_MODES:
            errors.append(
                f"contracts[{i}].execution_mode must be one of {sorted(ALLOWED_EXECUTION_MODES)}"
            )

        if risk and risk not in ALLOWED_RISKS:
            errors.append(f"contracts[{i}].risk must be one of {sorted(ALLOWED_RISKS)}")

        if status and status not in ALLOWED_STATUSES:
            errors.append(f"contracts[{i}].status must be one of {sorted(ALLOWED_STATUSES)}")

        entrypoint = c.get("entrypoint")
        if entrypoint is not None:
            if not isinstance(entrypoint, str) or not entrypoint.strip():
                errors.append(f"contracts[{i}].entrypoint must be null or non-empty string")
            elif _is_absolute_path_like(entrypoint):
                errors.append(f"contracts[{i}].entrypoint must be repo-relative (not absolute): {entrypoint}")
            else:
                ep_path = PROJECT_ROOT / entrypoint
                if not ep_path.exists():
                    errors.append(f"contracts[{i}].entrypoint not found: {entrypoint}")

        command = c.get("command")
        if command is not None and (not isinstance(command, str) or not command.strip()):
            errors.append(f"contracts[{i}].command must be null or non-empty string")

        inputs = c.get("inputs")
        if not isinstance(inputs, list):
            errors.append(f"contracts[{i}].inputs must be a list")

        outputs = c.get("outputs")
        if not isinstance(outputs, list):
            errors.append(f"contracts[{i}].outputs must be a list")

        side_effects = c.get("side_effects")
        if not isinstance(side_effects, list):
            errors.append(f"contracts[{i}].side_effects must be a list")
        else:
            for se in side_effects:
                if not isinstance(se, str) or not se.strip():
                    errors.append(f"contracts[{i}].side_effects contains invalid value")
                    continue
                if se not in ALLOWED_SIDE_EFFECTS:
                    errors.append(
                        f"contracts[{i}].side_effects contains unsupported value: {se} (allowed={sorted(ALLOWED_SIDE_EFFECTS)})"
                    )

        healthcheck = c.get("healthcheck")
        if not isinstance(healthcheck, dict):
            errors.append(f"contracts[{i}].healthcheck must be a mapping")
        else:
            hc_type = healthcheck.get("type")
            if not isinstance(hc_type, str) or hc_type not in ALLOWED_HEALTHCHECK_TYPES:
                errors.append(
                    f"contracts[{i}].healthcheck.type must be one of {sorted(ALLOWED_HEALTHCHECK_TYPES)}"
                )

            required = healthcheck.get("required")
            if not isinstance(required, bool):
                errors.append(f"contracts[{i}].healthcheck.required must be a boolean")

        tests = c.get("tests")
        if not isinstance(tests, list):
            errors.append(f"contracts[{i}].tests must be a list")
        else:
            for t in tests:
                if not isinstance(t, str) or not t.strip():
                    errors.append(f"contracts[{i}].tests contains invalid value")
                    continue
                if _is_absolute_path_like(t):
                    errors.append(f"contracts[{i}].tests entry must be repo-relative (not absolute): {t}")
                    continue
                t_path = PROJECT_ROOT / t
                if not t_path.exists():
                    errors.append(f"contracts[{i}].tests entry not found: {t}")

        for k, v in c.items():
            if isinstance(v, str):
                label = _looks_like_secret(v)
                if label:
                    errors.append(f"contracts[{i}].{k} contains secret-like pattern ({label})")

    if errors:
        _fail(errors)

    print("[PASS] runtime_execution_contracts registry validation")


if __name__ == "__main__":
    os.chdir(PROJECT_ROOT)
    validate()
