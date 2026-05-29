---
doc_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_FILTRAGE_ROUTAGE_01_IMPLEMENTATION_SPEC
doc_type: implementation_spec
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_FILTRAGE_ROUTAGE_01
status: open
lifecycle_stage: implementation
surface: modules/telegram_screener
created_at: 2026-05-28
updated_at: 2026-05-28
---

# 10_IMPLEMENTATION_SPEC — GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_FILTRAGE_ROUTAGE_01

## Router interface

```python
@dataclass
class RouteDecision:
    signal: ScreenerSignal
    accepted: bool
    channel: Optional[Channel]
    rejection_reason: Optional[str]
    metadata: dict

class FilterRouter:
    def __init__(self, registry: ChannelRegistry, min_tier: TrustTier = TrustTier.D)
    def route(self, signal: ScreenerSignal) -> RouteDecision
    def route_batch(self, signals: list[ScreenerSignal]) -> list[RouteDecision]
```

## Filter rules (in order)

1. **channel existence** — `registry.by_alias(signal.source_channel)` — if None → reject
2. **enabled flag** — `channel.enabled` — if False → reject
3. **trust_tier** — `channel.trust_tier > min_tier` — if below → reject (trust_tier A < B < C < D where A is highest)
4. **expected_parsers** — map `SignalType` → parser names, check overlap with `channel.expected_parsers`
5. **category** — soft warning in `metadata["category_mismatch"]`, does not reject

## Signal type to parser mapping

| SignalType | expected_parsers |
|---|---|
| TRADE | trade_claim, setup |
| NEWS | news |
| ALPHA | alpha |

## Module structure

```
modules/telegram_screener/router/
  __init__.py    # FilterRouter + RouteDecision
```

## Dependencies

- `modules/telegram_screener/parser/` — ScreenerSignal, SignalType
- `modules/telegram_screener/registry/` — Channel, ChannelRegistry, TrustTier
