from __future__ import annotations
import os
from pathlib import Path
from typing import Any, Optional, Dict, Tuple


CREDENTIAL_NAMES = ("api_key", "secret_key", "passphrase")
DEFAULT_PROFILE = "readonly_main"
SECRETS_FILE = Path("/opt/trading/.secrets/bitget.env")


def _load_secrets_file(path: Path = SECRETS_FILE) -> bool:
    """
    Load KEY=VALUE pairs from a local secrets file into os.environ.
    Only sets vars that are not already present in the environment.
    Returns True if file was loaded, False if not found.
    """
    if not path.exists():
        return False
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val
        return True
    except Exception:
        return False


def _env_name(profile: str, field: str) -> str:
    return f"BITGET_{profile.upper()}_{field.upper()}"


def load_credentials(profile: str = DEFAULT_PROFILE) -> Tuple[str, Optional[Dict[str, str]]]:
    """
    Load Bitget credentials from local file then env vars by profile.

    Returns:
        (status, creds)
        status: "ok" | "missing" | "incomplete"
        creds: dict with api_key, secret_key, passphrase (only if status == "ok")
    """
    _load_secrets_file()

    result = {}
    missing = []

    for field in CREDENTIAL_NAMES:
        env_name = _env_name(profile, field)
        val = os.environ.get(env_name, "").strip()
        if val:
            result[field] = val
        else:
            missing.append(env_name)

    if not missing:
        return "ok", result
    if len(missing) == len(CREDENTIAL_NAMES):
        return "missing", None
    return "incomplete", None


def secrets_file_status() -> Dict[str, Any]:
    """Check if the local secrets file exists and is readable."""
    path = SECRETS_FILE
    if not path.exists():
        return {"exists": False, "path": str(path)}
    try:
        content = path.read_text(encoding="utf-8")
        lines = [l.strip() for l in content.splitlines() if l.strip() and not l.strip().startswith("#")]
        return {"exists": True, "path": str(path), "vars_count": len(lines)}
    except Exception as e:
        return {"exists": True, "path": str(path), "error": str(e)}


def list_profiles_status() -> Dict[str, str]:
    """Check all profiles found in env vars and local file."""
    _load_secrets_file()

    profiles = set()
    for key in os.environ:
        if key.startswith("BITGET_") and key.count("_") >= 2:
            parts = key.split("_")
            if len(parts) >= 3:
                profile = "_".join(parts[1:-1]).lower()
                profiles.add(profile)

    result = {}
    for p in sorted(profiles):
        status, _ = load_credentials(p)
        result[p] = status
    return result
