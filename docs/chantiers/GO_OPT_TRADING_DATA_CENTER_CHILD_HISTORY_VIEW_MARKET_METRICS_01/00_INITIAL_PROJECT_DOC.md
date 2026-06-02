---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_HISTORY_VIEW_MARKET_METRICS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_HISTORY_VIEW_MARKET_METRICS_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: closed
lifecycle_stage: implementation
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
MASTER_PROJECT_PLAN_ID: MPP_DATA_CENTER_NORMALIZED_REGISTRY
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
BUNDLE_TARGET: HISTORY_VIEW_MARKET_METRICS_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: null
topic_keys:
  - opt-trading
  - data_center
  - consumers
  - full_history
  - view_migration
  - perf_engine
  - history_view
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_BY_SYMBOL_CONSUMER_VIEW_01/90_REPRISE_POINT.md
  - modules/data_center/registry/consumers.json
  - modules/data_center/layout.py
  - modules/data_center/tests/test_contract_tests.py
  - modules/derivatives_collector/app/market_metrics_writer.py
  - modules/derivatives_collector/tests/test_market_metrics_writer.py
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_HISTORY_VIEW_MARKET_METRICS_01

## Objet

Corriger `perf_engine__replay_context` — dernier consumer encore couplé à un producer_id — et verrouiller le pattern `full_history` pour `market_metrics.v1`.

## Décision figée

```text
Un consumer full_history lit data/data_center/views/market_metrics/history/<SYMBOL>/<run_id>.json.
Un consumer full_history ne lit jamais un producer path ni un sous-répertoire producer (normalized/).
Un consumer non implémenté reste not_started ; on ne crée pas de faux reader.
```

## 1_MASTER_TARGET

*(hérité)* Data Center opérationnel : rule `producer <> registry data <> consumer`.

## 6_FINAL_TARGET

- `perf_engine__replay_context` : `full_history`, `read_path` corrigé → `views/market_metrics/history/`, verrouillé par tests.
- `write_market_metrics_history_view()` : new function, écrit `history/<SYMBOL>/<run_id>.json`, découplagée du producer_id.
- `layout.py` : `views/market_metrics/history/` créé par `ensure_data_center_dirs()`.
- Tests contractuels : `full_history` consumers couverts par invariants.

## 7_CANONICAL_STATE — après livraison

### Consumer `full_history` `market_metrics.v1`

| Consumer | read_path | Status | Reader réel |
|---|---|---|---|
| `perf_engine__replay_context` | `views/market_metrics/history/` | not_started | Non |

### Tests ajoutés

| Test | Fichier | Invariant |
|---|---|---|
| `test_not_implemented_consumers_remain_not_started` | `test_contract_tests.py` | +perf_engine dans le set no_reader |
| `test_full_history_consumers_read_from_view` | `test_contract_tests.py` | full_history → views/ |
| `test_full_history_consumers_have_no_producer_id_in_path` | `test_contract_tests.py` | no bitget/binance/normalized |
| `test_perf_engine_history_path_reachable_via_history_writer` | `test_contract_tests.py` | writer → consumer path atteignable |
| `TestWriteHistoryView` (6 tests) | `test_market_metrics_writer.py` | history writer invariants |
| `test_layout_creates_views_history_dir` | `test_layout.py` | layout crée le répertoire history |

## 11_KEY_DECISIONS

- `perf_engine__replay_context` : aucun reader dans le repo → `not_started` correct, aucun reader fantôme créé.
- `write_market_metrics_history_view()` : run_id default = metrics_ts sanitisé (colons strippés).
- History accumule les fichiers (pas de overwrite) ; consumer lit tout l'historique disponible.

## 12_INVARIANTS

- Aucun appel API, DB, Telegram.
- Aucun reader fantôme créé.
- Aucun path `full_history` ne référence un `producer_id` ni `normalized/`.
- Tests existants non cassés.

## BUNDLE_TARGET — HISTORY_VIEW_MARKET_METRICS_V1

- [x] `read_path` `perf_engine__replay_context` corrigé : `views/market_metrics/history/`
- [x] `write_market_metrics_history_view()` ajoutée dans `market_metrics_writer.py`
- [x] `layout.py` crée `views/market_metrics/history/`
- [x] 4 tests contractuels ajoutés dans `test_contract_tests.py`
- [x] 6 tests writer ajoutés dans `test_market_metrics_writer.py`
- [x] 1 test layout ajouté dans `test_layout.py`
- [x] 135/135 PASS (125 existants + 10 nouveaux)
