---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_LATEST_CONSUMERS_VIEW_MIGRATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_LATEST_CONSUMERS_VIEW_MIGRATION_01
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
BUNDLE_TARGET: LATEST_CONSUMERS_VIEW_MIGRATION_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: null
topic_keys:
  - opt-trading
  - data_center
  - consumers
  - latest_only
  - view_migration
  - inventory
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_CLASS_VIEW_MARKET_METRICS_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01/90_REPRISE_POINT.md
  - modules/data_center/registry/consumers.json
  - modules/data_center/tests/test_contract_tests.py
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_LATEST_CONSUMERS_VIEW_MIGRATION_01

## Objet

Inventorier et vérifier l'état de migration de tous les consumers `market_metrics.v1` + `latest_only` vers la vue neutre Data Center. Verrouiller les invariants manquants par des tests.

## Décision figée

```text
Un consumer latest_only lit une contract-class view.
Un consumer latest_only ne lit jamais un producer path.
Un consumer non implémenté reste not_started ;
on ne crée pas de faux reader pour satisfaire le registre.
```

## 1_MASTER_TARGET

*(hérité)* Data Center opérationnel : rule `producer <> registry data <> consumer`.

## 6_FINAL_TARGET

Tous les consumers `latest_only` + `market_metrics.v1` ont :
- `read_path` → `data/data_center/views/market_metrics/latest.json`
- pas de `producer_id` dans le path
- `implementation_status` cohérent avec l'existence d'un reader réel

## 7_CANONICAL_STATE — après livraison

### État consumers `latest_only` + `market_metrics.v1`

| Consumer | read_path | Status | Migration | Reader réel |
|---|---|---|---|---|
| `desk_pro__market_metrics` | `views/market_metrics/latest.json` | implemented | false | Oui — `market_metrics_reader.py` |
| `telegram_screener__signal_context` | `views/market_metrics/latest.json` | not_started | false | Non |
| `google_sheets__market_reporting` | `views/market_metrics/latest.json` | not_started | false | Non |

### Tests ajoutés à `test_contract_tests.py`

| Test | Classe | Invariant |
|---|---|---|
| `test_not_implemented_consumers_remain_not_started` | `TestConsumerRegistryConsistency` | telegram + sheets restent `not_started` |
| `test_latest_only_consumers_have_no_producer_id_in_path` | `TestRegistryAlignment` | aucun path `latest_only` ne contient `bitget`/`binance`/`derivatives_collector__` |

## 11_KEY_DECISIONS

- Aucun reader créé pour `telegram_screener` ni `google_sheets` : `not_started` est l'état correct.
- Les paths sont déjà corrects depuis #751 — ce GO verrouille les invariants et documente.
- Les tests existants (`test_latest_only_consumers_read_from_view`) déjà présents — ce GO ajoute les assertions complémentaires (producer_id absent + not_started figé).

## 12_INVARIANTS

- Aucun appel Telegram, Sheets, API live.
- Aucun reader fantôme créé.
- Aucun path `latest_only` ne référence un `producer_id`.
- Tests existants non cassés.

## BUNDLE_TARGET — LATEST_CONSUMERS_VIEW_MIGRATION_V1

- [x] Inventaire complet des consumers `latest_only` (voir `10_LATEST_CONSUMERS_INVENTORY.md`)
- [x] Confirmation : tous les `read_path` pointent vers `views/market_metrics/latest.json`
- [x] Confirmation : aucun reader fantôme pour `telegram_screener` / `google_sheets`
- [x] `test_not_implemented_consumers_remain_not_started` ajouté
- [x] `test_latest_only_consumers_have_no_producer_id_in_path` ajouté
- [x] 121/121 PASS (119 existants + 2 nouveaux)
