from typing import List

from .schema import (
    VALID_FRESHNESS_STATES,
    VALID_BIAS,
    VALID_REGIME,
    VALID_SQUEEZE,
    VALID_CONFIDENCE,
)

_REQUIRED_TOP = {"contract", "bundle_id", "produced_at", "freshness_state", "assets", "inputs", "analysis", "missing_inputs", "source_refs"}


def validate_bundle(data: dict) -> List[str]:
    errors: List[str] = []

    if not isinstance(data, dict):
        return ["bundle must be a dict"]

    # required top-level keys
    missing_top = _REQUIRED_TOP - set(data.keys())
    if missing_top:
        for k in sorted(missing_top):
            errors.append(f"missing required key: {k}")

    if errors:
        return errors

    # contract
    if not isinstance(data["contract"], str) or not data["contract"].startswith("bundle."):
        errors.append(f"contract must start with 'bundle.', got {data['contract']!r}")

    # bundle_id
    if not isinstance(data["bundle_id"], str):
        errors.append(f"bundle_id must be a string, got {type(data['bundle_id']).__name__}")

    # produced_at
    if not isinstance(data["produced_at"], str):
        errors.append(f"produced_at must be a string, got {type(data['produced_at']).__name__}")

    # freshness_state
    if data["freshness_state"] not in VALID_FRESHNESS_STATES:
        errors.append(f"freshness_state must be one of {VALID_FRESHNESS_STATES}, got {data['freshness_state']!r}")

    # assets
    if not isinstance(data["assets"], list) or not all(isinstance(a, str) for a in data["assets"]):
        errors.append("assets must be a list of strings")

    # inputs
    if not isinstance(data["inputs"], dict):
        errors.append("inputs must be a dict")
    else:
        for name, inp in data["inputs"].items():
            if not isinstance(inp, dict):
                errors.append(f"inputs.{name} must be a dict")
                continue
            if "source" not in inp:
                errors.append(f"inputs.{name}: missing 'source'")
            if "freshness" not in inp:
                errors.append(f"inputs.{name}: missing 'freshness'")

    # analysis
    if not isinstance(data["analysis"], dict):
        errors.append("analysis must be a dict")
    else:
        analysis = data["analysis"]
        if analysis.get("timeframe") is not None and not isinstance(analysis["timeframe"], str):
            errors.append("analysis.timeframe must be a string")
        if "bias_short_term" in analysis and analysis["bias_short_term"] not in VALID_BIAS:
            errors.append(f"analysis.bias_short_term must be one of {VALID_BIAS}")
        if "bias_intraday" in analysis and analysis["bias_intraday"] not in VALID_BIAS:
            errors.append(f"analysis.bias_intraday must be one of {VALID_BIAS}")
        if "regime" in analysis and analysis["regime"] not in VALID_REGIME:
            errors.append(f"analysis.regime must be one of {VALID_REGIME}")
        if "squeeze_or_stress_level" in analysis and analysis["squeeze_or_stress_level"] not in VALID_SQUEEZE:
            errors.append(f"analysis.squeeze_or_stress_level must be one of {VALID_SQUEEZE}")
        if "confidence" in analysis and analysis["confidence"] not in VALID_CONFIDENCE:
            errors.append(f"analysis.confidence must be one of {VALID_CONFIDENCE}")

    # missing_inputs
    if not isinstance(data["missing_inputs"], list):
        errors.append("missing_inputs must be a list")
    if data["freshness_state"] == "STALE" and len(data.get("missing_inputs", [])) == 0:
        errors.append("missing_inputs must not be empty when freshness_state is STALE")

    # source_refs
    if not isinstance(data["source_refs"], list):
        errors.append("source_refs must be a list")

    return errors
