from __future__ import annotations
import hmac
from typing import Optional, Mapping, Any

from modules.auth.secrets import get_secret, require_secret

ENV_KEY_NAME = "TV_WEBHOOK_KEY"

def expected_webhook_key() -> str:
    return require_secret(ENV_KEY_NAME)

def extract_provided_key(payload: Mapping[str, Any]) -> Optional[str]:
    """
    TradingView payload convention: {"key": "..."}.
    """
    v = payload.get("key")
    if v is None:
        return None
    if not isinstance(v, str):
        return None
    v = v.strip()
    return v if v else None

def validate_webhook_key(provided: str, expected: str) -> bool:
    """
    Constant-time comparison.
    """
    if not isinstance(provided, str) or not isinstance(expected, str):
        return False
    return hmac.compare_digest(provided, expected)

def payload_key_is_valid(payload: Mapping[str, Any]) -> bool:
    expected = get_secret(ENV_KEY_NAME, "") or ""
    expected = expected.strip()
    if not expected:
        return False
    provided = extract_provided_key(payload)
    if not provided:
        return False
    return validate_webhook_key(provided, expected)
