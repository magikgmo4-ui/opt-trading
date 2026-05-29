from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class RawMessage:
    message_id: str
    channel: str
    raw_text: str
    sender: str | None = None
    timestamp: str | None = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc).isoformat()


@dataclass
class InboundMessage:
    message_id: str
    channel: str
    sender: str | None
    timestamp: str
    raw_text: str
    normalized_type: str = "text"

    @classmethod
    def from_raw(cls, raw: RawMessage, normalized_type: str = "text") -> "InboundMessage":
        return cls(
            message_id=raw.message_id,
            channel=raw.channel,
            sender=raw.sender,
            timestamp=raw.timestamp or datetime.now(timezone.utc).isoformat(),
            raw_text=raw.raw_text,
            normalized_type=normalized_type,
        )
