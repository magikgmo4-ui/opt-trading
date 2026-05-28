"""Handoff contract schema for the semi-auto pilot."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {
    "run_id",
    "go_id",
    "parent_go_id",
    "mode",
    "input_prompt_path",
    "actions_planned",
    "actions_executed",
    "stop_conditions",
    "human_gate_required",
    "verdict",
    "next_go",
}

ALLOWED_MODES = {"dry_run"}


class ContractError(ValueError):
    pass


def validate(contract: dict[str, Any]) -> None:
    missing = REQUIRED_FIELDS - contract.keys()
    if missing:
        raise ContractError(f"missing fields: {sorted(missing)}")

    if contract["mode"] not in ALLOWED_MODES:
        raise ContractError(f"mode must be one of {ALLOWED_MODES}, got {contract['mode']!r}")

    if not contract.get("human_gate_required"):
        raise ContractError("human_gate_required must be true")

    if not contract.get("verdict"):
        raise ContractError("verdict must not be empty")

    if not isinstance(contract.get("actions_planned"), list):
        raise ContractError("actions_planned must be a list")

    if not isinstance(contract.get("actions_executed"), list):
        raise ContractError("actions_executed must be a list")

    if not isinstance(contract.get("stop_conditions"), list):
        raise ContractError("stop_conditions must be a list")


def load(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text())
    validate(data)
    return data


def build_empty(
    run_id: str,
    go_id: str,
    parent_go_id: str,
    input_prompt_path: str,
    next_go: str = "",
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "go_id": go_id,
        "parent_go_id": parent_go_id,
        "mode": "dry_run",
        "input_prompt_path": input_prompt_path,
        "actions_planned": [],
        "actions_executed": [],
        "stop_conditions": [],
        "human_gate_required": True,
        "verdict": "",
        "next_go": next_go,
    }
