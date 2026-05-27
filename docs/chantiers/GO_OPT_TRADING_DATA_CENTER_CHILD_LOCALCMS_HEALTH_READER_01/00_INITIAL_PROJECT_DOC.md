---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_LOCALCMS_HEALTH_READER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_LOCALCMS_HEALTH_READER_01
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
BUNDLE_TARGET: LOCALCMS_HEALTH_READER_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: null
topic_keys:
  - opt-trading
  - data_center
  - localcms
  - consumers
  - health
links:
  - modules/data_center/localcms_health_reader.py
  - modules/data_center/registry/consumers.json
  - modules/localcms/app/main.py
  - modules/data_center/tests/test_localcms_health_reader.py
  - modules/data_center/tests/test_contract_tests.py
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_LOCALCMS_HEALTH_READER_01

## Objet

Implémenter `localcms__data_center_health` comme second consumer runtime réel de PF_DATA_CENTER.

LocalCMS lit une surface registry/status Data Center neutre et expose `GET /data-center/health`.
Data Center atteint ainsi ≥2 consumers implemented : Desk Pro + LocalCMS.

## Décision figée

```text
localcms__data_center_health est un consumer runtime réel.
access_pattern = status_only : lecture registry uniquement (pas de data/ files).
read_path = data/data_center/_registry/producers.json (symbolique — lecture via loader Python).
implementation_status = implemented.
PF_DATA_CENTER reste OPEN.
```

## 6_FINAL_TARGET

- `read_data_center_health()` dans `modules/data_center/localcms_health_reader.py`.
- `GET /data-center/health` dans `modules/localcms/app/main.py`.
- `consumers.json` : `localcms__data_center_health.implementation_status = implemented`.
- Tests : `test_localcms_health_reader.py` (10 tests) + 2 tests dans `test_contract_tests.py`.
- `sanity_check.sh` vérifie `len(implemented) >= 2`.

## 7_CANONICAL_STATE — après livraison

| Consumer | implementation_status | Endpoint |
|---|---|---|
| `desk_pro__market_metrics` | implemented | (Desk Pro reader) |
| `localcms__data_center_health` | implemented | `GET /data-center/health` |

## 12_INVARIANTS

- Aucun appel API live.
- Aucun reader fantôme créé.
- PF_DATA_CENTER non fermé.
- `localcms__data_center_health` lit uniquement le registry Python (load_producers_registry / load_consumers_registry).

## BUNDLE_TARGET — LOCALCMS_HEALTH_READER_V1

- [x] `read_data_center_health()` créée dans `modules/data_center/localcms_health_reader.py`
- [x] `GET /data-center/health` ajouté à `modules/localcms/app/main.py`
- [x] `consumers.json` : `localcms__data_center_health` → `implemented`
- [x] `test_localcms_health_reader.py` — 10 tests
- [x] `test_contract_tests.py` — +2 tests (localcms implemented + ≥2 gate)
- [x] `sanity_check.sh` — assert ≥2 implemented
- [x] 162/162 PASS (150 existants + 12 nouveaux)
