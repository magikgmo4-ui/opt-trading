from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


class TrustTier(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


@dataclass
class Channel:
    alias: str
    kind: str
    title: str
    trust_tier: TrustTier
    categories: list[str] = field(default_factory=list)
    expected_parsers: list[str] = field(default_factory=list)
    symbols_scope: list[str] = field(default_factory=list)
    timeframes_scope: list[str] = field(default_factory=list)
    allow_forwarded: bool = False
    allow_media: bool = True
    enabled: bool = False
    notes: str = ""


@dataclass
class ChannelRegistry:
    version: int
    updated_at: str
    channels: list[Channel] = field(default_factory=list)

    def enabled_channels(self) -> list[Channel]:
        return [c for c in self.channels if c.enabled]

    def by_tier(self, tier: TrustTier) -> list[Channel]:
        return [c for c in self.channels if c.trust_tier == tier]

    def by_category(self, category: str) -> list[Channel]:
        return [c for c in self.channels if category in c.categories]

    def by_alias(self, alias: str) -> Optional[Channel]:
        for c in self.channels:
            if c.alias == alias:
                return c
        return None
