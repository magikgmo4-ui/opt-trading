"""Writes structured proof artefacts (JSON + Markdown summary)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ARTIFACTS_DIR = Path("artifacts/automation_ops/semiauto_pilot")


def write(contract: dict[str, Any], base_dir: Path | None = None) -> tuple[Path, Path]:
    """Write proof JSON and Markdown summary. Returns (json_path, md_path)."""
    out_dir = (base_dir or ARTIFACTS_DIR) / contract["run_id"]
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / "proof.json"
    json_path.write_text(json.dumps(contract, indent=2))

    md_path = out_dir / "proof_summary.md"
    md_path.write_text(_render_md(contract))

    return json_path, md_path


def _render_md(c: dict[str, Any]) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    planned = c.get("actions_planned", [])
    executed = c.get("actions_executed", [])
    stops = c.get("stop_conditions", [])

    lines = [
        f"# Proof — {c['run_id']}",
        "",
        f"| Field | Value |",
        f"|---|---|",
        f"| GO | `{c['go_id']}` |",
        f"| Parent GO | `{c['parent_go_id']}` |",
        f"| Mode | `{c['mode']}` |",
        f"| Human gate | `{c['human_gate_required']}` |",
        f"| Verdict | **{c['verdict']}** |",
        f"| Next GO | `{c.get('next_go') or '—'}` |",
        f"| Generated | {ts} |",
        "",
    ]

    if planned:
        lines += ["## Actions planned", ""]
        lines += [f"- {a}" for a in planned]
        lines += [""]

    if executed:
        lines += ["## Actions executed", ""]
        lines += [f"- {a}" for a in executed]
        lines += [""]

    if stops:
        lines += ["## Stop conditions", ""]
        lines += [f"- {s}" for s in stops]
        lines += [""]

    return "\n".join(lines)
