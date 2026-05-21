---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01_CANONICAL_CONTRACT_GAP
doc_type: gap_analysis
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01
status: closed
audited_at: 2026-05-20
---

# 40_CANONICAL_CONTRACT_GAP

## Contrat cible (rappel)

Défini dans `GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01/30_CANONICAL_OHLCV_CONTRACT.md` :

```text
timestamp, open, high, low, close, volume, bid, ask, spread, source, symbol, timeframe
```

## Comparaison toutes sources

| Champ | Yahoo/GC=F (smoke) | simex_bitget_bridge | MT5 export | Dukascopy tick |
|---|---|---|---|---|
| `timestamp` | UTC converti | ms epoch → UTC | UTC ou local | UTC tick |
| `open` | ✅ | ✅ | ✅ | ✅ (resampleé) |
| `high` | ✅ | ✅ | ✅ | ✅ |
| `low` | ✅ | ✅ | ✅ | ✅ |
| `close` | ✅ | ✅ | ✅ | ✅ |
| `volume` | ✅ (futures vol) | ✅ (baseVol) | ✅ (tick_volume) | ✅ (tick count) |
| `bid` | ❌ absent | ❌ absent | ⚠️ estimable via spread | ✅ bid OHLC par bar |
| `ask` | ❌ absent | ❌ absent | ⚠️ estimable via spread | ✅ ask OHLC par bar |
| `spread` | ❌ hardcodé config | ❌ absent (ticker approximatif) | ✅ colonne `spread` dans MT5 | ✅ ask-bid par bar |
| `source` | ❌ implicite | ⚠️ à ajouter | ✅ à ajouter | ✅ à ajouter |
| `symbol` | GC=F (faux) | XAUUSDT (approx) | XAUUSD | XAUUSD |
| `timeframe` | M5/M15 | M5 (configurable) | M5/M15 | resamplé M5/M15 |
| Instrument | futures CME | futures Bitget | **spot/CFD broker** | **spot interbank** |
| Fenêtre max | 60j (yfinance) | à vérifier | illimitée (export) | illimitée (archive) |

## Classement par complétude canonique

| Source | Score contrat | Classification | Verdict |
|---|---|---|---|
| MT5 export broker | 9/10 | PRIMARY_READY | ✅ Recommandé bootstrap |
| Dukascopy tick → M5 | 10/10 | PRIMARY_READY | ✅ Recommandé si accessible |
| simex_bitget_bridge adapté | 7/10 | PRIMARY_WITH_GAPS | ⚠️ Acceptable avec effort |
| Yahoo/GC=F | 4/10 | SMOKE_ONLY | ❌ Interdit pour verdict |

## Gaps par priorité

### CRITIQUE (bloque le verdict)

1. **bid/ask/spread absent de toutes les sources actuelles dans le repo**
   - Impact : simulateur utilise spread hardcodé 3.0 pips — fausse les résultats scalping
   - Solution MT5 : colonne `spread` native disponible dans l'export
   - Solution Dukascopy : bid/ask OHLC par bar → spread = ask_close - bid_close
   - Solution Bitget : approximation via ticker API, non idéal

2. **Fenêtre 60j insuffisante (source Yahoo actuelle)**
   - Impact : trop court pour SMC/COMBINED atteindre 100 trades
   - Solution : MT5 (illimité) ou Dukascopy (archive 2003+)

### IMPORTANT (affecte la qualité du verdict)

3. **Instrument XAUUSDT vs XAUUSD**
   - XAUUSDT Bitget futures ≠ XAUUSD spot broker
   - Basis futures/spot : quelques $/oz — acceptable pour backtest scalping M5 si documenté
   - Funding rate Bitget : ignoré dans backtest intraday

4. **Sessions broker non définies**
   - Les sessions London/NY actuelles dans indicators.py sont des approximations UTC
   - Un export broker MT5 XAUUSD aura les sessions réelles du broker

### FAIBLE (n'affecte pas la validité du verdict)

5. **Output HTTP push vs fichier** (simex_bitget_bridge)
6. **Pattern famille collector** (manifest/status/events)
7. **source field explicite** — simple à ajouter

## Conclusion gap analysis

```
Aucune source dans le repo n'est PRIMARY_READY aujourd'hui.
simex_bitget_bridge est PRIMARY_WITH_GAPS (effort ~1 jour).
MT5/Dukascopy sont PRIMARY_READY mais externes au repo.
```

La décision bootstrap (MT5/Dukascopy) vs adaptation collector (simex_bitget_bridge) est dans `50_SOURCE_DECISION.md`.
