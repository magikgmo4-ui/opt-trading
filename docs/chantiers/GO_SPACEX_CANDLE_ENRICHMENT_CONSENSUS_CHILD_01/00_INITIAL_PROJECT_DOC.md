# GO_SPACEX_CANDLE_ENRICHMENT_CONSENSUS_CHILD_01

## 00_INITIAL_PROJECT_DOC

### Objectif

Transformer chaque chandelle SPCX brute en chandelle enrichie multi-sources avec suffisamment de features pour backtests, setups, alertes et décision.

### Livrables

- `modules/ipo_tracking/enrichment/` — package d'enrichissement
- `schemas/ipo/spacex_enriched_candle.schema.json` — contrat de chandelle enrichie
- `scripts/ipo/spacex_enrich_candles.sh` — enrichment smoke
- `scripts/ipo/spacex_verify_enriched_candles.sh` — vérification

### Architecture

```text
bars OHLCV brutes
     │
     ▼
indicators.py ──── 23 indicateurs techniques locaux
smart_money.py ─── FVG, OB, BOS, CHOCH, liquidité, premium/discount
source_consensus.py ─── consensus multi-source avec score de désaccord
     │
     ▼
candle_enricher.py ─── orchestrateur
     │
     ▼
spacex_enriched_candle.v1  (56 features)
```

### Features produites par chandelle

| Domaine | Count | Examples |
|---|---|---|
| Candle base | 9 | OHLCV, vwap, source, confidence, session |
| Indicators | 23 | EMA 9/20/50/200, SMA 20/50/200, RSI 14, MACD, ATR 14, BB, RelVol, Vol Z-score, OR 5/15/30m, gaps |
| Smart Money | 14 | FVG, Order Blocks, Liquidity Sweeps, BOS, CHOCH, Equal Highs/Lows, Premium/Discount, SMC score, SMC bias |
| Consensus | 7 | consensus_price, source_count, trusted_source_count, disagreement_score, stale/missing sources |
| Mega Scores | 10 | momentum, volatility, liquidity, news, catalyst, smart_money, trend, risk, trade_ready, accumulation |
| Context | 4 | news_count, sec_filings_count, bot_vision_available, tv_alert_active |

### Smoke

```bash
bash scripts/ipo/spacex_enrich_candles.sh    # SPACEX_ENRICH_OK
bash scripts/ipo/spacex_verify_enriched_candles.sh  # SPACEX_VERIFY_ENRICHED_OK
```
