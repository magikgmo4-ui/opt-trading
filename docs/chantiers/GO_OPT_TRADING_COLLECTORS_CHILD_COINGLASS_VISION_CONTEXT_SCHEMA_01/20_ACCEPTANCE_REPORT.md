---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_VISION_CONTEXT_SCHEMA_01_ACCEPTANCE
doc_type: acceptance_report
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_VISION_CONTEXT_SCHEMA_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: accepted
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_ACCEPTANCE_REPORT

## Verdict : ACCEPTED

## Résultats tests

```
modules/vision/coinglass/tests/test_vision_context_v1.py — 11 passed
```

| Test ID | Cas | Résultat |
|---|---|---|
| TC-SCHEMA-01 | Payload minimal valide | PASS |
| TC-SCHEMA-02 | `extracted_value = null` autorisé | PASS |
| TC-SCHEMA-03 | `confidence < 0.5` sans warning → ValueError | PASS |
| TC-SCHEMA-03+ | `confidence < 0.5` avec warning → OK | PASS |
| TC-SCHEMA-04 | `input_class` incorrect → ValueError | PASS |
| TC-SCHEMA-04b | `contract_version` incorrect → ValueError | PASS |
| TC-SCHEMA-05 | `extracted_value` non-null + `confidence=0` → ValueError | PASS |
| TC-SCHEMA-05+ | `null` + `confidence=0` → OK | PASS |
| TC-SCHEMA-06 | JSON roundtrip | PASS |
| Extra-01 | Multiples detections valides | PASS |
| Extra-02 | `to_dict()` structure | PASS |

## Fichiers livrés

| Fichier | Lignes | Rôle |
|---|---|---|
| `modules/vision/coinglass/vision_context_v1.py` | 63 | Dataclasses + validate() + to_json() |
| `modules/vision/coinglass/tests/test_vision_context_v1.py` | 115 | 11 tests |

## Prochaine étape

PATCH-A2 : fixtures + parser mock (`GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_PARSER_MOCK_01`)
