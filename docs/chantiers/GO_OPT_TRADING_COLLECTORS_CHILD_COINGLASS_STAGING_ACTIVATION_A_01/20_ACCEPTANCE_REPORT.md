---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_STAGING_ACTIVATION_A_01_ACCEPTANCE
doc_type: acceptance_report
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_STAGING_ACTIVATION_A_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: accepted
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_ACCEPTANCE_REPORT

## Verdict : ACCEPTED

## Résultats tests

```
modules/vision/coinglass/tests/test_staging_validator.py — 10 passed in 0.06s
```

| Test ID | Cas | Résultat |
|---|---|---|
| TC-STAGING-01 | 3 runs PASS → ok=True | PASS |
| TC-STAGING-02 | 1 run FAIL sur 3 → ok=False | PASS |
| TC-STAGING-03 | Fichier absent → ok=False | PASS |
| TC-STAGING-04 | Fichier vide → ok=False + "empty" | PASS |
| TC-STAGING-05 | < N runs → INSUFFICIENT | PASS |
| TC-STAGING-06 | confidence < 0.60 → FAIL | PASS |
| TC-STAGING-07 | extracted_value null → FAIL | PASS |
| TC-STAGING-08 | Seuls les N derniers runs évalués | PASS |
| TC-STAGING-09 | Ligne JSON malformée → FAIL | PASS |
| TC-STAGING-10 | required=1 + 1 bon run → ok=True | PASS |

## Fichiers livrés

| Fichier | Rôle |
|---|---|
| `modules/vision/coinglass/playwright_capture.py` | BrowserFn Playwright injectable |
| `modules/vision/coinglass/staging_validator.py` | Validation N runs consécutifs |
| `modules/vision/coinglass/tests/test_staging_validator.py` | 10 tests |
| `scripts/run_vision_capture.py` | CLI capture + --validate |

## Note stub extraction

L'`extraction_fn` dans le CLI est un stub — retourne 0 détections, loggue un warning.
Les runs staging avec le stub seront FAIL au validator.
La gate prod (3 runs PASS) ne pourra être franchie qu'après wiring d'une extraction_fn réelle (OCR/AI).

## Prochaine étape

Option B (Telegram sender) ou wiring extraction_fn réelle.
