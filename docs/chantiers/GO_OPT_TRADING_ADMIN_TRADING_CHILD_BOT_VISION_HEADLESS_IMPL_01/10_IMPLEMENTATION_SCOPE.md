---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01_SCOPE
doc_type: implementation_scope
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 10_IMPLEMENTATION_SCOPE

## Implemente

| Composant | Details |
| --- | --- |
| Module | modules/bot_vision/headless_capture/ |
| Script | capture_headless.js (Node.js + Playwright + Chromium) |
| Config | profiles.example.json (URLs de capture) |
| Package | package.json (npm dependencies) |
| Documentation | README.md |

## Pipeline

```
capture_headless.js
  -> atomic write (PNG + JSON sidecar)
  -> vision_inbox/screen_*.png + .json
  -> vision_bot (watch loop detecte)
  -> OCR -> vision_processed + vision_outbox
  -> desk_bridge (timer 10 min)
  -> crop 2x2 -> inbox
  -> Desk Pro
```

## Non implemente

- Systemd timer (prochain GO)
- Wrappers globaux (prochain GO)
- Multi-profile scheduling
- Error retry logic (deja basics dans le script)
- Notification Telegram (deja dans bot_vision_step2)

## ShareX conserve

ShareX reste fallback. Les deux sources peuvent coexister:
- Nommage unique avec timestamp
- vision_bot traite sequentiellement
- Aucun conflit de fichiers

## desk_bridge et Desk Pro inchanges

Le contrat d'entree (vision_inbox/screen_*.png) est identique.
Aucune modification necessaire des modules downstream.
