from __future__ import annotations

import os
from pathlib import PurePosixPath
from typing import Any, Iterable, Mapping


TRUE_VALUES = {"1", "true", "yes", "on"}
FALSE_VALUES = {"0", "false", "no", "off"}
AGGRESSIVE_ACTIVE_ENGINES = {"COINM_SHORT", "USDTM_LONG"}


def _env_value(env: Mapping[str, str], name: str) -> str:
    return str(env.get(name, "") or "").strip()


def _flag_is_true(value: str) -> bool:
    return value.strip().lower() in TRUE_VALUES


def _flag_is_false(value: str) -> bool:
    return value.strip().lower() in FALSE_VALUES


def evaluate_paper_test_runtime_guards(
    *,
    env: Mapping[str, str] | None = None,
    active_engine: str | None = None,
    adapter_names: Iterable[str] | None = None,
) -> dict[str, Any]:
    if env is None:
        env = os.environ
    adapters = set(adapter_names or [])

    runner_mode = _env_value(env, "RUNNER_MODE")
    simulation_mode = _env_value(env, "SIMULATION_MODE")
    trade_allowed = _env_value(env, "TRADE_ALLOWED")
    ledger_path = _env_value(env, "LEDGER_PATH")
    active = (active_engine or "").strip()

    runner_ok = runner_mode.upper() == "PAPER"
    simulation_ok = _flag_is_true(simulation_mode)
    trade_allowed_ok = _flag_is_false(trade_allowed)
    ledger_name = PurePosixPath(ledger_path).name if ledger_path else ""
    ledger_ok = bool(ledger_path) and ledger_name == "ledger_paper.json" and "ledger_live" not in ledger_path.lower()
    active_engine_ok = active == "" or active not in AGGRESSIVE_ACTIVE_ENGINES
    paper_adapter_ok = "paper" in adapters

    guards = {
        "runner_mode": {
            "ok": runner_ok,
            "value": runner_mode or "unset",
            "expected": "PAPER",
        },
        "simulation_mode": {
            "ok": simulation_ok,
            "value": simulation_mode or "unset",
            "expected": "true",
        },
        "trade_allowed": {
            "ok": trade_allowed_ok,
            "value": trade_allowed or "unset",
            "expected": "false",
        },
        "ledger_path": {
            "ok": ledger_ok,
            "value": ledger_path or "unset",
            "expected": "path ending in ledger_paper.json and not ledger_live.json",
        },
        "active_engine": {
            "ok": active_engine_ok,
            "value": active or "unset",
            "expected": "unset or non-aggressive engine",
        },
        "paper_adapter": {
            "ok": paper_adapter_ok,
            "value": "registered" if paper_adapter_ok else "missing",
            "expected": "registered",
        },
    }

    reasons = [
        f"{name}: expected {detail['expected']}, got {detail['value']}"
        for name, detail in guards.items()
        if not detail["ok"]
    ]

    return {
        "ok": not reasons,
        "mode": "PAPER_TEST",
        "guards": guards,
        "reasons": reasons,
    }
