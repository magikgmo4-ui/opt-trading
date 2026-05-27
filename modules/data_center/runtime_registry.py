from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Runtime registry — distinct from static modules/data_center/registry/*.json
# Stores live producer state: last_write, last_output_path, status, evidence
_RUNTIME_REGISTRY_PATH = Path("data/data_center/_registry/producers.json")


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp"
    ) as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)


def _load_or_init(root: Path) -> dict:
    path = root / _RUNTIME_REGISTRY_PATH
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"runtime_registry_version": "v1", "updated_at": None, "producers": {}}


def update_producer_last_write(
    producer_id: str,
    contract_class: str,
    output_path: Union[str, Path],
    root: Optional[Path] = None,
    status: str = "ok",
    evidence: Optional[dict] = None,
) -> dict:
    """Record a successful producer write in the runtime registry.

    Writes/updates data/data_center/_registry/producers.json.
    Thread-safe via atomic rename. Idempotent for same producer_id.

    Returns the producer entry as stored.
    """
    root = Path(root) if root is not None else _PROJECT_ROOT
    now = datetime.now(timezone.utc).isoformat()
    data = _load_or_init(root)
    entry = {
        "producer_id": producer_id,
        "contract_class": contract_class,
        "last_write": now,
        "last_output_path": str(output_path),
        "status": status,
        "evidence": evidence if evidence is not None else {},
        "updated_at": now,
    }
    data["producers"][producer_id] = entry
    data["updated_at"] = now
    _atomic_write_json(root / _RUNTIME_REGISTRY_PATH, data)
    return entry


def load_runtime_registry(root: Optional[Path] = None) -> dict:
    """Load runtime registry from data/data_center/_registry/producers.json.

    Returns an empty registry dict if the file does not exist yet.
    Safe to call before any producer has written.
    """
    root = Path(root) if root is not None else _PROJECT_ROOT
    return _load_or_init(root)
