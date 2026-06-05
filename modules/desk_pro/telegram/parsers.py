from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

# Whitelist of known crypto + macro assets
_KNOWN_ASSETS = {
    "BTC", "ETH", "SOL", "XRP", "DOGE", "LTC", "ADA", "DOT", "AVAX",
    "MATIC", "LINK", "UNI", "ATOM", "APE", "SUI", "APT", "ARB", "OP",
    "PEPE", "SHIB", "WIF", "BONK", "FLOKI", "INJ", "HYPE", "RUNE",
    "XAUUSD", "GOLD", "XAU", "DXY", "SPX", "SPY", "VIX", "US10Y",
    "EURUSD", "GBPUSD", "USDJPY", "WTI", "BRENT", "NATGAS",
    "BNB", "TRX", "XLM", "HBAR", "TON", "NEAR", "INJ", "WLD", "POL",
    "OM", "ENA", "JUP", "RNDR", "WIF", "BOME", "NOT", "STRK",
}

# Pattern 1: Free text format: "BTC LONG Entry: 50000"
_ASSET_PATTERN = re.compile(
    r'(?:[#$]?(?P<asset>' + '|'.join(sorted(_KNOWN_ASSETS, key=len, reverse=True)) + r'))'
    r'(?:/USDT)?\s+'
    r'(?P<direction>LONG|SHORT|BUY|SELL)\b',
    re.IGNORECASE,
)

# Pattern 2: Structured "COIN: **$INJ**/USDT Direction: LONG"
_STRUCTURED_COIN_RE = re.compile(
    r'(?:COIN|SYMBOL|PAIR)\s*:\s*\*+\$?(?P<asset>[A-Z]{2,10})\*+\s*(?:/USDT)?.*?(?P<direction>LONG|SHORT)',
    re.IGNORECASE | re.DOTALL,
)

# Pattern 3: Chinese "做多**BTC**" / "做空**ETH**"
_CHINESE_LONG_RE = re.compile(
    r'做多\**(?P<asset>[A-Z]{2,10})\**',
    re.IGNORECASE,
)
_CHINESE_SHORT_RE = re.compile(
    r'做空\**(?P<asset>[A-Z]{2,10})\**',
    re.IGNORECASE,
)

# Price value: 1-8 digit number with optional decimals (used by all price regexes)
_PRICE_STR = r'\d{1,8}(?:\.\d+)?'

# Pattern 4: Hashtag coin format: "#ACEUSDT", "#BTCUSDT" with Direction: Long
_HASHTAG_COIN_RE = re.compile(
    r'#(?P<asset>[A-Z]{2,10})USDT.*?(?P<direction>Long|Short|LONG|SHORT)',
    re.IGNORECASE | re.DOTALL,
)

# Pattern 5: GOLD/XAU trade: "BUY GOLD NOW Entry: 4496 SL: 4485 TP1: 4503"
_GOLD_TRADE_RE = re.compile(
    r'(?:BUY|SELL)\s+(?:GOLD|XAU).*?'
    r'(?:Entry|Price)[:\s]+(?P<entry>' + _PRICE_STR + ')',
    re.IGNORECASE | re.DOTALL,
)

# Pattern 6: XAUHQ signal: "XAUHQ | HIT TARGET ENTRY: 4468.5"
_XAUHQ_RE = re.compile(
    r'XAUHQ.*?(?:ENTRY|Entry)\s*(?:Point)?\s*[:\s]+(?P<entry>' + _PRICE_STR + ')',
    re.IGNORECASE | re.DOTALL,
)

# Pattern 7: Whale transfer: "1,026 $BTC (65,704,264 USD)", "3,399 $BTC ($215M)"
_WHALE_BTC_RE = re.compile(
    r'(?P<amount>[\d,]+)\s*\$(?P<asset>BTC|ETH)\s*\(\s*\$?(?P<value>[\d,]+)',
    re.IGNORECASE,
)

# Pattern 8: GOLD entry: "BUY GOLD NOW ... Entry Point: 4496.0"
_GOLD_TRADE_RE = re.compile(
    r'(?:BUY|SELL)\s+(?:GOLD|XAU).*?'
    r'Entry\s*(?:Point)?\s*[:\s]+\s*(?P<entry>' + _PRICE_STR + ')',
    re.IGNORECASE | re.DOTALL,
)

# Pattern 8: Signal #ID format "SIGNAL ID: #2138 COIN: **$INJ**/USDT"
_SIGNAL_ID_COIN_RE = re.compile(
    r'SIGNAL\s*(?:ID)?\s*[:\#]\s*\d+.*?COIN.*?\$?(?P<asset>[A-Z]{2,10})',
    re.IGNORECASE | re.DOTALL,
)

# Price regexes used by _extract_prices_from_text
_ENTRY_RE = re.compile(
    r'(?:Entry|Price|@|开仓价格)\s*(?:Point|Price)?\s*[:\s\$]+(?P<entry>' + _PRICE_STR + ')',
    re.IGNORECASE,
)

_SL_RE = re.compile(
    r'(?:Stop[-\s]?Loss|SL|Stop)[:\s]+(?P<sl>' + _PRICE_STR + ')',
    re.IGNORECASE,
)

_TP_RE = re.compile(
    r'(?:Take[-\s]?Profit|TP|Target)\d*[:\s]+(?P<tp>' + _PRICE_STR + ')',
    re.IGNORECASE,
)

_TP_MULTI_RE = re.compile(
    r'(?:TP|Target)\s*\d*\s*[:\s]+\s*(?P<tp>' + _PRICE_STR + ')',
    re.IGNORECASE,
)

_LEVERAGE_RE = re.compile(
    r'(?:leverage|levier|x)\s*(?P<leverage>\d+)\s*x?',
    re.IGNORECASE,
)


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


