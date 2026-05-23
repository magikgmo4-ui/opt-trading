---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_HEADLESS_RUNTIME_B1_01_INBOX
doc_type: inbox_entry
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_HEADLESS_RUNTIME_B1_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: accepted
created_at: 2026-05-23
---

# GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_HEADLESS_RUNTIME_B1_01

PATCH-B1 — Headless capture runtime gated (`VISION_BOT_ENABLED=true`).

`headless_capture.py` (gate + BrowserFn injectable) + `runner.py` (pipeline capture→parse→write). Writes isolés dans `data/vision/coinglass/` et `data/deskpro/inputs/vision_context/coinglass/`. 9 tests, 9 PASS.

Docs : `docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_HEADLESS_RUNTIME_B1_01/`
