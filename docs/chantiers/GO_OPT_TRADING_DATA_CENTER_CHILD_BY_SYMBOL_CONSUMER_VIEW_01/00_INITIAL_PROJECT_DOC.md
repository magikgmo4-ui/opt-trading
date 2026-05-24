---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BY_SYMBOL_CONSUMER_VIEW_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BY_SYMBOL_CONSUMER_VIEW_01
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
BUNDLE_TARGET: BY_SYMBOL_CONSUMER_VIEW_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: null
topic_keys:
  - opt-trading
  - data_center
  - consumers
  - by_symbol
  - view_migration
  - strategy_framework
  - inventory
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_LATEST_CONSUMERS_VIEW_MIGRATION_01/90_REPRISE_POINT.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_CLASS_VIEW_MARKET_METRICS_01/00_INITIAL_PROJECT_DOC.md
  - modules/data_center/registry/consumers.json
  - modules/data_center/tests/test_contract_tests.py
  - modules/derivatives_collector/tests/test_market_metrics_writer.py
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_BY_SYMBOL_CONSUMER_VIEW_01

## Objet

Inventorier, vérifier et verrouiller le pattern consumer `by_symbol` pour `market_metrics.v1`. Compléter les tests invariants manquants pour la vue neutre `by_symbol`.

## Décision figée

```text
Un consumer by_symbol lit data/data_center/views/market_metrics/by_symbol/<SYMBOL>.json.
Un consumer by_symbol ne lit jamais un producer path (bitget/binance/derivatives_collector__).
Un consumer non implémenté reste not_started ; on ne crée pas de faux reader.
```

## 1_MASTER_TARGET

*(hérité)* Data Center opérationnel : rule `producer <> registry data <> consumer`.

## 6_FINAL_TARGET

- `strategy_framework__market_context` : `by_symbol`, `not_started`, `read_path` correct, verrouillé par tests.
- Writer `write_market_metrics_view()` : `by_symbol` path découplagé du producer_id, verrouillé par test.
- Tests contractuels : `by_symbol` consumers couverts par 4 nouveaux tests invariants.

## 7_CANONICAL_STATE — après livraison

### Consumer `by_symbol` `market_metrics.v1`

| Consumer | read_path | Status | Reader réel |
|---|---|---|---|
| `strategy_framework__market_context` | `views/market_metrics/by_symbol/` | not_started | Non |

### Tests ajoutés

| Test | Fichier | Invariant |
|---|---|---|
| `test_not_implemented_consumers_remain_not_started` | `test_contract_tests.py` | +strategy_framework dans le set no_reader |
| `test_by_symbol_consumers_read_from_view` | `test_contract_tests.py` | by_symbol → views/ |
| `test_by_symbol_consumers_have_no_producer_id_in_path` | `test_contract_tests.py` | no bitget/binance/derivatives_collector__ |
| `test_strategy_framework_by_symbol_path_reachable_via_view_writer` | `test_contract_tests.py` | writer → consumer path atteignable |
| `test_view_by_symbol_decoupled_from_producer_id` | `test_market_metrics_writer.py` | binance = bitget on by_symbol view path |

## 11_KEY_DECISIONS

- `strategy_framework__market_context` : aucun reader dans le repo → `not_started` correct, aucun reader fantôme créé.
- `write_market_metrics_view()` écrit déjà `by_symbol/<SYMBOL>.json` depuis #751 — ce GO verrouille les invariants.
- `test_view_path_decoupled_from_producer_id` existant ne couvrait que `latest` — nouveau test ajouté pour `by_symbol`.

## 12_INVARIANTS

- Aucun appel API, DB, Telegram.
- Aucun reader fantôme créé.
- Aucun path `by_symbol` ne référence un `producer_id`.
- Tests existants non cassés.

## BUNDLE_TARGET — BY_SYMBOL_CONSUMER_VIEW_V1

- [x] Inventaire complet (voir `10_BY_SYMBOL_CONSUMERS_INVENTORY.md`)
- [x] `read_path` `strategy_framework` correct : `views/market_metrics/by_symbol/`
- [x] 4 tests contractuels ajoutés dans `test_contract_tests.py`
- [x] 1 test writer ajouté dans `test_market_metrics_writer.py`
- [x] 125/125 PASS (121 existants + 4 nouveaux)
