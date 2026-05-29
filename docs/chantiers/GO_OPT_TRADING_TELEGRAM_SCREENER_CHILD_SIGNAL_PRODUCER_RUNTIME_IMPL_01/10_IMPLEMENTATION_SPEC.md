# 10_IMPLEMENTATION_SPEC

## Signal producer

`signal/signal_producer.py` transforme un `ScreenerSignal` (parser output)
en `ScreenerProducedSignal` (canonical signal prêt pour Desk Pro).

### Format produit

```json
{
  "id": "uuid4",
  "source": "telegram_screener",
  "signal_type": "trade|news|alpha",
  "channel": "source_channel",
  "parsed_at": "ISO8601",
  "produced_at": "ISO8601",
  "payload": {
    "pair": "string | null",
    "direction": "LONG|SHORT|null",
    "entry_price": "number | null",
    "sl": "number | null",
    "tp": "number | null",
    "size": "string | null",
    "category": "string | null",
    "confidence": "HIGH|MEDIUM|LOW|null",
    "raw_text": "string",
    "summary": "string"
  }
}
```

### Règles de production

| Champ | Source |
|---|---|
| `id` | uuid4 généré à la production |
| `source` | "telegram_screener" (configurable) |
| `signal_type` | `ScreenerSignal.signal_type.value` |
| `channel` | `ScreenerSignal.source_channel` |
| `parsed_at` | `ScreenerSignal.parsed_at` |
| `produced_at` | datetime.now(timezone.utc) |
| `pair` | trade: pair; alpha: pair; news: null |
| `entry_price` | trade: price; else null |
| `sl`, `tp` | forward from parsed signal |
| `size` | forward from parsed signal |
| `category` | news: category; else null |
| `confidence` | forward from parsed signal |
| `summary` | généré selon type |

### Summary generation

| Type | Format |
|---|---|
| trade | `PAIR DIRECTION @ PRICE` |
| news | `[CATEGORY]` |
| alpha | `TICKER: message` |

## Desk Pro adapter

`signal/desk_pro_adapter.py` convertit `ScreenerProducedSignal` en
format `telegram_claim.v1` compatible avec Desk Pro.

### Mapping

| telegram_claim.v1 | Source |
|---|---|
| `input_class` | `"telegram_claim.v1"` |
| `claim_id` | `tg_claim_{timestamp}_{pair}` |
| `source` | `signal.source` |
| `channel_id` | `signal.channel` (overrideable) |
| `symbol` | `signal.pair` |
| `timeframe` | `"H1"` (default) |
| `claim_ts` | `signal.produced_at` |
| `claim_type` | trade→trade_context, news→news_alert, alpha→alpha_signal |
| `text` | `signal.raw_text` |
| `entities.direction` | lowercase direction |
| `entities.levels` | [entry_price, sl, tp] (non-null) |
| `entities.confidence` | HIGH→0.85, MEDIUM→0.60, LOW→0.35 |
