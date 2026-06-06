from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

_KNOWN_ASSETS = {
    "BTC", "ETH", "SOL", "XRP", "DOGE", "LTC", "ADA", "DOT", "AVAX",
    "MATIC", "LINK", "UNI", "ATOM", "APE", "SUI", "APT", "ARB", "OP",
    "PEPE", "SHIB", "WIF", "BONK", "FLOKI", "INJ", "HYPE", "RUNE",
    "XAUUSD", "GOLD", "XAU", "DXY", "SPX", "SPY", "VIX", "US10Y",
    "EURUSD", "GBPUSD", "USDJPY", "WTI", "BRENT", "NATGAS",
    "BNB", "TRX", "XLM", "HBAR", "TON", "NEAR", "WLD", "POL",
    "OM", "ENA", "JUP", "RNDR", "WIF", "BOME", "NOT", "STRK",
}

_PRICE_STR = r'\d{1,8}(?:\.\d+)?'

# ── Pattern 1: Free text "BTC LONG Entry: 50000" ─────────────────────
_ASSET_PATTERN = re.compile(
    r'(?:[#$]?(?P<asset>' + '|'.join(sorted(_KNOWN_ASSETS, key=len, reverse=True)) + r'))'
    r'(?:/USDT)?\s+'
    r'(?P<direction>LONG|SHORT|BUY|SELL)\b',
    re.IGNORECASE,
)

# ── Pattern 2: Structured "COIN: **$INJ**/USDT (2-5x) Direction: LONG" ─
_STRUCTURED_COIN_RE = re.compile(
    r'(?:COIN|SYMBOL|PAIR)\s*:\s*\*+\$?(?P<asset>[A-Z]{2,10})\*+\s*/?USDT.?\((?P<leverage>\d+)[-]?\d*x\).*?(?P<direction>LONG|SHORT)',
    re.IGNORECASE | re.DOTALL,
)

# ── Pattern 3: Chinese 做多**BTC** / 做空**ETH** 开仓价格 $62377 ─────────
_CHINESE_LONG_RE = re.compile(
    r'做多\**(?P<asset>[A-Z]{2,10})\**.*?开仓价格\s*\*{0,2}\$?(?P<entry>' + _PRICE_STR + r')',
    re.IGNORECASE | re.DOTALL,
)
_CHINESE_SHORT_RE = re.compile(
    r'做空\**(?P<asset>[A-Z]{2,10})\**.*?开仓价格\s*\*{0,2}\$?(?P<entry>' + _PRICE_STR + r')',
    re.IGNORECASE | re.DOTALL,
)

# ── Pattern 4: Hashtag "#ACEUSDT ... Direction: Long" ────────────────
_HASHTAG_COIN_RE = re.compile(
    r'#(?P<asset>[A-Z]{2,10})USDT.*?(?P<direction>Long|Short|LONG|SHORT)',
    re.IGNORECASE | re.DOTALL,
)

# ── Pattern 5: XAUUSD BUY/SELL GOLD with Entry+SL+TPs ─────────────────
# "BUY GOLD NOW\nEntry Point: 4496.0\nStop Loss: 4485.0\nTP1: 4503.0"
# "XAUUSD BUY NOW 2354\nSL 2343\nTP 2358\nTP 2362"
# "#Gold buy @ 2370\nSl: @ 2360\nTP: @ 2380"
_GOLD_SIGNAL_RE = re.compile(
    r'(?P<direction>BUY|SELL)\s+GOLD\b',
    re.IGNORECASE,
)

# Standalone direction without GOLD keyword: "SELL : 4455.5", "BUY 4500"
_GOLD_STANDALONE_RE = re.compile(
    r'(?P<direction>BUY|SELL)\b\s*[:\s@]+\s*\d',
    re.IGNORECASE,
)

_GOLD_XAUUSD_RE = re.compile(
    r'(?:XAUUSD|GOLD|#BTCUSD|#ETHUSDT|BTCUSDT|ETHUSDT)\s*[*_]*\s+(?P<direction>BUY|SELL)(?=[_*\s]|$)',
    re.IGNORECASE,
)

# Crypto futures format: "Buy/Long #BTCUSDT Entry: 63522 Stop: 62852 Targets: 64367 Leverage: 20X"
_CRYPTO_FUTURES_RE = re.compile(
    r'(?P<direction>Buy|Sell|Long|Short)[/\s]*(?:signal)?\s*#?(?P<asset>[A-Z]{3,10})(?:USDT)?\s*[\n\r]'
    r'.*?Entry\s*(?:range)?\s*[:\s]+(?P<entry>' + _PRICE_STR + r')'
    r'.*?Stop\s*[:\s]+(?P<sl>' + _PRICE_STR + r')',
    re.IGNORECASE | re.DOTALL,
)

