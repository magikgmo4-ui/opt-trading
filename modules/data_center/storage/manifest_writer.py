from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp"
    ) as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)


def write_manifest(
    producer_dir: Path,
    producer_id: str,
    schema_name: str,
    status: str = "ok",
    extra: Optional[dict] = None,
    root: Optional[Path] = None,
) -> Path:
    producer_path = Path(producer_dir)
    if root is not None:
        producer_path = Path(root) / producer_dir

    manifest = {
        "producer_id": producer_id,
        "schema": schema_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
    }
    if extra:
        manifest["extra"] = extra

    manifest_path = producer_path / "manifest.json"
    _atomic_write_json(manifest_path, manifest)
    return manifest_path
