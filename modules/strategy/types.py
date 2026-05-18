from dataclasses import dataclass


@dataclass(frozen=True)
class StrategyRegistryEntry:
    strategy_id: str
    version: str
    lifecycle: str
    runtime: str | None = None
