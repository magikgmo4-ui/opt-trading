---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_TELEGRAM_SENDER_B_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_TELEGRAM_SENDER_B_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_TELEGRAM_SENDER_B_01

## Objectif

Implémenter option B — Telegram sender réel via caller séparé.

`send_vision_summary()` : lit `data/vision/coinglass/latest.json` via `load_and_format()`, envoie via `send_telegram_html()` (injectable). CLI `--send` flag pour déclencher après capture.

## Périmètre

- **IN** : `telegram_sender.py`, `--send` flag CLI, 8 tests
- **OUT** : activation prod sans staging PASS, adapter API Coinglass
- **Appel Telegram réel** : uniquement si `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` — jamais en tests

## Architecture

```
send_vision_summary(path, send_fn)
  load_and_format(path)         # telegram_summary.py
    → None si absent/mauvais input_class → return False
  send_fn(message)              # injecté — send_telegram_html() en prod
    → exception → return False
  → return True si envoyé
```

## CLI

```bash
VISION_BOT_ENABLED=true VISION_AI_PROVIDER=openai OPENAI_API_KEY=sk-... \
  python scripts/run_vision_capture.py --send
```

## Fichiers modifiés

| Fichier | Action |
|---|---|
| `modules/vision/coinglass/telegram_sender.py` | créé |
| `modules/vision/coinglass/tests/test_telegram_sender.py` | créé |
| `scripts/run_vision_capture.py` | `--send` flag + import telegram_sender |