def _parse_float(raw: Optional[str]) -> Optional[float]:
    if raw is None:
        return None
    try:
        return float(raw.replace(",", "").replace(" ", ""))
    except (ValueError, AttributeError):
        return None


def _extract_prices_from_text(text: str) -> tuple[Optional[float], Optional[float], list[float], Optional[int]]:
    entry = _parse_float(_ENTRY_RE.search(text).group("entry") if _ENTRY_RE.search(text) else None)
    sl = _parse_float(_SL_RE.search(text).group("sl") if _SL_RE.search(text) else None)
    tps = [t for t in [_parse_float(m.group("tp")) for m in _TP_MULTI_RE.finditer(text)] if t is not None]
    if not tps:
        tp = _parse_float(_TP_RE.search(text).group("tp") if _TP_RE.search(text) else None)
        if tp is not None:
            tps = [tp]
    lev = _parse_float(_LEVERAGE_RE.search(text).group("leverage") if _LEVERAGE_RE.search(text) else None)
    leverage = int(lev) if lev is not None else None
    return entry, sl, tps, leverage


def parse_telegram_message(raw_dict: dict) -> ParsedTelegramMessage:
    raw_text = raw_dict.get("raw_text", "")
    channel_alias = raw_dict.get("channel_alias", raw_dict.get("channel", ""))

    if not raw_text or not isinstance(raw_text, str):
        return ParsedTelegramMessage(message_type="UNKNOWN_RAW", raw_text=str(raw_text), channel_alias=channel_alias)

    asset = None
    direction = None

    # Try free-text pattern first
    m = _ASSET_PATTERN.search(raw_text)
    if m:
        asset = m.group("asset").upper()
        direction_raw = m.group("direction").upper()
        direction = "LONG" if direction_raw in ("LONG", "BUY") else "SHORT"

    # Try structured COIN format (trusted signal channel, skip whitelist)
    if asset is None:
        m = _STRUCTURED_COIN_RE.search(raw_text)
        if m:
            asset = m.group("asset").upper()
            direction_raw = m.group("direction").upper()
            direction = "LONG" if direction_raw == "LONG" else "SHORT"

    # Try Chinese long format
    if asset is None:
        m = _CHINESE_LONG_RE.search(raw_text)
        if m:
            asset = m.group("asset").upper()
            direction = "LONG"

    # Try Chinese short format
    if asset is None:
        m = _CHINESE_SHORT_RE.search(raw_text)
        if m:
            asset = m.group("asset").upper()
            direction = "SHORT"

    # Try hashtag coin format: "#ACEUSDT ... Direction: Long"
    if asset is None:
        m = _HASHTAG_COIN_RE.search(raw_text)
        if m:
            asset = m.group("asset").upper()
            direction_raw = m.group("direction").upper()
            direction = "LONG" if direction_raw in ("LONG", "BUY") else "SHORT"

    # Try Signal ID + COIN format: "SIGNAL ID: #2138 COIN: **$INJ**/USDT"
    if asset is None:
        m = _SIGNAL_ID_COIN_RE.search(raw_text)
        if m:
            asset = m.group("asset").upper()
            # Look for direction nearby
            dir_match = re.search(r'(?:Direction)[:\s]+(?P<dir>LONG|SHORT)', raw_text, re.IGNORECASE)
            if dir_match:
                direction = dir_match.group("dir").upper()

    # Try GOLD trade format: "BUY GOLD NOW Entry: 4496"
    if asset is None:
        m = _GOLD_TRADE_RE.search(raw_text)
        if m:
            asset = "XAUUSD"
            direction = "LONG" if "BUY" in raw_text.upper() else "SHORT"

    # Try XAUHQ format: "XAUHQ | ENTRY: 4468.5"
    if asset is None:
        m = _XAUHQ_RE.search(raw_text)
        if m:
            asset = "XAUUSD"
            direction = None  # Direction not explicit, derive from context later

    # Try whale alert: "1,026 BTC ($65M) transferred from X to Y"
    if asset is None:
        m = _WHALE_BTC_RE.search(raw_text)
        if m:
            asset = m.group("asset").upper()
            claim = {
                "claim_type": "CRYPTO_FLOW",
                "asset": asset,
                "amount": m.group("amount").replace(",", ""),
                "value_usd": m.group("value").replace(",", ""),
                "source_channel": channel_alias,
                "message_id": raw_dict.get("message_id", ""),
            }
            return ParsedTelegramMessage(
                message_type="CRYPTO_FLOW",
                raw_text=raw_text,
                channel_alias=channel_alias,
                claim=claim,
            )

    if asset is None:
        return ParsedTelegramMessage(message_type="UNKNOWN_RAW", raw_text=raw_text, channel_alias=channel_alias)

    # Validate: structured coin matches skip whitelist (trusted signal format)
    from_structured = _STRUCTURED_COIN_RE.search(raw_text) is not None
    if not from_structured and asset not in _KNOWN_ASSETS:
        return ParsedTelegramMessage(message_type="UNKNOWN_RAW", raw_text=raw_text, channel_alias=channel_alias)

    entry, sl, tps, leverage = _extract_prices_from_text(raw_text)

    claim = {"claim_type": "TRADE_SETUP", "asset": asset, "direction": direction}
    if entry is not None: claim["entry"] = entry
    if sl is not None: claim["sl"] = sl
    if tps: claim["tp"] = tps[0]
    if len(tps) > 1: claim["tps"] = tps
    if leverage is not None: claim["leverage"] = leverage
    claim["source_channel"] = channel_alias
    claim["message_id"] = raw_dict.get("message_id", "")

    return ParsedTelegramMessage(message_type="TRADE_SETUP", raw_text=raw_text, channel_alias=channel_alias, claim=claim)
