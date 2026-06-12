# End-to-End Architecture

```text
TradingView alerts        Bot Vision screenshots       SEC/news/API collectors
      │                          │                           │
      ├──────────────┬───────────┴─────────────┬─────────────┤
                     ↓                         ↓
              raw event store             normalized event store
                     ↓                         ↓
              scoring engine ─────→ spacex_super_desk.v1
                     ↓                         ↓
        Data Center latest view       UI / reports / Telegram / Sheets
                     ↓
              Trading Lab + Backtest
                     ↓
          Accumulation + leverage-momentum decision support
```

## Contracts

- Raw: `data/ipo/spacex/raw/events.jsonl`
- Scored: `data/ipo/spacex/scored/latest_snapshot.json`
- Data Center: `data/data_center/views/spacex_super_desk/latest.json`
- UI: `ui/spacex_desk/index.html`
- Reports: `reports/ipo/spacex/`
