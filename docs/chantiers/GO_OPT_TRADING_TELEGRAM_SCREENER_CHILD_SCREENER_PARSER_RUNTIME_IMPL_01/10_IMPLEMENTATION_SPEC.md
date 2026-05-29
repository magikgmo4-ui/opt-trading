# 10_IMPLEMENTATION_SPEC

## Signaux supportés

| Type | Format attendu | Exemple |
|---|---|---|
| Trade setup | `PAIR: DIRECTION @ PRICE [SL x] [TP x] [SIZE x]` | `BTCUSDT: LONG @ 65000 SL 64000 TP 66000 SIZE 1.5` |
| News/Alert | `[CATEGORY] message` | `[MACRO] FOMC rate decision` |
| Alpha | `TICKER: message` | `AAPL: breakout pattern detected` |

## Structure module

```text
modules/telegram_screener/
  parser/
    __init__.py
    trade_parser.py
    news_parser.py
    alpha_parser.py
    signal_normalizer.py
    signal_schema.py
```

## Format normalisé (ScreenerSignal)

```python
@dataclass
class ScreenerSignal:
    source_channel: str
    signal_type: SignalType       # trade | news | alpha
    timestamp: str                # ISO8601 (original ou now)
    parsed_at: str                # ISO8601 (now)
    raw_text: str
    pair: Optional[str]           # trade: pair; alpha: ticker
    direction: Optional[Direction] # LONG | SHORT | None
    price: Optional[float]
    sl: Optional[float]
    tp: Optional[float]
    size: Optional[str]
    category: Optional[str]       # news only
    confidence: Optional[Confidence] # HIGH | MEDIUM | LOW
    metadata: dict                # extras (message for alpha)
```

## Règles de parsing

### Trade parser
- Pattern regex: `PAIR: DIRECTION @ PRICE [SL x] [TP x] [SIZE x]`
- PAIR: 5-20 alphanum uppercase (e.g. BTCUSDT, ETHUSDT)
- DIRECTION: LONG, SHORT, or LONG_SHORT (→ direction=None)
- PRICE: float (comma support for thousands)
- SL/TP: optional float
- SIZE: optional string
- Confidence: HIGH if SL+TP, MEDIUM if SL or TP only, LOW if neither

### News parser
- Pattern: `[CATEGORY] message`
- Category: alphanumeric + underscore
- Confidence: MEDIUM (default for news)

### Alpha parser
- Pattern: `TICKER: message`
- Ticker: 1-10 alphanumeric
- Pair field = ticker (for schema alignment)
- Message stored in metadata
- Confidence: LOW (default for alpha)

## Dépendances

- Aucune dépendance externe
- Standard library only (re, datetime, dataclasses, enum)
