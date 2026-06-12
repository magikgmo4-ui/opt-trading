---
doc_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01_EXISTING_STATE
doc_type: existing_state
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01
status: final
lifecycle_stage: closeout
parent_go_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01
topic_keys:
  - opt-trading
  - vision
  - existing-state
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01/01_EXISTING_STATE.md
point_de_reprise: "Etat complet du cluster VISION."
updated_at: 2026-05-13
links:
  - docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01/00_CADRAGE.md
---

# 01_EXISTING_STATE

## 1_MODULES

### vision_bot (modules/vision_bot/)

```text
Role : capture intake / inbox-outbox processor
Scripts : 13 (vision_bot_*, vision_runtime_*, cmd, menu, sanity, install/uninstall service)
Systemd : vision_bot.service
Shared paths : /srv/sftp/shared_files/shared/vision_{inbox,outbox,processed}
```

### bot_vision_step2 (modules/bot_vision_step2/)

```text
Role : analyse Vision + Telegram + Desk Pro outputs
Scripts : 7 (bot_vision_step2_*, install/uninstall service, sharex watchdog)
Systemd : bot_vision_step2.service, send.service+timer, prune.service+timer
Config  : bot_vision.env
```

### bot_vision (modules/bot_vision/) — LEGACY

```text
Role : verticale historique, non survivant
Contient : step1 skeleton, headless_capture optionnel
```

## 2_WRAPPER UNIFIE (PR #260)

```text
Shortcuts installes :
  cmd-vision     → vision_runtime_cmd.sh
  menu-vision    → vision_runtime_menu.sh
  sanity-vision  → vision_runtime_sanity.sh

Conserves :
  cmd-vision_bot, sanity-vision_bot, menu-vision_bot
  cmd-bot_vision_step2, menu-bot_vision_step2, sanity-bot_vision_step2
```

## 3_SYSTEMD

```text
vision_bot.service                         → watch loop capture
bot_vision_step2.service                   → Telegram bot
bot_vision_step2_send.service + .timer     → envoi periodique
bot_vision_step2_prune.service + .timer    → nettoyage
```

## 4_HEALTH INTEGRATION

```text
modules/health/scripts/health-check :
  bot_vision → bash modules/vision_bot/scripts/vision_runtime_sanity.sh
```

## 5_DEPENDANCES

```text
- sftp/inbox partage
- OpenAI API (analyse)
- Telegram token (notifications)
- systemd (services + timers)
```

## RISKS

- À qualifier.
