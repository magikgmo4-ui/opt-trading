---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01_FILES
doc_type: service_timer_doc
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 20_SERVICE_AND_TIMER

## Fichiers crees

### Repo (versionnes)

| Fichier | Role |
| --- | --- |
| modules/bot_vision/headless_capture/systemd/bot-vision-headless-capture.service | Service oneshot |
| modules/bot_vision/headless_capture/systemd/bot-vision-headless-capture.timer | Timer 10 min |
| scripts/run_bot_vision_headless_capture.sh | Wrapper shell |
| modules/bot_vision/headless_capture/scripts/install_systemd.sh | Script d'installation |
| modules/bot_vision/headless_capture/scripts/uninstall_systemd.sh | Script de rollback |

### Systeme (installes sur admin-trading)

| Fichier | Emplacement |
| --- | --- |
| bot-vision-headless-capture.service | /etc/systemd/system/ |
| bot-vision-headless-capture.timer | /etc/systemd/system/ |

## Service

```
[Unit]
Description=Bot Vision Headless Capture
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
WorkingDirectory=/opt/trading
ExecStart=/usr/bin/bash /opt/trading/scripts/run_bot_vision_headless_capture.sh
User=ghost
Group=ghost
Nice=5
IOSchedulingClass=best-effort
TimeoutStartSec=120
```

## Timer

```
[Unit]
Description=Run Bot Vision Headless Capture every 10 minutes

[Timer]
OnBootSec=2min
OnUnitActiveSec=10min
RandomizedDelaySec=30s
Persistent=false
Unit=bot-vision-headless-capture.service

[Install]
WantedBy=timers.target
```

## Wrapper

```bash
#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="/opt/trading/modules/bot_vision/headless_capture"
cd "$MODULE_DIR"
exec /usr/bin/node capture_headless.js --profile profiles.example.json --once
```

## User

`ghost:ghost` — meme user que vision_bot, bot_vision_step2, desk_bridge.
Pas de root necessaire.
