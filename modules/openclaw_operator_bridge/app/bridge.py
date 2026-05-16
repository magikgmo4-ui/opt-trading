from __future__ import annotations
import uuid
import logging
from .schema import BridgeRequest, BridgeResponse, ActionNotAllowed, BridgeError, BridgeTimeout
from .client import call_builder

log = logging.getLogger("openclaw_operator_bridge")


class OperatorBridge:
    """Single entry point for opt-trading → OpenClaw communication."""

    def send(self, request: BridgeRequest) -> BridgeResponse:
        if not request.request_id:
            request.request_id = str(uuid.uuid4())

        try:
            request.validate()
        except ActionNotAllowed as exc:
            log.warning("blocked action: %s", exc)
            return BridgeResponse(
                request_id=request.request_id,
                status="error",
                content="",
                error=str(exc),
            )

        log.info("bridge.send action=%s request_id=%s", request.action, request.request_id)

        try:
            response = call_builder(
                action=request.action,
                instruction=request.instruction,
                context=request.context,
                request_id=request.request_id,
                timeout_s=request.timeout_s,
            )
        except BridgeTimeout as exc:
            log.error("bridge timeout: %s", exc)
            return BridgeResponse(
                request_id=request.request_id,
                status="timeout",
                content="",
                error=str(exc),
            )
        except BridgeError as exc:
            log.error("bridge error: %s", exc)
            return BridgeResponse(
                request_id=request.request_id,
                status="error",
                content="",
                error=str(exc),
            )

        log.info(
            "bridge.response status=%s duration_ms=%d",
            response.status,
            response.duration_ms,
        )
        return response
