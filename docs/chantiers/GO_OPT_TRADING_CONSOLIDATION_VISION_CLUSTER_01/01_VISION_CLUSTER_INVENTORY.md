---
doc_id: GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01_INVENTORY
doc_type: cluster_inventory
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_inventory
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - consolidation
  - vision
  - inventory
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01/01_VISION_CLUSTER_INVENTORY.md
point_de_reprise: "Inventaire des surfaces vision_bot, bot_vision_step2 et bot_vision."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01/00_CADRAGE.md
---

# 01_VISION_CLUSTER_INVENTORY

## 1_VISION_BOT — modules/vision_bot/

```text
Role : intake capture / inbox-outbox processor
Fonctions :
  - recoit les screenshots dans vision_inbox
  - traite via OCR / dummy / custom shell engine
  - ecrit .md / .txt dans vision_outbox
  - deplace les inputs vers vision_processed
  - expose une watch loop + service systemd

Structure visible :
  - app/vision_bot.py
  - scripts/vision_bot_* + aliases legacy cmd/menu/sanity
  - systemd/vision_bot.service
  - README.md, SHAREX_SETUP.md
```

## 2_BOT_VISION_STEP2 — modules/bot_vision_step2/

```text
Role : analyse enrichie + Telegram + artefacts Desk Pro
Fonctions :
  - trouve la derniere capture
  - resize/crop dashboard
  - appelle OpenAI Vision
  - ecrit analysis.txt, analysis.md, summary.json, vision.log.jsonl
  - miroir vers vision_outbox
  - expose Telegram /analyze, send timer, prune timer

Structure visible :
  - app/bot_vision_step2.py
  - scripts/bot_vision_step2_* + sharex_capture_watchdog.ps1
  - systemd/*.service *.timer
  - README.md, DESKPRO_OUTPUTS.md, SHAREX_WATCHDOG.md
```

## 3_BOT_VISION — modules/bot_vision/

```text
Role : verticale vision historique
Sous-blocs :
  - bot_vision_step1/       → squelette de generation visuelle Desk Pro
  - headless_capture/       → Playwright screenshot producer vers vision_inbox

Signaux legacy :
  - README le qualifie explicitement d'historique
  - step1 reste placeholder / ancien lineage
  - headless_capture reste compatible avec vision_bot, mais non survivant
```

## 4_FLUX REEL

```text
headless_capture ou ShareX
          │
          ▼
vision_inbox/shared_files
          │
          ▼
vision_bot
          │
          ├── vision_outbox
          └── vision_processed
                    │
                    ▼
             bot_vision_step2
                    │
                    ├── artefacts Desk Pro
                    ├── summary.json
                    ├── Telegram send / analyze
                    └── watchdog / prune
```

## 5_MATRICE DE ROLE

| Surface | Role reel | Statut |
|---|---|---|
| `modules/vision_bot/` | entree capture operationnelle | CANONIQUE_PAIR |
| `modules/bot_vision_step2/` | cerveau/analyse operationnelle | CANONIQUE_PAIR |
| `modules/bot_vision/` | famille historique | LEGACY |
| `modules/bot_vision/headless_capture/` | source de capture compatible | COMPAT |
| `modules/bot_vision/bot_vision_step1/` | ancien squelette | LEGACY_STEP1 |

## 6_RESUME

```text
La famille VISION n'a pas un survivant unique ; elle a une paire survivante.
Survivants operationnels : vision_bot + bot_vision_step2.
bot_vision reste contexte historique et compatibilite.
```
