---
doc_id: GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01_RUNTIME_SURFACE_MAP
doc_type: runtime_surface_map
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - vision
  - runtime
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/20_CALLERS_AUDIT.md
---

# 30_RUNTIME_SURFACE_MAP

## Carte cible observee aujourd'hui

```text
bot_vision/headless_capture
        │
        │ PNG + sidecar JSON vers vision_inbox
        ▼
vision_bot.service
        │
        ├── vision_outbox (.md/.txt)
        ├── vision_processed/
        └── rejet blocked/invalid_visual
                    │
                    ▼
bot_vision_step2.service
        │
        ├── analyze_latest
        ├── send_latest
        ├── prune_old
        ├── Telegram / callbacks
        └── Desk Pro artifacts
```

## Surfaces par role

| Role | Module | Preuves |
| --- | --- | --- |
| producteur headless | `modules/bot_vision/headless_capture/` | `capture_headless.js`, `bot-vision-headless-capture.service`, `scripts/run_bot_vision_headless_capture.sh` |
| consumer inbox/outbox | `modules/vision_bot/` | `app/vision_bot.py`, `vision_bot.service` |
| analyse Vision/Telegram | `modules/bot_vision_step2/` | `app/bot_vision_step2.py`, `bot_vision_step2.service` |
| wrapper operateur de paire | `modules/vision_bot/scripts/vision_runtime_cmd.sh` | `cmd-vision`, `menu-vision`, `sanity-vision` |

## Systemd reel

| Unite | Portee | Statut dans la famille |
| --- | --- | --- |
| `vision_bot.service` | watch loop inbox/outbox | runtime utile |
| `bot_vision_step2.service` | bot Telegram / analyse | runtime utile |
| `bot_vision_step2_send.timer` | diffusion periodique | runtime utile optionnel |
| `bot_vision_step2_prune.timer` | hygiene | runtime utile |
| `bot-vision-headless-capture.timer` | capture headless periodique | runtime utile mais loge sous module legacy |

## Wrappers reellement exposes

| Wrapper | Host | Sens |
| --- | --- | --- |
| `cmd-vision` | `modules/vision_bot/scripts/vision_runtime_cmd.sh` | wrapper unifie de paire |
| `menu-vision` | `modules/vision_bot/scripts/vision_runtime_menu.sh` | wrapper unifie de paire |
| `sanity-vision` | `modules/vision_bot/scripts/vision_runtime_sanity.sh` | sanity de paire |
| `cmd-vision_bot` | `modules/vision_bot/scripts/vision_bot_cmd.sh` | wrapper module capture |
| `cmd-bot_vision_step2` | `modules/bot_vision_step2/scripts/bot_vision_step2_cmd.sh` | wrapper module analyse |
| `cmd-bot_vision` | `modules/bot_vision/scripts/cmd.sh` | wrapper historique |

## Lecture structurante

La surface runtime utile n'est pas homologuee sur un seul dossier.

Elle est repartie entre :

- `vision_bot` pour l'entree et la discipline inbox/outbox
- `bot_vision_step2` pour l'analyse et la supervision fleet
- `bot_vision/headless_capture` pour la capture headless

Le vrai probleme de famille n'est donc pas un simple doublon nominal.
Le probleme est qu'un runtime encore utile reste heberge sous un module globalement legacy.
