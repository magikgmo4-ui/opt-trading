# 04_ANALYSIS_SETS

## Jeux d'analyse par type d'ecran

| Screen type | Analyseur principal | Outputs principaux |
|---|---|---|
| `CHART_TECHNICAL_SCREEN` | technical chart analyzer | summary, signals, levels, risk_flags |
| `LIQUIDITY_DERIVATIVES_SCREEN` | liquidity / derivatives analyzer | detections, squeeze risk, funding state |
| `MACRO_CROSS_ASSET_SCREEN` | macro correlation analyzer | risk-on/off summary, divergence flags |
| `ETF_CRYPTO_SCREEN` | ETF relative strength analyzer | institutional proxy summary |
| `STOCK_SCREENER_SCREEN` | screener clustering analyzer | watchlist candidates, sector rotation |
| `NEWS_SENTIMENT_SCREEN` | event sentiment analyzer | urgency, impacted assets, catalyst summary |

## Format minimal d'une analyse

```json
{
  "capture_id": "uuid",
  "screen_type": "CHART_TECHNICAL_SCREEN",
  "asset": "BTCUSDT",
  "timeframe": "15m",
  "summary": "BTC teste une resistance avec volume en hausse.",
  "signals": [
    {
      "type": "breakout_attempt",
      "direction": "bullish",
      "confidence": 0.68,
      "evidence": ["price above VWAP", "volume increasing", "RSI rising"]
    }
  ],
  "levels": {
    "support": [104000, 102800],
    "resistance": [106500, 108000]
  },
  "risk_flags": ["funding elevated", "liquidity above current price"],
  "next_watch": "confirmation above resistance or rejection back below VWAP"
}
```

## Invariants analytiques

- un screenshot brut ne suffit pas
- chaque screenshot doit avoir un type
- chaque type doit avoir un analyseur dedie
- chaque capture doit produire un JSON
