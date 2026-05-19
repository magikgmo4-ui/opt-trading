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
        if len(parts) < 6:
            continue

        strategy_id = parts[1]
        version = parts[2] if len(parts) > 2 else ""
        lifecycle = parts[5] if len(parts) > 5 else ""
        runtime = parts[6] if len(parts) > 6 else None

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
