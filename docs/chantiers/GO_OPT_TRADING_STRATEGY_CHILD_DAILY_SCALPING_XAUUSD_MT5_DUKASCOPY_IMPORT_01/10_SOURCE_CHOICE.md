---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01_SOURCE_CHOICE
doc_type: decision
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01
status: open
updated_at: 2026-05-20
---

# 10_SOURCE_CHOICE

## Comparatif MT5 vs Dukascopy

| Critère | MT5 export broker | Dukascopy tick data |
|---|---|---|
| Accès | broker MT5 requis (ICMarkets, Pepperstone, Darwinex...) | gratuit, inscription Dukascopy.com |
| Instrument | XAUUSD spot/CFD selon broker | XAUUSD spot interbank |
| Fenêtre | illimitée (depuis ouverture compte) | depuis 2003 |
| Granularité | M1 à MN nativement | tick → à resampler |
| bid/ask/spread | colonne `spread` nativement dans M5 export | bid + ask OHLC par tick → spread par bar |
| Effort | 5 min (History Center export) | ~30 min (download + resample Python) |
| Qualité spread | spread broker réel (variable) | spread interbank (très serré, non broker) |
| Sessions | sessions broker réelles | UTC interbank |
| Format export | CSV colonnes fixes MT5 | CSV bid/ask tick séparés |

## Recommandation

**MT5 si disponible** : le plus rapide, bid/ask/spread broker réel, sessions broker, effort minimal.

**Dukascopy si MT5 non disponible** : source institutionnelle de qualité, resample nécessaire mais script fourni dans ce chantier.

## Decision gate

```
Accès à un compte MT5 avec XAUUSD ?
  OUI → voir 20_MT5_EXPORT_RUNBOOK.md
  NON → voir 30_DUKASCOPY_IMPORT_RUNBOOK.md
```

## Brokers MT5 avec XAUUSD recommandés (pour référence)

| Broker | Accès démo | Spread XAUUSD typique |
|---|---|---|
| ICMarkets | oui | 0.10-0.30 USD |
| Pepperstone | oui | 0.13-0.40 USD |
| Darwinex | oui | 0.30-0.60 USD |
| XM | oui | 0.30-0.60 USD |

Un compte démo suffit pour exporter l'historique — pas besoin de compte réel.

## Période recommandée

```
Minimum  : 2024-01-01 → 2025-12-31 (24 mois)
Cible    : 2023-01-01 → 2025-12-31 (36 mois)
Raison   : couvrir phases trend (2023 bull), range (early 2024), high-vol news (2024-2025)
```
