---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01_START
doc_type: start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01
parent_go: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
previous_go: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 00_START - Bot Vision Headless Pipeline Review

## GO ID

`GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01`

## Parent GO

`GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01`

## Previous GO

`GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01` — verdict `PASS` @ `20c7026`

## Base branch

```
origin/go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01 @ 20c7026
```

## Objectif

Auditer le pipeline Bot Vision Headless comme producer de `visual_context`, compatible avec :
- `signal_event` V1 produit par WEBHOOK_SIGNAL_DIAG
- `desk_snapshot` produit/adapté par `desk_bridge`
- Desk Pro comme futur consumer final

## Invariants

- Ne pas modifier runtime
- Ne pas start/stop/restart/reload service
- Ne pas déclencher capture active si elle a un side effect non documenté
- Ne pas envoyer Telegram
- Ne pas lire ni afficher `.env`
- Ne pas committer `journal.md`
- Ne pas restaurer automatiquement `/tmp/opt-trading-quarantine/headless_capture_20260505_171247/`
- Ne pas committer `modules/bot_vision/headless_capture/` si le répertoire réapparaît non suivi
- Ne pas mélanger cursor-ai, db-layer, student ou fantome
- Diagnostic documentaire/read-only seulement

## Runtime side effects attendus

`NONE`
