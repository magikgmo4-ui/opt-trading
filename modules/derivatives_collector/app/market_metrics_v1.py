from dataclasses import dataclass, field, asdict
from typing import Optional, List
import json

VALID_COVERAGE_STATUSES = {"full", "partial", "not_proven_runtime_adapter", "spot_only"}
VALID_FRESHNESS_STATES = {"fresh", "stale", "unknown"}
_KNOWN_METRICS = {
    "open_interest", "funding_rate", "volume_futures",
    "long_short_ratio", "liquidations_long", "liquidations_short",
}


@dataclass
class ProviderCoverage:
    status: str
    collectable_metrics: List[str] = field(default_factory=list)
    missing_metrics: List[str] = field(default_factory=list)


@dataclass
class MetricsPayload:
    open_interest: Optional[float] = None
    funding_rate: Optional[float] = None
    volume_futures: Optional[float] = None
    long_short_ratio: Optional[float] = None
    liquidations_long: Optional[float] = None
    liquidations_short: Optional[float] = None


@dataclass
class Refs:
    primary_output: str
    meta_output: str
    latest: str
    status: str


@dataclass
class MarketMetricsV1:
    contract_version: str
    input_class: str
    module_id: str
    symbol: str
    metrics_ts: str
    freshness_state: str
    provider_coverage: ProviderCoverage
    metrics: MetricsPayload
    refs: Refs
    provider_id: Optional[str] = None
    warnings: List[str] = field(default_factory=list)

    def validate(self) -> bool:
        errors = []

        if self.contract_version != "v1":
            errors.append(f"contract_version must be 'v1', got '{self.contract_version}'")

        if self.input_class != "market_metrics.v1":
            errors.append(f"input_class must be 'market_metrics.v1', got '{self.input_class}'")

        if not self.module_id:
            errors.append("module_id must not be empty")

        if not self.symbol:
            errors.append("symbol must not be empty")

        if not self.metrics_ts:
            errors.append("metrics_ts must not be empty")

        if self.freshness_state not in VALID_FRESHNESS_STATES:
            errors.append(
                f"freshness_state must be one of {VALID_FRESHNESS_STATES}, "
                f"got '{self.freshness_state}'"
            )

        if self.provider_coverage.status not in VALID_COVERAGE_STATUSES:
            errors.append(
                f"provider_coverage.status must be one of {VALID_COVERAGE_STATUSES}, "
                f"got '{self.provider_coverage.status}'"
            )

        metrics_dict = asdict(self.metrics)

        # Invariant 1: metric in missing_metrics → value must be null
        for m in self.provider_coverage.missing_metrics:
            if m in metrics_dict and metrics_dict[m] is not None:
                errors.append(
                    f"'{m}' is in missing_metrics but has non-null value {metrics_dict[m]}"
                )

        # Invariant 2: metric in collectable_metrics → value must not be null
        for m in self.provider_coverage.collectable_metrics:
            if m in metrics_dict and metrics_dict[m] is None:
                errors.append(f"'{m}' is in collectable_metrics but has null value")

        # Invariant 3: status = "partial" → missing_metrics non-empty
        if (
            self.provider_coverage.status == "partial"
            and not self.provider_coverage.missing_metrics
        ):
            errors.append(
                "provider_coverage.status is 'partial' but missing_metrics is empty"
            )

        # Invariant 5: non-null metric must be in collectable_metrics
        for m, v in metrics_dict.items():
            if v is not None and m not in self.provider_coverage.collectable_metrics:
                errors.append(
                    f"'{m}' has non-null value {v} but is not in collectable_metrics"
                )

        # Invariant 4: not_proven_runtime_adapter → collectable_metrics = [], all metrics null
        if self.provider_coverage.status == "not_proven_runtime_adapter":
            if self.provider_coverage.collectable_metrics:
                errors.append(
                    "status is 'not_proven_runtime_adapter' but collectable_metrics is not empty"
                )
            for m, v in metrics_dict.items():
                if v is not None:
                    errors.append(
                        f"status is 'not_proven_runtime_adapter' but metrics.{m} = {v} (must be null)"
                    )

        if errors:
            raise ValueError(
                "MarketMetricsV1 validation failed:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

        return True

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)
