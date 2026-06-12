---
doc_id: HEADLESS_CLOSEOUT_01_COMMANDS
doc_type: operator_commands
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_CLOSEOUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 40_OPERATOR_COMMANDS

## Verifier etat

```bash
# Timers
systemctl list-timers | grep -E "bot-vision-headless|desk_bridge"

# Status services
systemctl status bot-vision-headless-capture.timer desk_bridge.timer vision_bot

# Verifier inbox
ls -la /srv/sftp/shared_files/shared/vision_inbox/
ls -la /srv/sftp/shared_files/shared/vision_processed/

# Verifier corruption
find /srv/sftp/shared_files/shared/vision_inbox -type f \( -size 0 -o -name "*.uploading*" \)

# Verifier Desk Pro
cd /opt/trading && /opt/trading/venv/bin/python -m modules.desk_pro_runner.app.desk_pro_runner status
```

## Lancer capture manuelle

```bash
# Oneshot via systemd
sudo systemctl start bot-vision-headless-capture.service

# Ou directement
cd /opt/trading/modules/bot_vision/headless_capture
node capture_headless.js --profile profiles.example.json --once
```

## Lire logs

```bash
# Headless capture
sudo journalctl -u bot-vision-headless-capture.service -n 20

# Desk bridge
sudo journalctl -u desk_bridge.service -n 20

# Vision bot
sudo journalctl -u vision_bot -n 20
```

## Desk Pro

```bash
cd /opt/trading
/opt/trading/venv/bin/python -m modules.desk_pro_runner.app.desk_pro_runner status
/opt/trading/venv/bin/python -m modules.desk_pro_runner.app.desk_pro_runner run  # PAPER mode
```

## RISKS

- À qualifier.
