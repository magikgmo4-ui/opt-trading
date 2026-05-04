---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01_EXISTING
doc_type: bot_vision_review
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 10_REVIEW_EXISTING_BOT_VISION

## Famille vision (3 modules)

### bot_vision (LEGACY)

| Propriete | Valeur |
| --- | --- |
| Dossier | modules/bot_vision/ |
| Sous-dossier | bot_vision_step1/desk_pro_vision/ |
| Role | Skeleton step1, generateur visuel placeholder |
| Code actif | NON (legacy) |
| Wrappers | cmd-bot_vision, menu-bot_vision, sanity-bot_vision |
| Statut | LEGACY, garde pour trajectoire historique |
| Impact headless | Aucun |

### vision_bot (ACTIF, capture/inbox-outbox)

| Propriete | Valeur |
| --- | --- |
| Dossier | modules/vision_bot/ |
| Service | vision_bot.service (active, since Apr 19) |
| PID | 798 |
| Processus | /usr/bin/python3 vision_bot.py watch |
| Memoire | 51.3M |
| CPU cumul | 17 min |
| Entree | vision_inbox/screen_*.png |
| Sortie | vision_processed/ + vision_outbox/ |
| Moteur | OCR (tesseract) ou dummy fallback |
| Wrappers | cmd-vision_bot, menu-vision_bot, sanity-vision_bot |
| Systemd | vision_bot.service (enabled) |
| Impact headless | Aucun (recoit les memes screen_*.png) |

### bot_vision_step2 (ACTIF, Telegram + OpenAI Vision)

| Propriete | Valeur |
| --- | --- |
| Dossier | modules/bot_vision_step2/ |
| Service | bot_vision_step2.service (active, since Apr 19) |
| PID | 1463 |
| Processus | /opt/trading/.venvs/bot_vision_step2/bin/python bot_vision_step2.py serve |
| Memoire | 17.3M |
| CPU cumul | 10 min |
| Role | Telegram /analyze -> OpenAI Vision -> Desk Pro artifacts |
| Config | config/bot_vision.env |
| Venv | .venvs/bot_vision_step2/ |
| Wrappers | cmd-bot_vision_step2, menu, sanity |
| Timers | send (disabled), prune (enabled) |
| Impact headless | Aucun |
| Erreur recente | ssl read timeout (mai 4 14:48) — non bloquant |

## Etat des services

| Service | Statut | Memory | Notes |
| --- | --- | --- | --- |
| vision_bot | active | 51.3M | Watch loop, pret pour input |
| bot_vision_step2 | active | 17.3M | Telegram bot, pret |
| desk_bridge.timer | active | - | Every 10 min, echec propre si inbox vide |

## Wrappers installes

| Wrapper | Module |
| --- | --- |
| cmd-vision_bot, menu-vision_bot, sanity-vision_bot | vision_bot |
| cmd-bot_vision, menu-bot_vision, sanity-bot_vision | bot_vision (legacy) |
| cmd-bot_vision_step2, menu-bot_vision_step2, sanity-bot_vision_step2 | bot_vision_step2 |
| cmd-desk_bridge | Aucun (systemd only) |

## Constats

- Les 2 services actifs (vision_bot, bot_vision_step2) sont stables
- Consommation memoire acceptable (68.6M total)
- Aucune modification necessaire pour accepter capture headless
- Le contrat d'entree (vision_inbox/screen_*.png) est deja standardise
