---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01_ROLLBACK
doc_type: rollback_guide
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 50_ROLLBACK

## Desactiver le timer

```bash
sudo systemctl disable --now bot-vision-headless-capture.timer
sudo systemctl stop bot-vision-headless-capture.service 2>/dev/null || true
```

## Retirer les unites

```bash
sudo rm -f /etc/systemd/system/bot-vision-headless-capture.service
sudo rm -f /etc/systemd/system/bot-vision-headless-capture.timer
sudo systemctl daemon-reload
```

## Ou utiliser le script

```bash
bash /opt/trading/modules/bot_vision/headless_capture/scripts/uninstall_systemd.sh
```

## Etat apres rollback

- Aucune capture automatique
- vision_inbox ne recoit plus de fichiers du headless
- vision_bot continue de tourner (pret pour input)
- desk_bridge continue de tourner (clean fail si inbox vide)
- ShareX reste disponible comme fallback
- Module headless toujours present (capture manuelle toujours possible)

## Aucun impact sur les autres services

Rollback n'affecte pas:
- tv-webhook, tv-perf, vision_bot, bot_vision_step2, ngrok-tv
- desk_bridge, Desk Pro
- macro-xau (deja disabled)
- OpenClaw

## RISKS

- À qualifier.
