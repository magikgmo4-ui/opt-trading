---
doc_id: GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01_FAMILY_INVENTORY
doc_type: family_inventory
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - vision
  - inventory
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/00_INITIAL_PROJECT_DOC.md
---

# 10_FAMILY_INVENTORY

## Vue d'ensemble

| Module | Surface visible | Role constate | Statut retenu |
| --- | --- | --- | --- |
| `modules/vision_bot/` | `app/`, `scripts/`, `systemd/`, `README.md`, `SHAREX_SETUP.md` | consumer inbox/outbox, watch loop, wrapper host | survivant documentaire + composant operatoire |
| `modules/bot_vision_step2/` | `app/`, `config/`, `scripts/`, `systemd/`, docs module | analyse Vision, Telegram, artefacts Desk Pro, timers | composant operatoire complementaire |
| `modules/bot_vision/` | `bot_vision_step1/`, `headless_capture/`, `scripts/`, `README.md` | racine historique ; `step1` legacy ; `headless_capture` producteur headless | legacy preserve avec runtime residuel embarque |

## Detail par module

### `vision_bot`

- point d'entree Python: `modules/vision_bot/app/vision_bot.py`
- fonctions reelles:
  - lit `vision_inbox`
  - filtre les sidecars `blocked` et `invalid_visual`
  - genere sorties `.md` / `.txt` vers `vision_outbox`
  - deplace les captures vers `vision_processed`
  - expose `run_once` et `watch`
- surface runtime:
  - `modules/vision_bot/systemd/vision_bot.service`
  - wrappers legacy `cmd-vision_bot`, `menu-vision_bot`, `sanity-vision_bot`
  - wrappers unifies `cmd-vision`, `menu-vision`, `sanity-vision`

### `bot_vision_step2`

- point d'entree Python: `modules/bot_vision_step2/app/bot_vision_step2.py`
- fonctions reelles:
  - recupere la derniere capture `inbox` ou `processed`
  - resize/crop le dashboard
  - appelle OpenAI Vision
  - produit `summary.json`, `analysis.txt`, `analysis.md`, `vision.log.jsonl`
  - sert le bot Telegram et les callbacks `sendall:*`
  - gere `send_latest` et `prune_old`
- surface runtime:
  - `bot_vision_step2.service`
  - `bot_vision_step2_send.service` + `.timer`
  - `bot_vision_step2_prune.service` + `.timer`
  - venv dedie: `/opt/trading/.venvs/bot_vision_step2`

### `bot_vision`

- role de racine historique confirme par `modules/bot_vision/README.md`
- sous-surfaces distinctes:
  - `bot_vision_step1/`: squelette placeholder historique pour Desk Pro
  - `headless_capture/`: capture Playwright vers `vision_inbox`, avec service/timer propres
  - `scripts/`: anciens wrappers `cmd/menu/sanity`
- point cle:
  - le dossier racine est legacy
  - mais il contient encore `headless_capture`, qui porte un runtime actif de production headless

## Nature de la famille

La famille n'est pas une simple lignee `step1 -> step2 -> final`.

Elle combine :

- une lignee historique: `bot_vision` -> `bot_vision_step2`
- un renommage fonctionnel: `vision_bot`
- une stack complementaire actuelle:
  - producteur headless: `modules/bot_vision/headless_capture/`
  - consumer inbox/outbox: `modules/vision_bot/`
  - analyse Telegram/Desk Pro: `modules/bot_vision_step2/`

## Inventaire decisionnel

- `vision_bot` n'est pas un simple alias de `bot_vision_step2`
- `bot_vision_step2` n'est pas un remplaçant complet de `vision_bot`
- `bot_vision` ne peut pas etre considere comme survivant global, mais ne peut pas non plus etre classe archive simple tant que `headless_capture` reste dedans
