---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_ACCEPTANCE_01_BRANCH_STATE
doc_type: branch_state
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_ACCEPTANCE_01
status: active
created_at: 2026-05-23
updated_at: 2026-05-23
---

# BRANCH_STATE

## Branche courante

```
go/GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_ACCEPTANCE_01
base: sot/mainline
```

## Historique PRs vision Coinglass

| PR | Branche | Titre | État |
|---|---|---|---|
| #711 | go/GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01 | docs: Coinglass bot vision headless continuity GO | mergé |
| #712 | go/GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_VISION_CONTEXT_SCHEMA_01 | feat(vision): PATCH-A1 schema dataclass | mergé |
| #713 | go/GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_PARSER_MOCK_01 | feat(vision): PATCH-A2 fixtures + parser mock | mergé |
| #714 | go/GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_DESKPRO_CONSUMER_01 | feat(desk_pro): PATCH-A3 consumer read-only | mergé |
| #716 | go/GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_HEADLESS_RUNTIME_B1_01 | feat(vision): PATCH-B1 headless runtime gated | mergé |
| #717 | go/GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_TELEGRAM_SUMMARY_B2_01 | feat(vision): PATCH-B2 Telegram summary | mergé |

## Modules ajoutés sur sot/mainline

```
modules/vision/
  __init__.py
  coinglass/
    __init__.py
    vision_context_v1.py
    parser.py
    headless_capture.py
    runner.py
    telegram_summary.py
    tests/
      __init__.py
      test_vision_context_v1.py      (11 tests)
      test_parser_mock.py            (7 tests)
      test_headless_runner.py        (9 tests)
      test_telegram_summary.py       (12 tests)

modules/desk_pro/service/
  vision_context_reader.py

tests/
  test_desk_pro_vision_context_reader.py  (14 tests)
  fixtures/vision/coinglass/
    screenshot_mock_liquidations.png
    vision_coinglass_v1_valid.json
    vision_coinglass_v1_low_conf.json
    vision_coinglass_v1_null_vals.json
```