# Extract all targets from crypto futures "Targets: X Y Z" or "Targets: X_Y_Z"
_CRYPTO_TARGETS_RE = re.compile(
    r'Targets?\s*[:\s]+(.+)',
    re.IGNORECASE,
)

# Forex pair format: "SELL AUDJPY @ 113.822", "BUY GBPUSD 1.3534"
# Valid forex pairs (prevent false positives like "SIGNAL", "TARGET")
_VALID_FOREX_PAIRS = {
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD", "USDCAD", "USDCHF",
    "EURJPY", "GBPJPY", "AUDJPY", "NZDJPY", "CADJPY", "CHFJPY",
    "EURGBP", "EURAUD", "EURNZD", "EURCAD", "EURCHF",
    "GBPAUD", "GBPNZD", "GBPCAD", "GBPCHF",
    "AUDNZD", "AUDCAD", "AUDCHF",
    "NZDCAD", "NZDCHF", "CADCHF",
}

_FOREX_PAIR_RE = re.compile(
    r'(?P<direction>BUY|SELL)\s+(?P<asset>[A-Z]{6})\s*[@\s]',
    re.IGNORECASE,
)

_GOLD_HASH_RE = re.compile(
    r'#\s*Gold\s+(?P<direction>buy|sell)\b',
    re.IGNORECASE,
)

_GOLD_ENTRY_SL_RE = re.compile(
    r'Entry\s*(?:Point)?\s*[:\s]+\s*(?P<entry>' + _PRICE_STR + r')\s*/\s*(?P<entry2>' + _PRICE_STR + r')?'
    r'.*?Stop\s*(?:Loss|Loss)?\s*[:\s]+\s*(?P<sl>' + _PRICE_STR + r')',
    re.IGNORECASE | re.DOTALL,
)

_GOLD_INLINE_SL_RE = re.compile(
    r'(?:SL|Sl)\s*[:\s@.]*\s*(?P<sl>' + _PRICE_STR + r')',
    re.IGNORECASE,
)

# Inline SL without any separator: "SL2669", "SL.2610.50", "SL4515"
_GOLD_NO_SPACE_SL_RE = re.compile(
    r'(?:SL|Sl)[.\s]*?(?P<sl>' + _PRICE_STR + r')',
    re.IGNORECASE,
)

_GOLD_INLINE_PRICE_RE = re.compile(
    r'(?:^|\s)(?P<price>' + _PRICE_STR + r')(?:\s|$)',
    re.IGNORECASE | re.MULTILINE,
)

_GOLD_TPS_RE = re.compile(
    r'TP\s*(?P<tp_num>\d+)?\s*[:\s@]+\s*(?P<tp>' + _PRICE_STR + r')',
    re.IGNORECASE,
)

_GOLD_SL_TP_RE = re.compile(
    r'[:\s@]+\s*(?P<price>' + _PRICE_STR + r')\s*',
    re.IGNORECASE,
)

_GOLD_ENTRY_SL_RE = re.compile(
    r'Entry\s*(?:Point)?\s*[:\s]+\s*(?P<entry>' + _PRICE_STR + r')\s*/\s*(?P<entry2>' + _PRICE_STR + r')?'
    r'.*?Stop\s*(?:Loss|Loss)?\s*[:\s]+\s*(?P<sl>' + _PRICE_STR + r')',
    re.IGNORECASE | re.DOTALL,
)

_GOLD_TPS_RE = re.compile(
    r'TP\s*(?P<tp_num>\d+)\s*[:\s]+\s*(?P<tp>' + _PRICE_STR + r')',
    re.IGNORECASE,
)

# ── Pattern 6: XAUHQ "XAUHQ | ENTRY: 4468.5" ─────────────────────────
_XAUHQ_RE = re.compile(
    r'XAUHQ.*?ENTRY\s*[:\s]+\s*(?P<entry>' + _PRICE_STR + r')',
    re.IGNORECASE | re.DOTALL,
)

# ── Pattern 7: Whale transfer "1,026 $BTC (65,704,264 USD)" ────────
_WHALE_BTC_RE = re.compile(
    r'(?P<amount>[\d,]+)\s*\$(?P<asset>BTC|ETH)\s*\(\s*\$?(?P<value>[\d,]+)',
    re.IGNORECASE,
)

