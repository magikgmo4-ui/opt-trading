"""Stop conditions evaluated before finalizing a pilot run."""
from __future__ import annotations

from typing import Any


class StopConditionTriggered(RuntimeError):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


def check(contract: dict[str, Any]) -> None:
    """Raise StopConditionTriggered if any stop condition is met."""
    stops = contract.get("stop_conditions", [])

    for condition in stops:
        if isinstance(condition, dict):
            name = condition.get("name", "")
            triggered = condition.get("triggered", False)
        elif isinstance(condition, str):
            name = condition
            triggered = True
        else:
            continue

        if triggered:
            raise StopConditionTriggered(name)

    if contract.get("mode") != "dry_run":
        raise StopConditionTriggered("mode_not_dry_run")

    if not contract.get("human_gate_required"):
        raise StopConditionTriggered("human_gate_disabled")
