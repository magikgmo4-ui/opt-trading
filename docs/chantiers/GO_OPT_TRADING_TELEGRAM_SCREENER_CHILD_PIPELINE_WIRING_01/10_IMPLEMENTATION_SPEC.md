---
doc_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_PIPELINE_WIRING_01_IMPLEMENTATION_SPEC
doc_type: implementation_spec
repo: opt-trading
go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_PIPELINE_WIRING_01
status: open
lifecycle_stage: implementation
surface: modules/telegram_screener
created_at: 2026-05-28
updated_at: 2026-05-28
---

# 10_IMPLEMENTATION_SPEC — GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_PIPELINE_WIRING_01

## Pipeline interface

```python
@dataclass
class PipelineResult:
    raw_text: str
    channel_alias: str
    signal: Optional[ScreenerSignal]
    route: Optional[RouteDecision]
    produced: Optional[ScreenerProducedSignal]
    claim: Optional[dict]
    error: Optional[str]
    succeeded: bool  # computed: error is None and claim is not None

class ScreenerPipeline:
    def __init__(self, registry: Optional[ChannelRegistry] = None, min_tier: TrustTier = TrustTier.D)
    def run(self, raw_text: str, channel_alias: str) -> PipelineResult
    def run_batch(self, inputs: list[tuple[str, str]]) -> list[PipelineResult]
```

## Pipeline steps

1. **classify** — `classify_raw_text(raw_text)` → "trade" | "news" | "alpha" | None
2. **parse** — call matching parser → `ScreenerSignal`
3. **route** — `FilterRouter.route(signal)` → `RouteDecision`
4. **produce** — `produce_screener_signal(signal)` → `ScreenerProducedSignal`
5. **adapt** — `adapt_to_telegram_claim(produced)` → `telegram_claim.v1` dict

## Error handling

| Étape | Condition | error |
|---|---|---|
| classify | raw_text ne match aucun parser | "unparseable: ..." |
| parse | parser retourne None | "parse failed: ..." |
| route | route rejected | "rejected: ..." |
| produce/adapt | toujours réussi (pure functions) | — |

## Module structure

```
modules/telegram_screener/pipeline/
  __init__.py    # ScreenerPipeline + PipelineResult
```
