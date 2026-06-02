from __future__ import annotations
import json
import subprocess
import shutil
import sys
from pathlib import Path
from typing import Any
from .schema import BridgeResponse, GatewayUnreachable, BridgeTimeout, BridgeError


OPENCLAW_BIN = "openclaw"
BUILDER_AGENT = "builder"
DISPATCHER_SCRIPT = Path(__file__).resolve().parents[3] / "scripts/ai/workers/openclaw_strict_worker_dispatcher.py"


def _build_message(action: str, instruction: str, context: str) -> str:
    parts = [f"[{action.upper()}]"]
    if context:
        parts.append(f"Context: {context}")
    parts.append(instruction)
    return "\n".join(parts)


def call_builder(
    action: str,
    instruction: str,
    context: str,
    request_id: str,
    timeout_s: int,
) -> BridgeResponse:
    if not shutil.which(OPENCLAW_BIN):
        raise GatewayUnreachable(f"'{OPENCLAW_BIN}' not found in PATH")

    message = _build_message(action, instruction, context)

    cmd = [
        OPENCLAW_BIN, "agent",
        "--agent", BUILDER_AGENT,
        "--json",
        "--message", message,
        "--timeout", str(timeout_s),
    ]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_s + 10,
        )
    except subprocess.TimeoutExpired:
        raise BridgeTimeout(f"builder did not respond within {timeout_s}s")

    raw = proc.stdout.strip()
    if not raw:
        stderr = proc.stderr.strip()
        raise BridgeError(f"empty response from builder (stderr: {stderr})")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BridgeError(f"non-JSON response from builder: {raw[:200]}") from exc

    status = data.get("status", "error")
    if status != "ok":
        return BridgeResponse(
            request_id=request_id,
            status="error",
            content="",
            duration_ms=data.get("result", {}).get("meta", {}).get("durationMs", 0),
            error=f"builder status={status}: {raw[:300]}",
        )

    result = data.get("result", {})
    payloads = result.get("payloads", [])
    content = payloads[0].get("text", "") if payloads else ""
    duration_ms = result.get("meta", {}).get("durationMs", 0)

    return BridgeResponse(
        request_id=request_id,
        status="ok",
        content=content,
        structured=result.get("meta", {}),
        duration_ms=duration_ms,
    )


def call_dispatcher(
    parameters: dict[str, Any],
    request_id: str,
    timeout_s: int,
) -> BridgeResponse:
    """Route a dispatch action to openclaw_strict_worker_dispatcher.py.

    parameters keys (mutually exclusive):
      packet_id   — job packet ID resolved from job_packets/
      packet_path — absolute or repo-relative path to a job packet JSON file
      packet_json — inline JSON string of the job packet

    optional:
      dry_run      (bool, default True)
      gate_approved (bool, default False)
    """
    if not DISPATCHER_SCRIPT.exists():
        raise BridgeError(f"dispatcher script not found: {DISPATCHER_SCRIPT}")

    cmd = [sys.executable, str(DISPATCHER_SCRIPT)]

    if "packet_id" in parameters:
        cmd += ["--packet-id", str(parameters["packet_id"])]
    elif "packet_path" in parameters:
        cmd += ["--packet", str(parameters["packet_path"])]
    elif "packet_json" in parameters:
        cmd += ["--packet-json", str(parameters["packet_json"])]
    else:
        raise BridgeError("dispatch action requires one of: packet_id, packet_path, packet_json in parameters")

    dry_run = parameters.get("dry_run", True)
    gate_approved = parameters.get("gate_approved", False)

    if dry_run:
        cmd.append("--dry-run")
    if gate_approved:
        cmd.append("--gate-approved")

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_s + 10,
        )
    except subprocess.TimeoutExpired:
        raise BridgeTimeout(f"dispatcher did not respond within {timeout_s}s")

    raw = proc.stdout.strip()
    if not raw:
        raise BridgeError(f"empty response from dispatcher (stderr: {proc.stderr.strip()[:200]})")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BridgeError(f"non-JSON response from dispatcher: {raw[:200]}") from exc

    dispatch_status = data.get("status", "error")
    ok = dispatch_status in ("PASS", "DRY_RUN_PASS")

    return BridgeResponse(
        request_id=request_id,
        status="ok" if ok else "error",
        content=dispatch_status,
        structured=data,
        duration_ms=0,
        error=None if ok else f"dispatcher status={dispatch_status}",
    )
