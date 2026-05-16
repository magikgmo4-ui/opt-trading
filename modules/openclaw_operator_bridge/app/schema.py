from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


ALLOWED_ACTIONS = {"ask", "build", "evaluate", "review"}


@dataclass
class BridgeRequest:
    action: str
    instruction: str
    context: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    request_id: str = ""
    timeout_s: int = 60

    def validate(self) -> None:
        if self.action not in ALLOWED_ACTIONS:
            raise ActionNotAllowed(
                f"action '{self.action}' not in whitelist {sorted(ALLOWED_ACTIONS)}"
            )
        if not self.instruction.strip():
            raise ValueError("instruction must not be empty")


@dataclass
class BridgeResponse:
    request_id: str
    status: str          # ok | error | timeout
    content: str
    structured: dict[str, Any] = field(default_factory=dict)
    duration_ms: int = 0
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "status": self.status,
            "result": {
                "content": self.content,
                "structured": self.structured,
            },
            "duration_ms": self.duration_ms,
            "error": self.error,
        }


class BridgeError(Exception):
    pass


class ActionNotAllowed(BridgeError):
    pass


class GatewayUnreachable(BridgeError):
    pass


class BridgeTimeout(BridgeError):
    pass
