# 10_PARSER_SPEC

## Signaux supportés

| Type | Format attendu | Exemple |
|---|---|---|
| Trade setup | `PAIR: DIRECTION @ PRICE` | `BTCUSDT: LONG @ 65000` |
| News/Alert | `[CATEGORY] message` | `[MACRO] FOMC rate decision` |
| Alpha | `TICKER: alpha message` | `AAPL: breakout pattern detected` |

## Format normalisé

```json
{
  "source_channel": "string",
  "signal_type": "trade|news|alpha",
  "timestamp": "ISO8601",
  "parsed_at": "ISO8601",
  "raw_text": "string",
  "normalized": {
    "pair": "string | null",
    "direction": "LONG|SHORT|null",
    "price": "number | null",
    "sl": "number | null",
    "tp": "number | null",
    "size": "string | null",
    "category": "string | null",
    "confidence": "HIGH|MEDIUM|LOW|null"
  }
}
```

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
  tests/
    test_trade_parser.py
    test_news_parser.py
    test_alpha_parser.py
    test_signal_normalizer.py
  samples/
    trade_setup_samples.json
    news_samples.json
    alpha_samples.json
```
