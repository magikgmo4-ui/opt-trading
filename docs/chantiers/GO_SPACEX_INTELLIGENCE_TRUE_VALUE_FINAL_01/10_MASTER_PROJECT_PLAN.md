# 10_MASTER_PROJECT_PLAN

## Direction

Unifier trois surfaces :

1. **SPACEX_FINAL_CANONICAL** : IPO tracking, desk, collectors, data flow, UI, backtest.
2. **SPACEX_INTELLIGENCE_LAYER** : catalysts, Starlink, xAI, ecosystem watchlist.
3. **STOCK_TRUE_VALUE_ENGINE** : true value, hype, surprise, risk, confidence.

---

## Architecture cible

```text
TradingView / Yahoo / SEC / RSS / Bot Vision / Data Center / Manual Fixtures
        ↓
raw inputs
        ↓
normalized events
        ↓
SPACEX INTELLIGENCE SCORING
        ├── catalyst_score
        ├── ecosystem_score
        ├── price_action_score
        └── risk_penalty
        ↓
TRUE VALUE LAYER
        ├── fundamental_score
        ├── valuation_score
        ├── flow_score
        ├── surprise_score
        ├── hype_score
        ├── risk_score
        └── confidence_score
        ↓
final_score_engine
        ↓
outputs / Data Center draft / LocalCMS draft / reports / watchlists
```

---

## Workstreams

### WS1 — Canonical docs

Consolidated in this bundle.

### WS2 — Config + schema

Consolidated in this bundle.

### WS3 — Pure scoring module

Consolidated in this bundle under `modules/stock_true_value`.

### WS4 — Fixture-only dry run

Consolidated and upgraded in this bundle.

### WS5 — Data Center registration

Deferred to separate GO.

### WS6 — LocalCMS cards

Deferred to separate GO after Data Center output contract validation.

---

## Invariants

- No broker/order execution.
- No runtime activation inside this bundle.
- No registry active modification.
- No hidden background job.
- All scores 0-100.
- Every output must include `model_version`, `asof`, `confidence_score`, `source_health`.
