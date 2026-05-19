from __future__ import annotations

import json
import os
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .storage import now_z, write_json


@dataclass(frozen=True)
class MemorySyncResult:
    promoted_memory_brick_id: str | None
    memory_sync_status: str
    memory_sync_at: str | None
    memory_sync_error: str | None


def sync_to_memory_bricks(
    *,
    workspace_root: Path,
    campaign_id: str,
    capitalization_id: str,
    brick_payload: dict[str, Any],
    links: list[str],
    env: dict[str, str] | None = None,
) -> MemorySyncResult:
    cli_command = (env or os.environ).get("KIL_V1_MEMORY_BRICKS_CMD", "").strip()
    if not cli_command:
        return MemorySyncResult(
            promoted_memory_brick_id=None,
            memory_sync_status="SYNC_FAILED",
            memory_sync_at=now_z(),
            memory_sync_error="KIL_V1_MEMORY_BRICKS_CMD is not configured",
        )

    sync_dir = workspace_root / "exports" / campaign_id / "memory_bricks_sync"
    request_path = sync_dir / f"promotion_request_{capitalization_id}.json"
    write_json(
        request_path,
        {
            "campaign_id": campaign_id,
            "capitalization_id": capitalization_id,
            "brick": brick_payload,
            "links": links,
        },
    )

    command_prefix = shlex.split(cli_command)
    try:
        created = _run_json_command(command_prefix + ["new", "--payload-file", str(request_path)], env)
        brick_id = _extract_brick_id(created)
        if not brick_id:
            raise RuntimeError("Memory Bricks CLI did not return a brick id")

        for link in links:
            _run_json_command(command_prefix + ["link", "--id", brick_id, "--target", link], env)

        _run_json_command(command_prefix + ["index", "rebuild"], env)
        return MemorySyncResult(
            promoted_memory_brick_id=brick_id,
            memory_sync_status="SYNCED",
            memory_sync_at=now_z(),
            memory_sync_error=None,
        )
    except Exception as exc:
        return MemorySyncResult(
            promoted_memory_brick_id=None,
            memory_sync_status="SYNC_FAILED",
            memory_sync_at=now_z(),
            memory_sync_error=str(exc),
        )


def _run_json_command(command: list[str], env: dict[str, str] | None) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    stdout = completed.stdout.strip()
    if not stdout:
        return {}
    payload = json.loads(stdout)
    if not isinstance(payload, dict):
        raise RuntimeError("Memory Bricks CLI returned non-object JSON")
    return payload


def _extract_brick_id(payload: dict[str, Any]) -> str | None:
    for key in ("id", "brick_id", "promoted_memory_brick_id"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None
