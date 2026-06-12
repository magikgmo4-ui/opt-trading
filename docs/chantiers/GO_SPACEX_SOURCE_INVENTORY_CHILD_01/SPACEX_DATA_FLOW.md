# SPACEX_DATA_FLOW

```text
TradingView Alerts ─┐
Yahoo/Market APIs ──┤
SEC EDGAR ──────────┤
News RSS/API ───────┤
Bot Vision OCR ─────┤
Coinglass Context ──┤
Institutional ──────┘
        ↓
modules.ipo_tracking.collectors
        ↓
modules.ipo_tracking.storage
        ↓
data/ipo/spacex/raw/*.jsonl
        ↓
normalize + scoring
        ↓
data/ipo/spacex/scored/latest_snapshot.json
        ↓
data/data_center/views/spacex_super_desk/latest.json
        ↓
Desk UI / Telegram / Google Sheets / reports
```

## Contrat snapshot

Le snapshot contient :

- `asset`
- `market`
- `technical`
- `smart_money`
- `news`
- `sec`
- `institutional`
- `bot_vision`
- `coinglass_context`
- `scores`
- `setups`
- `alerts`
