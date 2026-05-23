---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_CLASS_VIEW_MARKET_METRICS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_CLASS_VIEW_MARKET_METRICS_01
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
BUNDLE_TARGET: CONTRACT_CLASS_VIEW_MARKET_METRICS_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: null
topic_keys:
  - opt-trading
  - data_center
  - contract_class_view
  - market_metrics
  - consumer_decoupling
  - writer
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_TESTS_01/00_INITIAL_PROJECT_DOC.md
  - modules/derivatives_collector/app/market_metrics_writer.py
  - modules/data_center/registry/consumers.json
  - modules/data_center/layout.py
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_CLASS_VIEW_MARKET_METRICS_01

## Objet

Corriger le couplage architectural identifié après `GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_TESTS_01`.

### Problème

`consumers.json` pointait les consumers `latest_only` vers le path producteur :

```text
data/data_center/derivatives/derivatives_collector__bitget/latest.json
```

Ce couplage est incorrect : Desk Pro ne doit pas connaître Bitget. Il doit connaître `market_metrics.v1`.

### Décision architecturale figée

```text
data/data_center/<family>/<producer_id>/  ← producteur écrit ici (inchangé)
data/data_center/views/<contract_class>/  ← consumer lit ici (nouveau)

Un consumer ne référence jamais un producer_id dans son read_path.
Un consumer lit une contract_class view.
```

## 1_MASTER_TARGET

*(hérité)* Data Center opérationnel : rule `producer <> registry data <> consumer`.

## 6_FINAL_TARGET

Vue neutre `market_metrics.v1` créée et câblée :

```text
data/data_center/views/market_metrics/
  latest.json          ← tous les producers latest_only lisent ici
  by_symbol/<SYMBOL>.json
```

`write_market_metrics_view()` alimente cette vue. `publish_market_metrics()` l'appelle en étape 2. `consumers.json` corrigé pour 4 consumers.

## 7_CANONICAL_STATE — après livraison

### Nouvelle fonction

| Fonction | Chemin cible | Statut |
|---|---|---|
| `write_market_metrics_view` | `data/data_center/views/market_metrics/latest.json` + `by_symbol/` | **Vue neutre** |

`publish_market_metrics()` signature étendue : `include_contract_view=True` (4e étape).

Retour dict étendu : `{"data_center": ..., "view": ..., "legacy": ..., "deskpro": ...}`.

### `consumers.json` — corrections

| Consumer | Avant | Après |
|---|---|---|
| `desk_pro__market_metrics` | `derivatives/.../bitget/latest.json` | `views/market_metrics/latest.json` |
| `telegram_screener__signal_context` | `derivatives/.../bitget/latest.json` | `views/market_metrics/latest.json` |
| `google_sheets__market_reporting` | `derivatives/.../bitget/latest.json` | `views/market_metrics/latest.json` |
| `strategy_framework__market_context` | `derivatives/.../bitget/cache/by_symbol/` | `views/market_metrics/by_symbol/` |
| `perf_engine__replay_context` | inchangé | `normalized/` (full_history — GO futur) |

### `layout.py`

`ensure_data_center_dirs()` crée `views/market_metrics/by_symbol/` à l'initialisation.

### `test_contract_tests.py` — assertions mises à jour

| Ancien test | Nouveau test |
|---|---|
| `test_desk_pro_reads_from_derivatives_producer_family` | `test_desk_pro_reads_from_contract_class_view` |
| `test_consumer_read_path_is_reachable_after_write` | `test_consumer_read_path_reachable_via_view_writer` |
| Nouveau : `test_latest_only_consumers_read_from_view` | enforce la règle pour tous les `latest_only` consumers |

## 11_KEY_DECISIONS

- Vue neutre = dernier write wins (multi-provider possible). Pas de merge/priorité dans ce GO.
- `perf_engine__replay_context` (`full_history/normalized/`) non migré : requiert une vue historique dédiée (GO futur).
- `desk_pro__spot_snapshot` non concerné : `pair_market_snapshot.v1`, pas `market_metrics.v1`.
- Tests : `TestWriteContractClassView` (6) + `TestPublishMarketMetricsView` (4) = 10 nouveaux tests.

## 12_INVARIANTS

- Aucun chemin legacy supprimé (`data/collectors/`, `data/deskpro/`).
- `write_market_metrics_to_data_center()` inchangé.
- Aucune modification de `market_metrics_v1.py` ni `lifecycle_compat.py`.
- Tests existants (42 writer + 11 layout) non cassés.

## BUNDLE_TARGET — CONTRACT_CLASS_VIEW_MARKET_METRICS_V1

- [x] `write_market_metrics_view()` implémenté
- [x] `publish_market_metrics()` étendu avec `include_contract_view=True`
- [x] `consumers.json` : 4 consumers migrés vers `views/market_metrics/`
- [x] `layout.py` : `views/market_metrics/` créé à l'init
- [x] `test_contract_tests.py` mis à jour : 28 tests, architecture correcte
- [x] Nouveaux tests : 10 (6 view + 4 publish_view)
- [x] Total : 91/91 PASS (42 writer + 11 layout + 28 contract + 10 nouveaux)
