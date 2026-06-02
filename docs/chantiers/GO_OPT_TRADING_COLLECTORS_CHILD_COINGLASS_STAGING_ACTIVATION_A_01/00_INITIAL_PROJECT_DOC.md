---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_STAGING_ACTIVATION_A_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_STAGING_ACTIVATION_A_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: closed
created_at: 2026-05-23
updated_at: 2026-05-23
---

# GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_STAGING_ACTIVATION_A_01

## Objectif

Wirer le runtime headless Coinglass pour activation staging (option A du reprise point).

Livrer :
1. `playwright_capture.py` — BrowserFn Playwright avec graceful ImportError
2. `staging_validator.py` — vérification N runs consécutifs PASS depuis `events.jsonl`
3. `scripts/run_vision_capture.py` — CLI entry point (capture + --validate)

## Périmètre

- **IN** : playwright_capture, staging_validator, CLI script, 10 tests
- **OUT** : activation prod (gate staging 3 runs PASS requis)
- **OUT** : OCR/AI extraction réelle (stub → retourne 0 détections, à wirer séparément)
- **OUT** : send Telegram réel

## Architecture

```
VISION_BOT_ENABLED=true python scripts/run_vision_capture.py
  → make_playwright_browser_fn()
  → run_capture(browser_fn, _stub_extraction_fn)
  → writes data/vision/coinglass/{raw/, normalized/, latest.json, events.jsonl}

VISION_BOT_ENABLED=true python scripts/run_vision_capture.py --validate
  → validate_staging_runs(events.jsonl, required=3)
  → exit 0 si PASS, exit 1 si FAIL/INSUFFICIENT
```

## Gate staging

3 runs consécutifs PASS dans `events.jsonl` avant activation prod.
PASS = ≥1 détection avec `confidence ≥ 0.60` ET `extracted_value` non-null.
(Avec stub extraction, runs seront FAIL jusqu'au wiring OCR réel.)

## Fichiers modifiés

| Fichier | Action |
|---|---|
| `modules/vision/coinglass/playwright_capture.py` | créé |
| `modules/vision/coinglass/staging_validator.py` | créé |
| `modules/vision/coinglass/tests/test_staging_validator.py` | créé |
| `scripts/run_vision_capture.py` | créé |
