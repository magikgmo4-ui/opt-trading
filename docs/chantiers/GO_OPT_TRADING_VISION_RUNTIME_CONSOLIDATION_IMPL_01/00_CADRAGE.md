---
doc_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01_CADRAGE
doc_type: cadrage
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
  - runtime
  - consolidation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01/00_CADRAGE.md
point_de_reprise: "Consolider l'etat runtime VISION apres session closeout."
updated_at: 2026-05-13
links:
  - docs/chantiers/GO_OPT_TRADING_SESSION_CLOSEOUT_MULTI_CHAIN_01/90_CLOSEOUT.md
---

# 00_CADRAGE — VISION_RUNTIME_CONSOLIDATION_IMPL_01

## 1_MASTER_TARGET

Documenter l'etat final du cluster VISION, verifier l'integrite des wrappers et services, et preparer le terrain pour la stabilisation runtime.

## 2_ETAT EXISTANT CONSOLIDE

```text
Modules actifs :
  modules/vision_bot/         → intake capture, 13 scripts, systemd service
  modules/bot_vision_step2/   → analyse + Telegram, 7 scripts, systemd services + timers

Legacy preserve :
  modules/bot_vision/         → historique, non survivant

Wrapper unifie :
  cmd-vision, menu-vision, sanity-vision (PR #260)
  Shortcuts installes via install_shortcuts.sh

Systemd :
  vision_bot.service
  bot_vision_step2.service
  bot_vision_step2_send.service + timer
  bot_vision_step2_prune.service + timer

Health integration :
  modules/health/scripts/health-check → bot_vision check via vision_runtime_sanity.sh
```

## 3_NON MODIFIE

```text
- aucun service systemd
- aucun chemin shared_files
- aucun restart
- aucun deploy
```
