# GO_VOICE_OPERATOR_COMMAND_CONTRACTS_AUDIT_01 — Report

## Fixes Applied

### 1. market_view Bug Fix
`len(all_top)` → `len(cards)` — `all_top` was not defined in market_view scope.

### 2. Intent Router — 12 New Commands Mapped

| Command | Intent | Endpoint |
|---|---|---|
| Analyse BTC | btc_full | /read/composite |
| Analyse Gold | gold_full | /read/composite |
| Alertes Telegram | telegram_alerts | /read/composite |
| Setups actifs | setups_all | /read/composite |
| Setup BTC/Gold/SPCX | setup_detail | /read/composite |
| Score BTC/Gold/SPCX | score_detail | /read/composite |
| Rapport quotidien | daily_report | /read/composite |

No command falls back to `/read/system` unintentionally.

### 3. New Composite Handlers

- **btc_full**: Reads vision_analysis + market_metrics for price/trend/VWAP/RSI
- **telegram_alerts**: Reads alert counts + top 3 signals
- **setups_all**: Lists all active setups
- **setup_detail**: Shows setup for specific symbol (BTC, XAUUSD, SPCX)
- **score_detail**: Reads true_value DC views (grade, TV, confidence, hype, risk)
- **daily_report**: Reads latest daily report from stock_true_value outputs

### 4. Watchlists Dynamic

- **watchlist_ia**: Now reads `spacex_true_value.v1/by_symbol/` for NVDA, AVGO, AMD, MRVL, MU, PLTR
- **watchlist_spatial**: Now reads same for SPCX, RKLB, ASTS, LUNR
- Falls back to hardcoded values if DC views unavailable

### 5. Response Contract — `missing` + `next_action`

Every composite response now includes:

```json
{
  "missing": [],
  "next_action": ["Aucune action immediate requise"]
}
```

`missing` lists expected-but-absent fields (cards, spoken_text, one_line).
`next_action` gives operational hints.

## All Commands Now Resolve

```
etat systeme        → system_status
rapport marche      → market_view
analyse btc         → btc_full
analyse gold        → gold_full
resume spcx         → spcx_full
alertes telegram    → telegram_alerts
setups actifs       → setups_all
setup btc/gold/spcx → setup_detail
score btc/gold/spcx → score_detail
rapport quotidien   → daily_report
priorites           → priorities
attention           → attention
resume executif     → exec_summary
top movers          → top_movers
watchlist ia        → watchlist_ia
watchlist spatial   → watchlist_spatial
```

No fallback to /read/system except truly unknown commands.
