---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_STORAGE_RECONCILE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_STORAGE_RECONCILE_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
lifecycle_stage: implementation
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
MASTER_PROJECT_PLAN_ID: MPP_DATA_CENTER_NORMALIZED_REGISTRY
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
BUNDLE_TARGET: MARKET_METRICS_STORAGE_RECONCILED_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_TESTS_01
topic_keys:
  - opt-trading
  - data_center
  - market_metrics
  - registry_reconcile
  - writer
  - producer_contracts
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01/20_ACCEPTANCE_REPORT.md
  - modules/derivatives_collector/app/market_metrics_writer.py
  - modules/data_center/registry/producers.json
  - docs/index/inbox/GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_STORAGE_RECONCILE_01.md
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_STORAGE_RECONCILE_01

## Objet

Absorber `GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01` dans `PF_DATA_CENTER`.

Deux problèmes identifiés :
1. `producers.json` indiquait `partial` pour Bitget et Binance — faux après acceptance report FULL 6/6.
2. `market_metrics_writer.py` écrivait seulement vers `data/collectors/` et `data/deskpro/` — pas vers `data/data_center/`.

## 1_MASTER_TARGET

*(hérité)* Data Center opérationnel : rule `producer <> registry data <> consumer`.

## 6_FINAL_TARGET

Le writer `market_metrics.v1` écrit en priorité dans `data/data_center/derivatives/<producer_id>/` (canonique), puis optionnellement dans les chemins legacy/vue. `producers.json` reflète la couverture réelle FULL 6/6.

## 7_CANONICAL_STATE — après livraison

### `producers.json`

| Producer | Avant | Après |
|---|---|---|
| `derivatives_collector__bitget` | partial, 3/6 | **full, 6/6** |
| `derivatives_collector__binance` | partial, 3/6 | **full, 6/6** |
| `collector_binance_spot` | full | full (inchangé) |

### `market_metrics_writer.py` — nouvelles fonctions

| Fonction | Chemin cible | Statut |
|---|---|---|
| `write_market_metrics_to_data_center` | `data/data_center/derivatives/<producer_id>/latest.json` + `cache/by_symbol/` | **Canonique** |
| `publish_market_metrics` | Data Center + legacy + Desk Pro | **Pipeline complet** |
| `write_market_metrics_latest` | `data/collectors/derivatives/latest.json` | Legacy view |
| `write_market_metrics_by_symbol` | `data/collectors/derivatives/cache/by_symbol/` | Legacy view |
| `publish_market_metrics_for_deskpro` | `data/deskpro/inputs/market_metrics/` | Vue consumer Desk Pro (migration_needed) |

### `_PROVIDER_TO_PRODUCER_ID`

```python
"bitget"             -> "derivatives_collector__bitget"
"binance_derivatives"-> "derivatives_collector__binance"
"binance"            -> "derivatives_collector__binance"
```

## 11_KEY_DECISIONS

- Les 3 fonctions legacy conservées telles quelles — aucune regression.
- `publish_market_metrics()` est le point d'entrée recommandé pour les nouveaux appels.
- `data/deskpro/inputs/market_metrics/` reste valide pendant la période de migration Desk Pro.
- `GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01` est ABSORBÉ — ne pas merger en standalone.

## 12_INVARIANTS

- Aucun appel API externe.
- Aucune modification de `market_metrics_v1.py` ni `lifecycle_compat.py`.
- Aucun chemin legacy supprimé.
- Tests existants (25) non cassés.

## BUNDLE_TARGET — MARKET_METRICS_STORAGE_RECONCILED_V1

- [x] `producers.json` corrigé : Bitget + Binance = full 6/6
- [x] `write_market_metrics_to_data_center()` implémenté
- [x] `publish_market_metrics()` implémenté
- [x] Tests writer : 25 anciens + 17 nouveaux = **42 PASS**
- [x] Tests layout : 11 PASS
- [x] Total : **53 PASS**
- [x] Ancien child FAST_STORAGE_CACHE absorbé — reprise annotée