# ── Pattern 8: Signal ID "SIGNAL ID: #2138 COIN: **$INJ**" ────────
_SIGNAL_ID_COIN_RE = re.compile(
    r'SIGNAL\s*(?:ID)?\s*[:\#]\s*\d+.*?COIN.*?\$?(?P<asset>[A-Z]{2,10})',
    re.IGNORECASE | re.DOTALL,
)

# ── Pattern 9: WallStreetQueen setup "Coin: #APTUSDT\nDirection: Long\nEntry: $0.95\nStop-loss: $0.92" ──
_WSQ_SETUP_RE = re.compile(
    r'Coin(?:\s*name)?\s*:\s*\**\#?(?P<asset>[A-Z]{2,10})USDT\**.*?'
    r'Direction\s*:\s*(?P<direction>Long|Short).*?'
    r'Entry\s*:\s*\$?(?P<entry>' + _PRICE_STR + r').*?'
    r'(?:Stop[-\s]?loss|SL)\s*:\s*\$?(?P<sl>' + _PRICE_STR + r')',
    re.IGNORECASE | re.DOTALL,
)

# ── Pattern 10: TP hit report "✔️✔️#APTUSDT✔️✔️\nTarget 1: 0.974$" ──
_WSQ_TP_HIT_RE = re.compile(
    r'✔️.*?#(?P<asset>[A-Z]{2,10})USDT.*?✔️\s*\n\s*\*{0,2}(?P<hits>\w+)\*{0,2}\s+Targets?\s+done',
    re.IGNORECASE | re.DOTALL,
)

# ── Price regexes for general extraction ──────────────────────────────
_ENTRY_RE = re.compile(
    r'(?:Entry|entry|Price|@|开仓价格)\s*(?:Point|Price)?\s*[:\s\$@]*\s*(?P<entry>' + _PRICE_STR + r')',
    re.IGNORECASE,
)
_SL_RE = re.compile(
    r'(?:Stop[-\s]?Loss|SL|Stop)\s*[:\s]+\s*(?P<sl>' + _PRICE_STR + ')',
    re.IGNORECASE,
)
_TP_ANY_RE = re.compile(
    r'(?:TP|Targets?)\s*[^\d]*(?P<tp>' + _PRICE_STR + r')',
    re.IGNORECASE,
)

