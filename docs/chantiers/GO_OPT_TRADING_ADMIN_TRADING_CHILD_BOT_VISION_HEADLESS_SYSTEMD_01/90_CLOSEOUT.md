---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01_CLOSEOUT
doc_type: closeout
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: closed
verdict: PASS
lifecycle_stage: closeout
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 90_CLOSEOUT — Bot Vision Headless Systemd

## GO

GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01

## Verdict

**PASS**

## Resume

Automatisation systemd timer pour bot_vision_headless:
- Service oneshot + timer 10 min avec 30s jitter
- User ghost, pas de root
- Oneshot valide: 91 KB PNG + JSON, exit 0
- Timer enabled + active, next trigger dans ~9 min
- CRLF corrige sur les fichiers deployes

## Fichiers

### Source (5)
- modules/bot_vision/headless_capture/systemd/bot-vision-headless-capture.service
- modules/bot_vision/headless_capture/systemd/bot-vision-headless-capture.timer
- scripts/run_bot_vision_headless_capture.sh
- modules/bot_vision/headless_capture/scripts/install_systemd.sh
- modules/bot_vision/headless_capture/scripts/uninstall_systemd.sh

### Systeme (2)
- /etc/systemd/system/bot-vision-headless-capture.service
- /etc/systemd/system/bot-vision-headless-capture.timer

### Documentation (8 + inbox)

## Modifications runtime

| Action | Impact |
| --- | --- |
| systemctl start (oneshot) | 2 captures produites, traitees par vision_bot |
| systemctl enable --now timer | Timer actif, declenche toutes les 10 min |

## Next GO

GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01 (P1)
