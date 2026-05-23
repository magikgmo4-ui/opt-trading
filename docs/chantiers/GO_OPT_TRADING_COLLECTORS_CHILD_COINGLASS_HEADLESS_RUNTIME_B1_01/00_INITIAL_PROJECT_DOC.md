---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_HEADLESS_RUNTIME_B1_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_HEADLESS_RUNTIME_B1_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_HEADLESS_RUNTIME_B1_01

## Objectif

Implémenter PATCH-B1 : orchestrateur headless capture runtime pour `vision_context.coinglass.v1`.

Gated par env var `VISION_BOT_ENABLED=true`. BrowserFn injectable — Playwright wired en staging, mock en tests.

## Périmètre

- **IN** : `headless_capture.py`, `runner.py`, 9 tests
- **OUT** : Playwright réel, activation prod (gate staging requis)
- **Writes autorisés** : `data/vision/coinglass/{raw/,normalized/,latest.json,events.jsonl}` et `data/deskpro/inputs/vision_context/coinglass/latest.json` uniquement

## Architecture

```
run_capture(browser_fn, extraction_fn) →
  capture_screenshot()  [gate VISION_BOT_ENABLED]
  parse_screenshot()
  VisionContextCoinglassV1.validate()
  write: normalized/, latest.json, events.jsonl, deskpro input
```

## Gate staging

Ne PAS activer en production sans 3 runs consécutifs PASS en staging.
Env var : `VISION_BOT_ENABLED=true`

## Fichiers modifiés

| Fichier | Action |
|---|---|
| `modules/vision/coinglass/headless_capture.py` | créé |
| `modules/vision/coinglass/runner.py` | créé |
| `modules/vision/coinglass/tests/test_headless_runner.py` | créé |