# Inline TP without separator: "TP2507", "TP2504"
_TP_NO_SPACE_RE = re.compile(
    r'TP\s*[¹²³⁴⁵⁶⁷⁸⁹⁰]*\s*(?P<tp>' + _PRICE_STR + r')',
    re.IGNORECASE,
)
_LEVERAGE_RE = re.compile(
    r'(?:\*\*|\(|leverage|levier|杠杆)\s*(?P<leverage>\d+)\s*x',
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
    if raw is None: return None
    try: return float(raw.replace(",", "").replace(" ", ""))
    except: return None


def _extract_prices(text: str) -> dict:
    """Extract all price fields from text."""
    result = {}
    e = _ENTRY_RE.search(text)
    if e: result["entry"] = _parse_float(e.group("entry"))
    s = _SL_RE.search(text)
    if s: result["sl"] = _parse_float(s.group("sl"))
    # TPs from both patterns (with separator + without)
    tps1 = [_parse_float(m.group("tp")) for m in _TP_ANY_RE.finditer(text)]
    tps2 = [_parse_float(m.group("tp")) for m in _TP_NO_SPACE_RE.finditer(text)]
    tps = [t for t in tps1 + tps2 if t is not None]
    if tps: result["tps"] = tps
    lv = _LEVERAGE_RE.search(text)
    if lv: result["leverage"] = int(lv.group("leverage"))
    return result


def parse_telegram_message(raw_dict: dict) -> ParsedTelegramMessage:
    raw_text = raw_dict.get("raw_text", "")
    channel_alias = raw_dict.get("channel_alias", raw_dict.get("channel", ""))

    if not raw_text or not isinstance(raw_text, str):
        return ParsedTelegramMessage(message_type="UNKNOWN_RAW", raw_text=str(raw_text), channel_alias=channel_alias)

    asset = None; direction = None; extra = {}

    # ── Try GOLD trade formats (all variants) ──
    gold_dir = None
    gold_match = _GOLD_SIGNAL_RE.search(raw_text)
    if gold_match:
        gold_dir = "LONG" if gold_match.group("direction").upper() == "BUY" else "SHORT"
    if gold_dir is None:
        gold_match = _GOLD_XAUUSD_RE.search(raw_text)
        if gold_match:
            gold_dir = "LONG" if gold_match.group("direction").upper() == "BUY" else "SHORT"
    if gold_dir is None:
        gold_match = _GOLD_HASH_RE.search(raw_text)
        if gold_match:
            gold_dir = "LONG" if gold_match.group("direction").lower() == "buy" else "SHORT"
    if gold_dir is None:
        gold_match = _GOLD_STANDALONE_RE.search(raw_text)
        if gold_match:
            gold_dir = "LONG" if gold_match.group("direction").upper() == "BUY" else "SHORT"

    # Try forex pair format (SELL AUDJPY @ price, BUY GBPUSD price)
    if gold_dir is None:
        forex_match = _FOREX_PAIR_RE.search(raw_text)
        if forex_match:
            asset_candidate = forex_match.group("asset").upper()
            if asset_candidate in _VALID_FOREX_PAIRS:
                asset = asset_candidate
                direction = "LONG" if forex_match.group("direction").upper() == "BUY" else "SHORT"

    # Try crypto futures format (Buy/Long #BTCUSDT Entry: X Stop: X)
    if asset is None:
        cf_match = _CRYPTO_FUTURES_RE.search(raw_text)
        if cf_match:
            asset = cf_match.group("asset").upper()
            dir_raw = cf_match.group("direction").lower()
            direction = "LONG" if dir_raw in ("buy", "long") else "SHORT"
            extra["entry"] = _parse_float(cf_match.group("entry"))
            extra["sl"] = _parse_float(cf_match.group("sl"))
            # Extract targets from "Targets: X_Y Z" or "Targets: X, Y, Z"
            targets_m = _CRYPTO_TARGETS_RE.search(raw_text)
            if targets_m:
                targets_section = targets_m.group(1)
                tps = []
                for pm in re.finditer(r'(' + _PRICE_STR + r')', targets_section):
                    val = _parse_float(pm.group(1))
                    if val and val > 0.00001:
                        tps.append(val)
                if tps: extra["tps"] = tps

    if gold_dir is not None:
        asset = "XAUUSD"
        direction = gold_dir
        # Extract entry + SL (structured: "Entry: 4496 / 4488 SL: 4485")
        es = _GOLD_ENTRY_SL_RE.search(raw_text)
        if es:
            extra["entry"] = _parse_float(es.group("entry"))
            if es.group("sl"): extra["sl"] = _parse_float(es.group("sl"))
        # Extract inline entry price (first price after BUY/SELL, e.g. "BUY NOW 2354", "SELL 2262")
        if not extra.get("entry"):
            # Find the first number after the gold direction keyword
            after_match = raw_text[gold_match.end():] if gold_match else raw_text
            # Look for first standalone price (not preceded by TP/SL)
            entry_m = re.search(r'(?<!\d)\b(' + _PRICE_STR + r')\b', after_match)
            if entry_m:
                price = _parse_float(entry_m.group(1))
                # Validate: price should be reasonable for gold (1000-10000 range)
                if price and 1000 < price < 10000:
                    extra["entry"] = price
        # Extract SL from inline format ("SL @ 2360", "SL 2343", "❌SL 2343")
        # Extract SL/TP from inline format ("SL @ 2360 TP @ 2380")
        if not extra.get("sl"):
            sl_m = re.search(r'(?:SL|Sl)\s*[:\s@]+\s*(' + _PRICE_STR + r')', raw_text, re.IGNORECASE)
            if sl_m: extra["sl"] = _parse_float(sl_m.group(1))
        # Fallback: inline SL without separator ("SL2669", "SL.2610.50")
        if not extra.get("sl"):
            sl_m = _GOLD_NO_SPACE_SL_RE.search(raw_text)
            if sl_m: extra["sl"] = _parse_float(sl_m.group("sl"))
        # Extract all TPs
        tps = [_parse_float(m.group("tp")) for m in _GOLD_TPS_RE.finditer(raw_text)]
        tps = [t for t in tps if t is not None]
        # Dedupe: first TP might be the entry; skip if it matches entry
        if extra.get("entry") and tps and abs(tps[0] - extra["entry"]) < 0.01:
            tps = tps[1:]
        if tps: extra["tps"] = tps

    # ── Try structured COIN format ──
    if asset is None:
        m = _STRUCTURED_COIN_RE.search(raw_text)
        if m:
            asset = m.group("asset").upper()
            direction = m.group("direction").upper()
            lev = m.group("leverage")
            if lev: extra["leverage"] = int(lev)

    # ── Try WSQ setup format (Coin: #APTUSDT + Direction + Entry + Stop-loss) ──
    if asset is None:
        m = _WSQ_SETUP_RE.search(raw_text)
        if m:
            asset = m.group("asset").upper()
            direction = "LONG" if m.group("direction").upper() == "LONG" else "SHORT"
            extra["entry"] = _parse_float(m.group("entry"))
            extra["sl"] = _parse_float(m.group("sl"))
            # Extract all targets
            tps = [_parse_float(m.group("tp")) for m in _TP_ANY_RE.finditer(raw_text)]
            tps = [t for t in tps if t is not None]
            if tps: extra["tps"] = tps
            # Extract leverage
            lev_m = re.search(r'(?:Leverage|Lev)\s*:\s*(\d+)', raw_text, re.IGNORECASE)
            if lev_m: extra["leverage"] = int(lev_m.group(1))

    # ── Skip TP hit reports ──
    if asset is None:
        if _WSQ_TP_HIT_RE.search(raw_text):
            return ParsedTelegramMessage(message_type="TP_HIT", raw_text=raw_text, channel_alias=channel_alias)

    # ── Try Chinese long/short ──
    if asset is None:
        m = _CHINESE_LONG_RE.search(raw_text)
        if m:
            asset = m.group("asset").upper()
            direction = "LONG"
            extra["entry"] = _parse_float(m.group("entry"))
    if asset is None:
        m = _CHINESE_SHORT_RE.search(raw_text)
        if m:
            asset = m.group("asset").upper()
            direction = "SHORT"
            extra["entry"] = _parse_float(m.group("entry"))

    # ── Try free-text asset+dir ──
    if asset is None:
        m = _ASSET_PATTERN.search(raw_text)
        if m:
            asset = m.group("asset").upper()
            direction = "LONG" if m.group("direction").upper() in ("LONG", "BUY") else "SHORT"

    # ── Try hashtag coin ──
    if asset is None:
        m = _HASHTAG_COIN_RE.search(raw_text)
        if m:
            asset = m.group("asset").upper()
            direction = "LONG" if m.group("direction").upper() in ("LONG", "BUY") else "SHORT"

    # ── Try XAUHQ ──
    if asset is None:
        m = _XAUHQ_RE.search(raw_text)
        if m:
            asset = "XAUUSD"
            direction = None
            extra["entry"] = _parse_float(m.group("entry"))

    # ── Try signal ID coin ──
    if asset is None:
        m = _SIGNAL_ID_COIN_RE.search(raw_text)
        if m:
            asset = m.group("asset").upper()
            dm = re.search(r'Direction[:\s]+(?P<dir>LONG|SHORT)', raw_text, re.IGNORECASE)
            if dm: direction = dm.group("dir").upper()

    # ── Try whale transfer ──
    if asset is None:
        m = _WHALE_BTC_RE.search(raw_text)
        if m:
            asset = m.group("asset").upper()
            return ParsedTelegramMessage(
                message_type="CRYPTO_FLOW", raw_text=raw_text, channel_alias=channel_alias,
                claim={"claim_type": "CRYPTO_FLOW", "asset": asset,
                       "amount": m.group("amount").replace(",", ""),
                       "value_usd": m.group("value").replace(",", ""),
                       "source_channel": channel_alias})

    if asset is None:
        return ParsedTelegramMessage(message_type="UNKNOWN_RAW", raw_text=raw_text, channel_alias=channel_alias)

    # Validate against whitelist (skip structured coins, forex pairs, crypto futures)
    from_structured = _STRUCTURED_COIN_RE.search(raw_text) is not None
    from_forex = asset is not None and asset in _VALID_FOREX_PAIRS
    from_crypto_futures = _CRYPTO_FUTURES_RE.search(raw_text) is not None
    if not (from_structured or from_forex or from_crypto_futures) and asset not in _KNOWN_ASSETS:
        return ParsedTelegramMessage(message_type="UNKNOWN_RAW", raw_text=raw_text, channel_alias=channel_alias)

    # Extract all prices from text (supplements channel-specific extractions)
    prices = _extract_prices(raw_text)
    entry = extra.get("entry") or prices.get("entry")
    sl = extra.get("sl") or prices.get("sl")
    tps = extra.get("tps") or prices.get("tps", [])
    leverage = extra.get("leverage") or prices.get("leverage")

    claim = {
        "claim_type": "TRADE_SETUP",
        "asset": asset,
        "direction": direction,
    }
    if entry is not None: claim["entry"] = entry
    if sl is not None: claim["sl"] = sl
    if tps: claim["tp"] = tps[0]
    if len(tps) > 1: claim["tps"] = tps
    if leverage is not None: claim["leverage"] = leverage
    claim["source_channel"] = channel_alias

    return ParsedTelegramMessage(message_type="TRADE_SETUP", raw_text=raw_text,
                                  channel_alias=channel_alias, claim=claim)
