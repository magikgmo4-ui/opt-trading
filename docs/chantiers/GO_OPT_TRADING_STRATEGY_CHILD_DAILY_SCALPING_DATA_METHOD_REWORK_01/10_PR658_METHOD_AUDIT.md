---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01_PR658_METHOD_AUDIT
doc_type: method_audit
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01
status: closed
updated_at: 2026-05-20
---

# 10_PR658_METHOD_AUDIT

## Statut PR #658

```
TECHNICAL_SMOKE_PASS
STRATEGY_VERDICT_INVALID
DATA_METHOD_REWORK_REQUIRED
```

## Ce que PR #658 a livré (PASS)

| Item | Résultat |
|---|---|
| `fetch_data.py` | télécharge GC=F M5/M15 via yfinance sans crash |
| `report.py` empty guard | plus de crash sur journal vide |
| Runner end-to-end | `run_backtest.py` s'exécute de bout en bout |
| Setups détectés | 559 (ORB_ONLY 341 + VWAP_PULLBACK_ONLY 218) |
| Trades simulés | 455 (avec min_score=4) |

## Défauts de méthode (INVALID)

### 1 — Source de prix non conforme

| Propriété | Valeur PR #658 | Requis |
|---|---|---|
| Ticker | `GC=F` (Gold futures CME) | XAUUSD spot broker |
| Source | Yahoo Finance API | Prod collector / broker export |
| bid/ask | absent | obligatoire pour scalping |
| Spread réel | absent | obligatoire |
| Slippage broker | hardcodé 1.0 pip estimé | doit venir du feed broker |
| Timezone | UTC (converti de NY) | UTC broker normalisé |
| Sessions | déduites de l'heure UTC | doit matcher les sessions broker réelles |

### 2 — Fenêtre temporelle insuffisante et atypique

| Propriété | Valeur PR #658 | Requis |
|---|---|---|
| Durée | 60 jours (limite yfinance intraday) | minimum 6 mois, idéal 1-2 ans |
| Période | Mars–Mai 2026 | inclure trend day, range day, news day |
| Contexte marché | Gold +15% en 2 mois (bullrun extrême) | distribution multi-régimes |
| Représentativité | non représentatif | doit couvrir les 4 régimes cibles |

### 3 — SMC_SWEEP_ONLY et COMBINED non testés

| Problème | Détail |
|---|---|
| 0 setups détectés | condition CHOCH = `close > last_swing_high` dans le même bar M5 |
| Condition irréaliste | nécessite un move de 15-20 pts en une seule bougie 5 minutes |
| Conséquence | les 2 variants les plus complexes sont complètement absents du verdict |

**Root cause CHOCH proxy actuel** (detectors.py) :
```python
swept = prev["low"] < swing_l and row["close"] > swing_l
if swept and swing_h is not None and row["close"] > swing_h:
    # setup long
```

La condition `row["close"] > swing_h` doit être vérifiable dans une fenêtre de 3 à 10 bougies suivantes, pas dans le même bar que le sweep.

### 4 — Filtre min_score incompatible

| Problème | Détail |
|---|---|
| Score max ORB_ONLY | 5/10 (pas de structure_state, pas de CHOCH) |
| Score max VWAP_PULLBACK | 4/10 (pas de liquidity_state ni orb_state) |
| min_score spec | 7/10 |
| Contournement PR #658 | `--min-score 4` utilisé pour faire tourner ORB/VWAP |
| Conséquence | le run viole la spec du runner — hors conditions normales d'usage |

**Correction nécessaire** : soit des seuils min_score par variant, soit définir que min_score=7 s'applique uniquement à COMBINED.

### 5 — Résultats non exploitables comme verdict stratégique

```
ORB_ONLY          : expectancy=-0.085R, PF=0.873  → REJECT sur 341 trades
VWAP_PULLBACK_ONLY: expectancy=-0.210R, PF=0.707  → REJECT sur 114 trades
SMC_SWEEP_ONLY    : 0 trades              → NO_DATA
COMBINED          : 0 trades              → NO_DATA
```

Ces résultats ne peuvent pas être utilisés pour rejeter `SMC_ORB_VWAP_SCALP_A_PLUS` car :
- La stratégie cible est COMBINED — qui n'a généré aucun setup
- La source n'est pas le bon instrument
- La fenêtre n'est pas représentative

## Leçons

1. Définir la source de données avant d'écrire le runner
2. Ne jamais produire un verdict sur proxy Yahoo/futures
3. Le contrat OHLCV doit inclure bid/ask/spread dès le début
4. Le CHOCH doit avoir une fenêtre de confirmation configurable
5. min_score doit être défini par variant ou la spec doit être clarifiée
