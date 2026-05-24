---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PAIR_SNAPSHOT_VIEW_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PAIR_SNAPSHOT_VIEW_01
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
BUNDLE_TARGET: PAIR_SNAPSHOT_VIEW_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: null
topic_keys:
  - opt-trading
  - data_center
  - pair_market_snapshot
  - consumers
  - view
  - collector_binance_spot
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01/30_REMAINING_GAPS_AND_NEXT_GO.md
  - modules/data_center/registry/consumers.json
  - modules/data_center/registry/producers.json
  - modules/data_center/layout.py
  - modules/data_center/pair_snapshot_view_writer.py
  - modules/data_center/tests/test_contract_tests.py
  - modules/collector_binance_spot/src/collector_binance_spot/normalize.py
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_PAIR_SNAPSHOT_VIEW_01

## Objet

Étendre la règle `producer <> view <> consumer` au contrat `pair_market_snapshot.v1`.

Corriger `desk_pro__spot_snapshot` — seul consumer `pair_market_snapshot.v1` dont le `read_path` pointait vers le path producteur `data/data_center/spot/collector_binance_spot/latest.json`.

## Décision figée

```text
pair_market_snapshot.v1 suit la même règle que market_metrics.v1 :
producer path = écriture/audit  (data/data_center/spot/<producer_id>/)
contract-class view = lecture consumer  (data/data_center/views/pair_market_snapshot/)
consumer non implémenté = not_started
PF_DATA_CENTER reste OPEN
```

## 6_FINAL_TARGET

- `desk_pro__spot_snapshot` : `read_path` → `views/pair_market_snapshot/latest.json`.
- `write_pair_market_snapshot_view()` : nouvelle fonction dans `modules/data_center/pair_snapshot_view_writer.py`.
- `layout.py` : crée `views/pair_market_snapshot/by_symbol/`.
- Tests invariants `pair_market_snapshot.v1` ajoutés et verrouillés.

## 7_CANONICAL_STATE — après livraison

### Consumer `pair_market_snapshot.v1`

| Consumer | read_path | Status | Reader réel |
|---|---|---|---|
| `desk_pro__spot_snapshot` | `views/pair_market_snapshot/latest.json` | not_started | Non |

### Payload structure `pair_market_snapshot.v1`

Le payload normalisé (produit par `normalize_pair_market_snapshot`) contient un champ `records: [...]` — batch multi-symboles.

- `views/pair_market_snapshot/latest.json` = payload complet (tous symboles)
- `views/pair_market_snapshot/by_symbol/<SYM>.json` = document par symbole (métadonnées + record)

## 11_KEY_DECISIONS

- Writer placé dans `modules/data_center/pair_snapshot_view_writer.py` (pas dans le package `collector_binance_spot` qui utilise un layout `src/`) pour rester importable depuis les contract tests.
- Pas de concept `not_proven_runtime_adapter` pour ce contrat — `binance_spot` est une API publique éprouvée.
- `desk_pro__spot_snapshot` : aucun reader dans le repo → `not_started` correct, aucun reader fantôme créé.

## 12_INVARIANTS

- Aucun appel API live.
- Aucun reader fantôme créé.
- PF_DATA_CENTER non fermé.
- Aucun path `pair_market_snapshot.v1` ne référence un `producer_id`.

## BUNDLE_TARGET — PAIR_SNAPSHOT_VIEW_V1

- [x] `read_path` `desk_pro__spot_snapshot` corrigé : `views/pair_market_snapshot/latest.json`
- [x] `write_pair_market_snapshot_view()` créée dans `modules/data_center/pair_snapshot_view_writer.py`
- [x] `layout.py` crée `views/pair_market_snapshot/by_symbol/`
- [x] Tests invariants dans `test_contract_tests.py`
- [x] Suite dédiée dans `test_pair_snapshot_view_writer.py`
- [x] 150/150 PASS (135 existants + 15 nouveaux)
