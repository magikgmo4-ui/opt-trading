#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"ERROR: missing dependency pyyaml: {exc}", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
PROVIDERS_PATH = CONFIG_DIR / "providers_policy.yaml"
MATRIX_PATH = CONFIG_DIR / "agent_model_matrix.yaml"
REQUIRED_AGENTS = ["orchestrateur", "builder", "reviewer", "lab"]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: root must be a mapping")
    return data


def load_config() -> tuple[dict[str, Any], dict[str, Any]]:
    return load_yaml(PROVIDERS_PATH), load_yaml(MATRIX_PATH)


def validate() -> list[str]:
    providers_cfg, matrix_cfg = load_config()
    errors: list[str] = []

    providers = providers_cfg.get("providers")
    if not isinstance(providers, dict):
        errors.append("providers_policy.yaml: 'providers' missing or invalid")
        return errors

    agents = matrix_cfg.get("agents")
    if not isinstance(agents, dict):
        errors.append("agent_model_matrix.yaml: 'agents' missing or invalid")
        return errors

    allowed = {name for name, cfg in providers.items() if isinstance(cfg, dict) and cfg.get("allowed") is True}

    for agent in REQUIRED_AGENTS:
        if agent not in agents:
            errors.append(f"agent missing: {agent}")
            continue
        cfg = agents[agent]
        if not isinstance(cfg, dict):
            errors.append(f"agent invalid mapping: {agent}")
            continue
        for section in ("primary", "fallback"):
            sec = cfg.get(section)
            if not isinstance(sec, dict):
                errors.append(f"{agent}: missing section {section}")
                continue
            provider = sec.get("provider")
            model = sec.get("model")
            if provider not in allowed:
                errors.append(f"{agent}: {section}.provider not allowed -> {provider}")
            if not isinstance(model, str) or not model.strip():
                errors.append(f"{agent}: {section}.model missing/empty")
        limits = cfg.get("limits")
        if not isinstance(limits, dict):
            errors.append(f"{agent}: limits missing")
            continue
        temp = limits.get("temperature")
        top_p = limits.get("top_p")
        max_tokens = limits.get("max_output_tokens")
        if not isinstance(temp, (int, float)) or not (0 <= temp <= 1):
            errors.append(f"{agent}: temperature must be between 0 and 1")
        if not isinstance(top_p, (int, float)) or not (0 < top_p <= 1):
            errors.append(f"{agent}: top_p must be > 0 and <= 1")
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            errors.append(f"{agent}: max_output_tokens must be > 0")
    return errors


def build_status() -> dict[str, Any]:
    providers_cfg, matrix_cfg = load_config()
    providers = providers_cfg.get("providers", {})
    agents = matrix_cfg.get("agents", {})
    allowed_providers = sorted(
        name for name, cfg in providers.items() if isinstance(cfg, dict) and cfg.get("allowed") is True
    )
    return {
        "module": "model_provider_openclaw",
        "policy_version": providers_cfg.get("policy_version"),
        "matrix_version": matrix_cfg.get("matrix_version"),
        "default_strategy": providers_cfg.get("default_strategy"),
        "allowed_providers": allowed_providers,
        "agents": agents,
    }


def print_status() -> int:
    status = build_status()
    print("MODULE: model_provider_openclaw")
    print(f"POLICY_VERSION: {status['policy_version']}")
    print(f"MATRIX_VERSION: {status['matrix_version']}")
    print(f"DEFAULT_STRATEGY: {status['default_strategy']}")
    print("ALLOWED_PROVIDERS:")
    for provider in status["allowed_providers"]:
        print(f"- {provider}")
    print("AGENTS:")
    for agent, cfg in status["agents"].items():
        primary = cfg.get("primary", {})
        fallback = cfg.get("fallback", {})
        limits = cfg.get("limits", {})
        print(f"- {agent}")
        print(f"  primary : {primary.get('provider')} / {primary.get('model')}")
        print(f"  fallback: {fallback.get('provider')} / {fallback.get('model')}")
        print(
            "  limits  : "
            f"temperature={limits.get('temperature')}, "
            f"top_p={limits.get('top_p')}, "
            f"max_output_tokens={limits.get('max_output_tokens')}, "
            f"reasoning_mode={limits.get('reasoning_mode')}"
        )
    return 0


def print_agent(agent: str) -> int:
    status = build_status()
    agents = status["agents"]
    if agent not in agents:
        print(f"ERROR: unknown agent: {agent}", file=sys.stderr)
        return 1
    print(json.dumps({agent: agents[agent]}, indent=2, ensure_ascii=False))
    return 0


def export_json() -> int:
    print(json.dumps(build_status(), indent=2, ensure_ascii=False))
    return 0


def run_sanity() -> int:
    missing = [str(p) for p in (PROVIDERS_PATH, MATRIX_PATH) if not p.exists()]
    if missing:
        print("SANITY: FAIL")
        for item in missing:
            print(f"- missing file: {item}")
        return 1

    errors = validate()
    if errors:
        print("SANITY: FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("SANITY: PASS")
    print("- providers policy readable")
    print("- agent matrix readable")
    print("- all required agents present")
    print("- primary/fallback providers allowed")
    print("- limits valid")
    return 0


def usage() -> int:
    print(
        "Usage: model_provider_openclaw.py "
        "[status|sanity|show-agent <name>|export-json]"
    )
    return 1


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        return usage()
    cmd = argv[1]
    if cmd == "status":
        return print_status()
    if cmd == "sanity":
        return run_sanity()
    if cmd == "show-agent":
        if len(argv) < 3:
            print("ERROR: missing agent name", file=sys.stderr)
            return 1
        return print_agent(argv[2])
    if cmd == "export-json":
        return export_json()
    return usage()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
