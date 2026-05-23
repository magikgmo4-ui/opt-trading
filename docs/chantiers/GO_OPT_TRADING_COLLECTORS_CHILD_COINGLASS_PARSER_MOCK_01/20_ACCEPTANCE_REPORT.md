---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_PARSER_MOCK_01_ACCEPTANCE
doc_type: acceptance_report
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_PARSER_MOCK_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: accepted
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_ACCEPTANCE_REPORT

## Verdict : ACCEPTED

## Résultats tests

```
modules/vision/coinglass/tests/test_parser_mock.py — 7 passed in 0.09s
```

| Test ID | Cas | Résultat |
|---|---|---|
| TC-PARSER-01 | Mock extraction → 2+ détections retournées | PASS |
| TC-PARSER-02 | Confidence < 0.6 → null + warning | PASS |
| TC-PARSER-03 | Fichier absent → liste vide, pas d'exception | PASS |
| TC-PARSER-04 | Screenshot > 4h → `freshness_state = "stale"` | PASS |
| Extra-01 | Screenshot < 4h → `freshness_state = "fresh"` | PASS |
| Extra-02 | `extraction_fn` exception → dégradation silencieuse | PASS |
| Extra-03 | Extraction vide → liste vide sans erreur | PASS |

## Fichiers livrés

| Fichier | Rôle |
|---|---|
| `modules/vision/coinglass/parser.py` | Parser avec injection extraction_fn |
| `modules/vision/coinglass/tests/test_parser_mock.py` | 7 tests |
| `tests/fixtures/vision/coinglass/screenshot_mock_liquidations.png` | Image synthétique |
| `tests/fixtures/vision/coinglass/vision_coinglass_v1_valid.json` | Payload valide |
| `tests/fixtures/vision/coinglass/vision_coinglass_v1_low_conf.json` | Payload low confidence |
| `tests/fixtures/vision/coinglass/vision_coinglass_v1_null_vals.json` | Payload null values |

## Prochaine étape

PATCH-A3 : Desk Pro read-only consumer (`GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_DESKPRO_CONSUMER_01`)
