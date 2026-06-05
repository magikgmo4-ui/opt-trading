---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01_RUNTIME_ACCESS_PROBLEM
doc_type: analysis
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
---

# 10_RUNTIME_ACCESS_PROBLEM

## Objet

Diagnostiquer le probleme d'acces runtime aux inventaires avant que DeskPro ou Strategy commencent a requeter massivement.

## 1. Situation actuelle

```text
modules/data_center/registry/
├── producers.json              (7 entries, ~3 KB)
├── consumers.json              (14 entries, ~5 KB)
├── pro_desk_data_inventory.json (~500 fields, ~150 KB)
└── source_candidates.json      (31 sources, ~30 KB)
```

Environnement de lecture actuel :
- `market_metrics_reader.py` lit `views/market_metrics/latest.json`
- `spot_snapshot_reader.py` lit `views/pair_market_snapshot/latest.json`
- Les readers DeskPro lisent des fichiers individuels, pas l'inventaire complet

Probleme futur :
- Quand les inventaires `pro_desk_data_inventory.json` et `source_candidates.json` seront utilises pour le source selector / resolver
- Chaque requete `resolve(contract_class, symbol, data_key)` devra croiser :
  - l'inventaire pour verifier que le data_key existe et sa priorite
  - les sources candidates pour lister les producers eligibles
  - le scoring pour choisir la meilleure source

## 2. Goulot identifie

```text
Requete: resolve("market_metrics.v1", "BTCUSDT", "open_interest")
    │
    ├── lit pro_desk_data_inventory.json (150 KB parse)
    ├── lit source_candidates.json (30 KB parse)
    ├── lit producers.json (3 KB parse)
    ├── calcule source_score pour chaque candidat
    ├── selectionne meilleur
    └── retourne canonical_value

Si 10 consumers × 10 symboles × 6 data_keys = 600 appels :
    → 600 × (150 + 30 + 3) = ~110 MB de JSON parse
    → ~10-30 secondes CPU juste pour parser les inventaires
```

## 3. Profil d'acces

| Type de donnee | Taille | Frequence acces | Modifie |
|---|---|---|---|
| pro_desk_data_inventory | ~150 KB | CHAQUE requete resolve() | Rarement (doc-only) |
| source_candidates | ~30 KB | CHAQUE requete resolve() | Rarement (ajout source) |
| producers.json | ~3 KB | CHAQUE requete resolve() | Ajout/retrait producer |
| consumers.json | ~5 KB | CHAQUE requete consumer setup | Ajout/retrait consumer |
| Contract schemas | ~2 KB/contract | Validation chaque write | Changement schema |
| Source scores | ~2 KB/source | A chaque scoring | Chaque evaluation |

## 4. Impact

```text
SANS OPTIMISATION :
  - 600 resolve()/min → 110 MB JSON parse/min → CPU bound
  - Latence p99 > 500ms par resolve
  - Risque de contention I/O si plusieurs consumers

AVEC OPTIMISATION :
  - Index compiles en memoire → 0 KB JSON parse par resolve
  - Latence p99 < 5ms par resolve
  - Pas de contention I/O
```

## 5. Separation des preoccupations

```text
COLD PATH (rare, lent accepte) :
  - Modification inventaire (ajout champ P0-P21)
  - Ajout source candidate
  - Registration nouveau producer/consumer
  - Mise a jour schema contract

HOT PATH (frequent, doit etre < 5ms) :
  - resolve(contract_class, symbol, data_key)
  - Validation schema d'un write producer
  - Lecture view par consumer
  - Check freshness / stale flag
```
