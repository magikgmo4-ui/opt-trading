from __future__ import annotations
import json
import subprocess
import shutil
from .schema import BridgeResponse, GatewayUnreachable, BridgeTimeout, BridgeError


OPENCLAW_BIN = "openclaw"
BUILDER_AGENT = "builder"


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
