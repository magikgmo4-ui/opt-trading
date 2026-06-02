---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_WRITE_VALIDATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_WRITE_VALIDATION_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: closed
lifecycle_stage: implementation
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-25
updated_at: 2026-05-25
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
MASTER_PROJECT_PLAN_ID: MPP_DATA_CENTER_NORMALIZED_REGISTRY
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
BUNDLE_TARGET: PRODUCER_WRITE_VALIDATION_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: null
topic_keys:
  - opt-trading
  - data_center
  - runtime_registry
  - producers
  - last_write
  - evidence
links:
  - modules/data_center/runtime_registry.py
  - modules/data_center/registry/producers.json
  - modules/data_center/scripts/sanity_check.sh
  - modules/data_center/localcms_health_reader.py
  - modules/derivatives_collector/app/market_metrics_writer.py
  - modules/data_center/tests/test_runtime_registry.py
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_WRITE_VALIDATION_01

## Objet

Créer le runtime registry Data Center et valider les writes producers avec fixtures.

Après ce GO, `data/data_center/_registry/producers.json` (runtime) enregistre chaque
write producer avec `last_write`, `last_output_path`, `status`, `evidence`. Les fixtures
prouvent bitget et binance capables d'alimenter ce registry.

## Décision architecturale figée

```text
modules/data_center/registry/*.json
  = registry statique / contrats déclarés
  = ne jamais muter à chaque run

data/data_center/_registry/*.json
  = registry runtime / état vivant
  = last_write, last_output_path, status, evidence
  = écrit après chaque write producer réussi
```

## Règle live

```text
ALLOW_LIVE_PRODUCER_WRITE=1 requis pour tout appel API live.
Ce GO utilise uniquement des fixtures — aucun appel live.
```

## 6_FINAL_TARGET

- `modules/data_center/runtime_registry.py` — `update_producer_last_write()` + `load_runtime_registry()`
- `write_market_metrics_to_data_center()` branche le runtime registry après write réussi (`update_registry=True` par défaut)
- `read_data_center_health()` expose `producer_runtime` depuis le runtime registry
- `sanity_check.sh` affiche `producers with last_write`
- Tests : `test_runtime_registry.py` (11 tests) + `TestRuntimeRegistryIntegration` (6 tests) + 1 test localcms
- **180/180 PASS**

## 12_INVARIANTS

- Aucun appel API live.
- Le registry statique `modules/data_center/registry/producers.json` n'est pas muté par les writes runtime.
- `not_proven_runtime_adapter` ne met pas à jour le runtime registry.
- `update_registry=False` permet de désactiver l'enregistrement (tests).

## BUNDLE_TARGET — PRODUCER_WRITE_VALIDATION_V1

- [x] `modules/data_center/runtime_registry.py` — créé
- [x] `write_market_metrics_to_data_center()` — `update_registry=True` branché
- [x] `localcms_health_reader.py` — `producer_runtime` ajouté
- [x] `sanity_check.sh` — `producers with last_write` affiché
- [x] `test_runtime_registry.py` — 11 tests
- [x] `TestRuntimeRegistryIntegration` dans `test_market_metrics_writer.py` — 6 tests
- [x] `test_producer_runtime_is_list` dans `test_localcms_health_reader.py` — 1 test
- [x] **180/180 PASS** (162 existants + 18 nouveaux)
