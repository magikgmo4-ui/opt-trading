---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01_SOURCE_DECISION
doc_type: decision
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01
status: open
updated_at: 2026-05-20
---

# 50_SOURCE_DECISION

## Synthèse de l'audit

```
collector_binance_spot  → NOT_RELEVANT
collector_coingecko     → NOT_RELEVANT
derivatives_collector   → CONTEXT_ONLY (rôle correct, aucune adaptation)
simex_bitget_bridge     → PRIMARY_WITH_GAPS (seul candidat repo)

Aucune source dans le repo = PRIMARY_READY aujourd'hui.
```

## Classification finale par collector

| Collector | Classification | Raisonnement |
|---|---|---|
| `collector_binance_spot` | NOT_RELEVANT | Crypto 24h snapshot, pas de klines, pas de XAUUSD |
| `collector_coingecko` | NOT_RELEVANT | Crypto seulement, pas de XAUUSD |
| `derivatives_collector` | CONTEXT_ONLY | Métriques dérivatives (OI/funding/liq/L/S), jamais source OHLCV |
| `simex_bitget_bridge` | PRIMARY_WITH_GAPS | XAUUSDT M5 via Bitget, gaps : CSV output, pagination 180j, bid/ask |

## Recommandation stratégique

### Court terme — Bootstrap rapide (débloque le verdict en 1-2 jours)

```
MT5 export broker XAUUSD
```

Raison : export CSV natif avec colonne `spread`, instrument correct (XAUUSD spot/CFD), fenêtre illimitée, aucun développement requis.

Procédure :
```
MT5 → History Center → XAUUSD → M5 → Export CSV (minimum 2024-01-01 → 2025-12-31)
MT5 → History Center → XAUUSD → M15 → Export CSV (même période)
→ Normaliser vers contrat canonique (renommage colonnes + ajout source=mt5_export)
→ data/market/xauusd_m5_canonical.csv + xauusd_m15_canonical.csv
→ Rejouer run_backtest.py → verdict valide
```

Si MT5 non disponible, alternative :
```
Dukascopy → XAUUSD tick CSV → resample M5/M15 en Python
→ bid/ask OHLC par bar → spread natif → source=dukascopy
```

### Moyen terme — Collector durable (adapte simex_bitget_bridge)

```
simex_bitget_bridge → mode export CSV + pagination historique
```

Effort estimé : 1 journée de développement.

Adaptations nécessaires :
1. Ajouter `--mode export_csv` → écrit `data/market/xauusd_m5_bitget.csv` (au lieu de HTTP push)
2. Implémenter pagination historique (startTime/endTime, boucle par blocs de N bougies) pour atteindre 180j
3. Capturer spread approximatif via Bitget ticker API (snapshot au moment du fetch)
4. Ajouter champ `source=bitget_xauusdt_futures` explicitement
5. Documenter XAUUSDT vs XAUUSD dans la config

Ce chantier sera : `GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_XAUUSD_BOOTSTRAP_01`.

### Contexte — derivatives_collector (aucune adaptation bloquante)

Ajouter XAUUSDT à la config derivatives_collector pour enrichir les setups avec OI/funding/liq lors du backtest. Non bloquant pour le verdict. Enrichissement optionnel.

## Séquence recommandée

```
Étape 1 (J+0 à J+2)
  → Obtenir MT5/Dukascopy export XAUUSD M5/M15, minimum 1 an
  → Normaliser vers contrat canonique
  → Rejouer run_backtest.py avec données canoniques
  → Produire verdict stratégique valide

Étape 2 (J+5 à J+10)
  → Adapter simex_bitget_bridge : mode CSV + pagination 180j
  → Remplacer MT5 par Bitget comme source durable
  → Intégrer derivatives_collector XAUUSDT comme couche contextuelle

Étape 3 (optionnel, post-verdict)
  → Rework code detectors/scorer/simulator (CHOCH multi-bar, min_score par variant)
  → Backtest final avec données canoniques + derivatives + rework code
  → Verdict stratégique reproductible
```

## Ce qui ne change pas

- Yahoo/GC=F reste `SMOKE_ONLY` — jamais source de verdict
- `derivatives_collector` reste `CONTEXT_ONLY` — jamais source OHLCV
- bot vision reste couche evidence — jamais source OHLCV

## Prérequis immédiats

Pour l'Étape 1 :

```
[ ] Accès à MetaTrader 5 avec historique XAUUSD M5 (broker XAUUSD : ICMarkets, Pepperstone, Darwinex...)
[ ] OU accès Dukascopy (gratuit, historique 2003+, tick data → resample)
[ ] Python pandas installé (déjà OK)
[ ] Script de normalisation CSV (à écrire : ~30 min)
```
