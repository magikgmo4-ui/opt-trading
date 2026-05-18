from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .types import StrategyRegistryEntry


def load_strategy_registry(registry_path: str | Path) -> list[StrategyRegistryEntry]:
    path = Path(registry_path)
    if not path.exists():
        raise FileNotFoundError(f"Strategy registry not found: {path}")

    entries: list[StrategyRegistryEntry] = []

    for line in path.read_text(encoding="utf-8").splitlines():
        if "|" not in line:
            continue
        if "strategy_id" in line or "---" in line:
            continue

        parts = [p.strip().strip("`") for p in line.strip().strip("|").split("|")]
        if len(parts) < 3:
            continue

        strategy_id = parts[0]
        version = parts[1] if len(parts) > 1 else ""
        lifecycle = parts[2] if len(parts) > 2 else ""
        runtime = parts[3] if len(parts) > 3 else None

        if strategy_id:
            entries.append(
                StrategyRegistryEntry(
                    strategy_id=strategy_id,
                    version=version,
                    lifecycle=lifecycle,
                    runtime=runtime,
                )
            )

    return entries


def iter_strategy_ids(entries: Iterable[StrategyRegistryEntry]) -> set[str]:
    return {entry.strategy_id for entry in entries}
