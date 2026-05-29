from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

import yaml

from .models import Channel, ChannelRegistry, TrustTier


_ALIAS_PATTERN = re.compile(r"^TG_SRC_[A-Z0-9_]+$")
_VALID_KINDS = {"channel", "group", "supergroup"}
_VALID_PARSERS = {"trade_claim", "setup", "news", "alpha"}


def load_channel_registry(path: Optional[Path] = None) -> ChannelRegistry:
    if path is None:
        path = Path(__file__).resolve().parent / "channels.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Channel registry not found: {path}")

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Registry must be a YAML mapping")

    version = raw.get("version")
    if version != 1:
        raise ValueError(f"Unsupported registry version: {version}")

    updated_at = raw.get("updated_at", "")

    channels_raw = raw.get("channels", [])
    if not isinstance(channels_raw, list):
        raise ValueError("'channels' must be a list")

    channels = [_parse_channel(c) for c in channels_raw]
    return ChannelRegistry(version=version, updated_at=updated_at, channels=channels)


def _parse_channel(raw: dict) -> Channel:
    alias = raw.get("alias", "")
    if not _ALIAS_PATTERN.match(alias):
        raise ValueError(f"Invalid alias: '{alias}' — must match TG_SRC_[A-Z0-9_]+")

    kind = raw.get("kind", "")
    if kind not in _VALID_KINDS:
        raise ValueError(f"Invalid kind '{kind}' for {alias} — must be one of {_VALID_KINDS}")

    tier_str = raw.get("trust_tier", "")
    try:
        trust_tier = TrustTier(tier_str)
    except ValueError:
        raise ValueError(f"Invalid trust_tier '{tier_str}' for {alias}")

    parsers = raw.get("expected_parsers", [])
    for p in parsers:
        if p not in _VALID_PARSERS:
            raise ValueError(f"Unknown parser '{p}' for {alias}")

    categories = raw.get("categories", [])
    if not categories:
        raise ValueError(f"categories must be non-empty for {alias}")

    if not parsers:
        raise ValueError(f"expected_parsers must be non-empty for {alias}")

    return Channel(
        alias=alias,
        kind=kind,
        title=raw.get("title", ""),
        trust_tier=trust_tier,
        categories=categories,
        expected_parsers=parsers,
        symbols_scope=raw.get("symbols_scope", []),
        timeframes_scope=raw.get("timeframes_scope", []),
        allow_forwarded=bool(raw.get("allow_forwarded", False)),
        allow_media=bool(raw.get("allow_media", True)),
        enabled=bool(raw.get("enabled", False)),
        notes=raw.get("notes", ""),
    )
