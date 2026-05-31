# 03_TRIGGER_ENGINE

## Maximum data trigger

### A. Triggers horaires fixes

| Moment | Pourquoi | Captures |
|---|---|---|
| 04:00-05:00 ET | pre-market Europe / commodities | DXY, gold, oil, BTC |
| 08:00-09:30 ET | pre-market US | stocks, ETF, BTC, DXY |
| 09:30 ET | open US | BTC, ETF, stocks, DXY, gold |
| 10:00-11:00 ET | confirmation open | charts + liquidity |
| 14:00 ET | Fed / macro window | DXY, yields, gold, BTC |
| 16:00 ET | close US | ETF, stocks, BTC |
| 20:00 ET | futures / Asia prep | BTC, gold, oil |
| Funding windows | perp pressure | Coinglass / exchange |

### B. Triggers prix / volatilite

Declencher capture si :

- `price_change_5m >= seuil`
- `price_change_15m >= seuil`
- `ATR_spike = true`
- `volume_relative > 2.0`
- breakout previous high / low
- cross EMA 20/50/200
- supertrend flip
- RSI > 70 ou < 30
- MACD cross
- VWAP reclaim / rejection

### C. Triggers liquidite

- `open_interest_change` eleve
- `funding_rate` extreme
- `liquidation_cluster` proche du prix
- `long_short_ratio` desequilibre
- `orderbook imbalance` visible
- `large liquidation event`

### D. Triggers macro

- DXY breakout / breakdown
- US10Y spike
- Gold breakout
- Oil breakout
- VIX spike
- BTC diverge fortement du DXY ou gold

### E. Triggers screener

- stock relative volume > 2
- stock move > 3% intraday
- mega cap move > 1.5%
- sector cluster actif
- AI / defense / space trend detectee
- crypto stocks bougent avec BTC

## Pipeline recommande

```text
1. Scheduler / trigger engine
2. Capture screenshot
3. Normalisation fichier image
4. Metadonnees capture
5. Analyse vision par type d'ecran
6. JSON structure
7. Data Center ingestion
8. Telegram resume court
9. DeskPro vue longue / historique / recherche
```
