from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ParsedTelegramMessage:
    message_type: str
    raw_text: str
    channel_alias: str
    claim: Optional[dict] = None
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = {
            "message_type": self.message_type,
            "raw_text": self.raw_text,
            "channel_alias": self.channel_alias,
            "warnings": list(self.warnings),
        }
        if self.claim is not None:
            d["claim"] = self.claim
        return d


_LOOSE_TRADE_RE = re.compile(
    r"(?P<asset>[A-Z]{2,10})\s+"
    r"(?P<direction>LONG|SHORT)\b",
    re.IGNORECASE,
)

_ENTRY_RE = re.compile(
    r"(?:Entry|Price)[:\s]+(?P<entry>[\d.,]+)",
    re.IGNORECASE,
)

_SL_RE = re.compile(
    r"(?:Stop\s*Loss|SL)[:\s]+(?P<sl>[\d.,]+)",
    re.IGNORECASE,
)

_TP_RE = re.compile(
    r"(?:Target|TP|Take\s*Profit)[:\s]+(?P<tp>[\d.,]+)",
    re.IGNORECASE,
)


def _parse_float(raw: Optional[str]) -> Optional[float]:
    if raw is None:
        return None
    try:
        return float(raw.replace(",", ""))
    except (ValueError, AttributeError):
        return None


def parse_telegram_message(raw_dict: dict) -> ParsedTelegramMessage:
    raw_text = raw_dict.get("raw_text", "")
    channel_alias = raw_dict.get("channel_alias", raw_dict.get("channel", ""))

    if not raw_text or not isinstance(raw_text, str):
        return ParsedTelegramMessage(
            message_type="UNKNOWN_RAW",
            raw_text=str(raw_text),
            channel_alias=channel_alias,
        )

    trade_match = _LOOSE_TRADE_RE.search(raw_text)
    if trade_match is None:
        return ParsedTelegramMessage(
            message_type="UNKNOWN_RAW",
            raw_text=raw_text,
            channel_alias=channel_alias,
        )

    asset = trade_match.group("asset").upper()
    direction = trade_match.group("direction").upper()

    entry = _parse_float(_ENTRY_RE.search(raw_text).group("entry") if _ENTRY_RE.search(raw_text) else None)
    sl = _parse_float(_SL_RE.search(raw_text).group("sl") if _SL_RE.search(raw_text) else None)
    tp = _parse_float(_TP_RE.search(raw_text).group("tp") if _TP_RE.search(raw_text) else None)

    claim = {
        "claim_type": "TRADE_SETUP",
        "asset": asset,
        "direction": direction,
    }
    if entry is not None:
        claim["entry"] = entry
    if sl is not None:
        claim["sl"] = sl
    if tp is not None:
        claim["tp"] = tp

    claim["source_channel"] = channel_alias
    claim["message_id"] = raw_dict.get("message_id", "")

    return ParsedTelegramMessage(
        message_type="TRADE_SETUP",
        raw_text=raw_text,
        channel_alias=channel_alias,
        claim=claim,
    )
