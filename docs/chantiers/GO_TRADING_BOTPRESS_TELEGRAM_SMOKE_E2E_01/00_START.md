---
doc_id: GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01_START
doc_type: chantier/start
repo: opt-trading
go_id: GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01
status: active
lifecycle_stage: e2e_smoke
updated_at: 2026-05-06
links:
  - docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_IMPL_01/90_CLOSEOUT.md
---

# 00_START — Telegram E2E Smoke

## Objet

Valider le flux E2E Telegram → Botpress → Adapter → response → Telegram, sans trade reel.

## Mode

Simulated Telegram webhook via Python (pas de bot Telegram reel). L adapter est teste avec des payloads identiques a ceux que Telegram enverrait.
