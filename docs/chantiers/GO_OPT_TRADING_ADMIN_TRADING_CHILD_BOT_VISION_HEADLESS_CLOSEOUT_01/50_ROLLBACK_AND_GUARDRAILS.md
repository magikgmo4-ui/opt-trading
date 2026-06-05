---
doc_id: HEADLESS_CLOSEOUT_01_ROLLBACK
doc_type: rollback_guardrails
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_CLOSEOUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 50_ROLLBACK_AND_GUARDRAILS

## Desactiver le timer headless

```bash
sudo systemctl disable --now bot-vision-headless-capture.timer
# ShareX reste fallback
```

## Reactiver si necessaire

```bash
sudo systemctl enable --now bot-vision-headless-capture.timer
```

## Rollback complet (desinstaller)

```bash
bash /opt/trading/modules/bot_vision/headless_capture/scripts/uninstall_systemd.sh
```

## Garde-fous actifs

| Garde | Ou | Effet |
| --- | --- | --- |
| Atomic write | capture_headless.js | .uploading -> rename, jamais 0-byte final |
| pick_latest() skip | bridge_vision_to_desk_inbox.sh | Ignore .uploading + 0-byte |
| main() verify | bridge script | Double-check avant crop |
| crop_with_python() guard | bridge script | sys.exit(0) si input invalide |
| Stale cleanup | capture_headless.js | .uploading > 5 min supprimes |

## macro-xau

- macro-xau.timer: disabled + inactive
- Ne pas reactiver (module obsolète)
- Ne pas restaurer jobs/macro_xau/run.sh

## ShareX fallback

- ShareX sur Windows peut toujours envoyer vers vision_inbox via SFTP
- Le nommage (screen_YYYY-MM-DD_HH-mm-ss_RANDOM.png) est compatible
- vision_bot traite toutes les sources de maniere transparente

## RISKS

- À qualifier.
