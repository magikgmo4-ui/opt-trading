# GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_GAP_MATRIX_AND_CONTRACTS_01

## Objectif

Compléter l'inventaire Desk Pro avec :
1. Contrats JSON Schema pour tous les contract_class existants
2. Gap matrix complète P0-P21 vs existant Data Center
3. Optimisation de `pro_desk_data_inventory.json` (split par priorité)

## Contexte

- PR #1094: pro_desk_data_inventory.json + source_candidates.json (mergée)
- PR #1095: registry cache + source_selector (mergée)
- PR #1098: canonical_value_publisher + 12/12 PROVEN (mergée)
- PR #1100: runtime validation PASS (mergée)

## Livrables

### 1. Contrats JSON Schema (`modules/data_center/contracts/`)

| Fichier | Description |
|---|---|
| `market_metrics.v1.schema.json` | Prix + 24h change, CoinGecko/Binance |
| `pair_market_snapshot.v1.schema.json` | Snapshot OHLCV pour Desk Pro |
| `canonical_value.v1.schema.json` | Valeur canonique résolue |
| `resolver_decision.v1.schema.json` | Décision du resolver (quelle source, pourquoi) |
| `source_score.v1.schema.json` | Score de fiabilité multi-dimensionnel |

### 2. Gap Matrix

`PRO_DESK_DATA_GAP_MATRIX.md` — 36 items classés par statut :
- 13 PROVEN, 4 PARTIAL, 4 DECLARED, 14 MISSING, 1 FUTURE

### 3. Optimisation inventory

`pro_desk_data_inventory_index.json` — index léger pointant vers les fichiers split par priorité (P0.json, P1.json...). Évite de charger l'inventaire complet en mémoire.

## Tests

```bash
# Validate all schemas are valid JSON
python3 -c "import json; [json.load(open(f'modules/data_center/contracts/{f}')) for f in ['market_metrics.v1.schema.json','pair_market_snapshot.v1.schema.json','canonical_value.v1.schema.json','resolver_decision.v1.schema.json','source_score.v1.schema.json']]; print('5 schemas OK')"
```
