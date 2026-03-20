from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from collectors_core import ConfigurationError, load_config_layers


@dataclass(frozen=True)
class ModulePaths:
    module_dir: Path
    runtime_dir: Path
    logs_dir: Path
    outputs_dir: Path
    raw_dir: Path
    normalized_dir: Path
    snapshots_dir: Path
    manifest_path: Path
    status_path: Path
    latest_path: Path
    events_path: Path
    errors_path: Path


@dataclass(frozen=True)
class CoinGeckoRuntimeConfig:
    module_id: str
    provider_id: str
    contract_version: str
    schema_version: str
    api_plan: str
    api_base_url: str
    api_timeout_seconds: int
    api_user_agent: str
    api_key: str | None
    collection_vs_currency: str
    collection_coin_ids: tuple[str, ...]
    collection_price_change_percentage: tuple[str, ...]
    collection_sparkline: bool
    collection_locale: str
    collection_precision: str
    freshness_max_age_seconds: int
    paths: ModulePaths

    @property
    def auth_header_name(self) -> str:
        if self.api_plan == "demo":
            return "x-cg-demo-api-key"
        if self.api_plan == "pro":
            return "x-cg-pro-api-key"
        raise ConfigurationError(f"Unsupported CoinGecko plan: {self.api_plan}")


def load_runtime_config(module_dir: Path) -> CoinGeckoRuntimeConfig:
    raw = load_config_layers(module_dir, "collector_coingecko")

    module_section = _require_section(raw, "module")
    contract_section = _require_section(raw, "contract")
    api_section = _require_section(raw, "api")
    collection_section = _require_section(raw, "collection")
    freshness_section = _require_section(raw, "freshness")
    paths_section = _require_section(raw, "paths")

    module_id = _require_string(module_section, "module_id")
    provider_id = _require_string(module_section, "provider_id")
    contract_version = _require_string(contract_section, "contract_version")
    schema_version = _require_string(contract_section, "schema_version")

    api_plan = _require_string(api_section, "plan").lower()
    api_base_url = _require_string(api_section, "base_url")
    api_timeout_seconds = _require_int(api_section, "timeout_seconds")
    api_user_agent = _require_string(api_section, "user_agent")
    api_key = _optional_string(api_section, "key")

    collection_vs_currency = _require_string(collection_section, "vs_currency").lower()
    collection_coin_ids = _require_string_list(collection_section, "coin_ids")
    collection_price_change_percentage = _require_string_list(collection_section, "price_change_percentage")
    collection_sparkline = _require_bool(collection_section, "sparkline")
    collection_locale = _require_string(collection_section, "locale")
    collection_precision = _require_string(collection_section, "precision")
    freshness_max_age_seconds = _require_int(freshness_section, "max_age_seconds")

    runtime_dir = _resolve_path(module_dir, _require_string(paths_section, "runtime_dir"))
    logs_dir = _resolve_path(module_dir, _require_string(paths_section, "logs_dir"))
    outputs_dir = _resolve_path(module_dir, _require_string(paths_section, "outputs_dir"))
    raw_dir = _resolve_path(module_dir, _require_string(paths_section, "raw_dir"))
    normalized_dir = _resolve_path(module_dir, _require_string(paths_section, "normalized_dir"))
    snapshots_dir = _resolve_path(module_dir, _require_string(paths_section, "snapshots_dir"))

    return CoinGeckoRuntimeConfig(
        module_id=module_id,
        provider_id=provider_id,
        contract_version=contract_version,
        schema_version=schema_version,
        api_plan=api_plan,
        api_base_url=api_base_url,
        api_timeout_seconds=api_timeout_seconds,
        api_user_agent=api_user_agent,
        api_key=api_key,
        collection_vs_currency=collection_vs_currency,
        collection_coin_ids=collection_coin_ids,
        collection_price_change_percentage=collection_price_change_percentage,
        collection_sparkline=collection_sparkline,
        collection_locale=collection_locale,
        collection_precision=collection_precision,
        freshness_max_age_seconds=freshness_max_age_seconds,
        paths=ModulePaths(
            module_dir=module_dir,
            runtime_dir=runtime_dir,
            logs_dir=logs_dir,
            outputs_dir=outputs_dir,
            raw_dir=raw_dir,
            normalized_dir=normalized_dir,
            snapshots_dir=snapshots_dir,
            manifest_path=outputs_dir / "manifest.json",
            status_path=outputs_dir / "status.json",
            latest_path=outputs_dir / "latest.json",
            events_path=outputs_dir / "events.jsonl",
            errors_path=outputs_dir / "errors.jsonl",
        ),
    )


def validate_runtime_requirements(config: CoinGeckoRuntimeConfig) -> None:
    if not config.api_key:
        raise ConfigurationError("Missing required secret env var: COLLECTOR_COINGECKO__API__KEY")
    if not config.collection_coin_ids:
        raise ConfigurationError("collection.coin_ids must contain at least one coin id")


def _resolve_path(module_dir: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return module_dir / path


def _require_section(raw: dict[str, Any], key: str) -> dict[str, Any]:
    value = raw.get(key)
    if not isinstance(value, dict):
        raise ConfigurationError(f"Missing required section: {key}")
    return value


def _require_string(section: dict[str, Any], key: str) -> str:
    value = section.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"Missing required string config: {key}")
    return value.strip()


def _optional_string(section: dict[str, Any], key: str) -> str | None:
    value = section.get(key)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"Config value must be a non-empty string when set: {key}")
    return value.strip()


def _require_int(section: dict[str, Any], key: str) -> int:
    value = section.get(key)
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.isdigit():
            return int(stripped)
    raise ConfigurationError(f"Config value must be an integer: {key}")


def _require_bool(section: dict[str, Any], key: str) -> bool:
    value = section.get(key)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes", "on"}:
            return True
        if lowered in {"false", "0", "no", "off"}:
            return False
    raise ConfigurationError(f"Config value must be a boolean: {key}")


def _require_string_list(section: dict[str, Any], key: str) -> tuple[str, ...]:
    value = section.get(key)
    items: list[str]
    if isinstance(value, list):
        items = [str(item).strip() for item in value if str(item).strip()]
    elif isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("["):
            decoded = json.loads(stripped)
            if not isinstance(decoded, list):
                raise ConfigurationError(f"Config value must decode to a list: {key}")
            items = [str(item).strip() for item in decoded if str(item).strip()]
        else:
            items = [item.strip() for item in stripped.split(",") if item.strip()]
    else:
        raise ConfigurationError(f"Config value must be a list of strings: {key}")

    if not items:
        raise ConfigurationError(f"Config list must not be empty: {key}")
    return tuple(items)
