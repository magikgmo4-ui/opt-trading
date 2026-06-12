---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01_RUNTIME_STATE
doc_type: runtime_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 10_HEADLESS_RUNTIME_STATE - Runtime State (read-only)

Observation le 2026-05-06 ~02:26 EDT. Aucun service modifié.

## bot-vision-headless-capture.timer

| Champ | Valeur |
| --- | --- |
| Unit file | `/etc/systemd/system/bot-vision-headless-capture.timer` |
| Active | `active (waiting)` |
| Depuis | 2026-05-04 17:28:49 EDT |
| Trigger | toutes les 10 min (`OnUnitActiveSec=10min`) |
| RandomizedDelaySec | 30s |
| Persistent | false |
| Triggers | `bot-vision-headless-capture.service` |

## bot-vision-headless-capture.service

| Champ | Valeur |
| --- | --- |
| Unit file | `/etc/systemd/system/bot-vision-headless-capture.service` |
| Type | oneshot |
| Enabled | disabled (timer-driven) |
| Active | `failed` (exit-code) |
| Dernier run | 2026-05-06 02:24:21 EDT |
| ExecStart | `/usr/bin/bash /opt/trading/scripts/run_bot_vision_headless_capture.sh` |
| User | ghost |
| TimeoutStartSec | 120 |
| Erreur | `MODULE_NOT_FOUND` — `capture_headless.js` ne peut pas charger `playwright` |

Le service échoue à chaque trigger car le module Node.js `playwright` n'est pas installé dans `modules/bot_vision/headless_capture/node_modules/`.

## vision_bot.service

| Champ | Valeur |
| --- | --- |
| Unit file | `/etc/systemd/system/vision_bot.service` |
| Type | long-running |
| Enabled | enabled |
| Active | `active (running)` depuis 2026-04-19 |
| PID | 798 |
| Commande | `python3 vision_bot.py watch` |
| Role | ShareX inbox → outbox watch loop (OCR) |

## bot_vision_step2.service

| Champ | Valeur |
| --- | --- |
| Unit file | `/etc/systemd/system/bot_vision_step2.service` |
| Type | long-running |
| Enabled | enabled |
| Active | `active (running)` depuis 2026-04-19 |
| PID | 1463 |
| Commande | `python bot_vision_step2.py serve` |
| Role | Telegram `/analyze` → Desk Pro artifacts |

Note: erreurs `URLError: timed out` observées dans les logs (réseau).

## desk_bridge.timer

| Champ | Valeur |
| --- | --- |
| Unit file | `/etc/systemd/system/desk_bridge.timer` |
| Active | `active (waiting)` depuis 2026-04-19 |
| Trigger | toutes les 10 min (`OnUnitActiveSec=10min`) |
| AccuracySec | 20s |
| Persistent | true |
| Triggers | `desk_bridge.service` |

## desk_bridge.service

| Champ | Valeur |
| --- | --- |
| Unit file | `/etc/systemd/system/desk_bridge.service` |
| Type | oneshot |
| Enabled | static |
| Active | `inactive (dead)` — dernier run 2026-05-06 02:25:35 EDT (SUCCESS) |
| ExecStart | `/opt/trading/scripts/desk_bridge/bridge_vision_to_desk_inbox.sh` |
| User | ghost |
| NoNewPrivileges | true |
| PrivateTmp | true |

## Synthèse état

| Composant | État | Blocking? |
| --- | --- | --- |
| headless-capture timer | active (waiting) | non |
| headless-capture service | failed — playwright manquant | oui pour headless |
| vision_bot | active (running) | non |
| bot_vision_step2 | active (running) | non |
| desk_bridge timer | active (waiting) | non |
| desk_bridge service | inactive (success last run) | non |

Le pipeline headless est **rompu** au niveau capture (playwright non installé), mais le fallback ShareX via `vision_bot` + `desk_bridge` fonctionne.

## RISKS

- À qualifier.
