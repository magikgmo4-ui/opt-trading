from __future__ import annotations

import os
from pathlib import Path

import yaml


MODULE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = MODULE_DIR / "config" / "mimo_open_observer.yaml"


def load_config(config_path: str | Path | None = None) -> dict:
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    if not path.is_file():
        raise FileNotFoundError(f"config not found: {path}")

    with open(path, "r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)

    _validate(cfg)
    return cfg


def _validate(cfg: dict) -> None:
    symbol = cfg.get("symbol")
    if symbol != "XAUUSD":
        raise ValueError(f"unexpected symbol: {symbol!r}, expected 'XAUUSD'")

    tz = cfg.get("timezone")
    if tz != "America/Montreal":
        raise ValueError(f"unexpected timezone: {tz!r}, expected 'America/Montreal'")

    windows = cfg.get("windows", {})
    if "open_1800" not in windows:
        raise ValueError("missing windows.open_1800")

    scope = cfg.get("scope", {})
    if scope.get("type") != "M1x5":
        raise ValueError(f"unexpected scope.type: {scope.get('type')!r}, expected 'M1x5'")

    sampling = cfg.get("sampling", {})
    horizons = sampling.get("horizons_minutes")
    if horizons != [30, 60]:
        raise ValueError(
            f"unexpected sampling.horizons_minutes: {horizons!r}, expected [30, 60]"
        )
