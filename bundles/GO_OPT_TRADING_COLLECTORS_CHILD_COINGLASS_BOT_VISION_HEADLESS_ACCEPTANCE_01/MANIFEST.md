---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_ACCEPTANCE_01_MANIFEST
doc_type: bundle_manifest
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_ACCEPTANCE_01
created_at: 2026-05-23
---

# Bundle — GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_ACCEPTANCE_01

## Contenu

```
docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_ACCEPTANCE_01/
  00_INITIAL_PROJECT_DOC.md
  20_ACCEPTANCE_REPORT.md
  90_REPRISE_POINT.md
  BRANCH_STATE.md

docs/index/inbox/
  GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_ACCEPTANCE_01.md
```

## Modules livrés (sur sot/mainline après #712–#717)

```
modules/vision/coinglass/
  vision_context_v1.py   — contrat Python vision_context.coinglass.v1
  parser.py              — parse_screenshot() avec ExtractionFn injectable
  headless_capture.py    — capture_screenshot() gated VISION_BOT_ENABLED
  runner.py              — run_capture() pipeline complet
  telegram_summary.py    — format_vision_summary() + load_and_format()

modules/desk_pro/service/
  vision_context_reader.py  — read_vision_context_coinglass() consumer Desk Pro

tests/fixtures/vision/coinglass/
  screenshot_mock_liquidations.png
  vision_coinglass_v1_valid.json
  vision_coinglass_v1_low_conf.json
  vision_coinglass_v1_null_vals.json
```

## PRs mergées

#712 #713 #714 #716 #717 → sot/mainline

## Tests

53 PASS (A1:11 + A2:7 + A3:14 + B1:9 + B2:12)
