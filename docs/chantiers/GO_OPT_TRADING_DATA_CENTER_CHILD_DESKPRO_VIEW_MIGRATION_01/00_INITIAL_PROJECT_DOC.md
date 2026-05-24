---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: desk_pro
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01
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
BUNDLE_TARGET: DESKPRO_VIEW_MIGRATION_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: null
topic_keys:
  - opt-trading
  - data_center
  - desk_pro
  - migration
  - market_metrics_reader
  - consumer_view
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_CLASS_VIEW_MARKET_METRICS_01/00_INITIAL_PROJECT_DOC.md
  - modules/desk_pro/service/market_metrics_reader.py
  - modules/data_center/registry/consumers.json
  - tests/test_desk_pro_market_metrics_reader.py
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01

## Objet

Migrer Desk Pro pour lire par défaut la vue neutre Data Center au lieu du chemin transitoire.

### Avant

```python
MARKET_METRICS_LATEST = Path("data/deskpro/inputs/market_metrics/latest.json")
```

### Après

```python
DC_MARKET_METRICS_VIEW = Path("data/data_center/views/market_metrics/latest.json")  # primary
MARKET_METRICS_LEGACY = Path("data/deskpro/inputs/market_metrics/latest.json")       # fallback
```

## 1_MASTER_TARGET

*(hérité)* Data Center opérationnel : rule `producer <> registry data <> consumer`.

## 6_FINAL_TARGET

`read_market_metrics()` utilise par défaut la vue neutre Data Center, avec fallback silencieux vers le chemin legacy si absent/malformé/vide. Aucun path par défaut ne référence un `producer_id`.

## 7_CANONICAL_STATE — après livraison

### `market_metrics_reader.py`

| Constante | Valeur | Rôle |
|---|---|---|
| `DC_MARKET_METRICS_VIEW` | `data/data_center/views/market_metrics/latest.json` | Path canonique (primary) |
| `MARKET_METRICS_LEGACY` | `data/deskpro/inputs/market_metrics/latest.json` | Fallback legacy |
| `MARKET_METRICS_LATEST` | alias → `DC_MARKET_METRICS_VIEW` | Backward compat |

Logique de résolution par défaut (`path=None`) :
1. Tente `DC_MARKET_METRICS_VIEW`
2. Si vide → tente `MARKET_METRICS_LEGACY`
3. Si les deux vides → retourne `[]`

Avec `path=` explicite : chemin direct, pas de fallback (comportement inchangé).

### `consumers.json`

`desk_pro__market_metrics` : `migration_needed → false`, `read_path_current → null`.

## 11_KEY_DECISIONS

- `_read_from_path()` helper extrait (DRY entre primary + fallback).
- Fallback silencieux : même sémantique que l'ancien comportement (`[]` sur échec).
- `MARKET_METRICS_LATEST` conservé comme alias pour ne pas casser les anciens monkeypatches.
- `TestAggregatorIntegration` mis à jour : patch `DC_MARKET_METRICS_VIEW` + `MARKET_METRICS_LEGACY`.
- `test_desk_pro_migration_needed` → `test_desk_pro_migration_complete` dans `test_contract_tests.py`.

## 12_INVARIANTS

- Aucun appel API, DB, Telegram.
- Aucune modification de `market_metrics_writer.py` ni des producers.
- `data/deskpro/inputs/market_metrics/` non supprimé.
- Tests existants non cassés.

## BUNDLE_TARGET — DESKPRO_VIEW_MIGRATION_V1

- [x] `DC_MARKET_METRICS_VIEW` constant + `MARKET_METRICS_LEGACY` fallback
- [x] `_read_from_path()` helper extrait
- [x] `read_market_metrics()` résolution primary → fallback
- [x] `consumers.json` : `migration_needed → false`
- [x] Tests `TestDefaultPathHierarchy` : 6 tests (path sans producer_id, DC primary, fallback, both absent, invalid fallback, explicit path)
- [x] `TestAggregatorIntegration` : 2 tests mis à jour
- [x] `test_contract_tests.py` : `test_desk_pro_migration_complete`
- [x] 28/28 reader PASS, 91/91 writer+layout+contract PASS
- [x] Total : **119 PASS**
