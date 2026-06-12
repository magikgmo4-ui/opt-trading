# 20_MEGA_DATA_CATALOG

## Raw

- Market quote raw.
- OHLCV raw.
- SEC filings raw.
- News raw.
- TradingView webhook payload raw.
- Bot Vision screenshot/OCR raw.
- Institutional raw.
- Context risk raw.

## Normalized

Contrat recommandé:

```json
{
  "source": "tradingview|sec_edgar|yahoo_chart|rss|bot_vision|institutional",
  "symbol": "SPCX",
  "ts": "ISO-8601",
  "event_type": "...",
  "payload": {},
  "quality": {
    "source_rank": 0,
    "freshness_sec": 0,
    "confidence": 0.0
  }
}
```

## Scored

Scores finaux:

- `momentum_score`
- `news_velocity_score`
- `technical_score`
- `smart_money_score`
- `risk_score`
- `trade_ready_score`
- `accumulation_score`
- `sector_halo_score`

## Retention

- raw: jamais supprimé sans politique explicite.
- normalized: rolling + snapshots.
- scored: latest + journal.
- reports: daily permanent.
- backtests: versionnés par setup et dataset.
