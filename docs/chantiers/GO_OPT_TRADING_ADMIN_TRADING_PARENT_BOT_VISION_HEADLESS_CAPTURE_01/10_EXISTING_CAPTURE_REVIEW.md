---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01_EXISTING
doc_type: existing_capture_review
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01
status: open
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 10_EXISTING_CAPTURE_REVIEW — Chaine actuelle

## Chaine complete

```
ShareX (Windows/cursor-ai)
  -> SFTP upload -> /srv/sftp/shared_files/shared/vision_inbox/screen_*.png

vision_bot (watch loop, admin-trading)
  -> OCR (tesseract) ou fallback dummy
  -> Deplace vers vision_processed/
  -> Ecrit .md/.txt dans vision_outbox/

desk_bridge (timer 10 min, admin-trading)
  -> bridge_vision_to_desk_inbox.sh
  -> Crop 2x2 avec PIL (convert ou Python)
  -> Renomme q_*.png dans /shared/inbox/
  -> Appelle desk_snapshot_ingest

Desk Pro
  -> Consomme les snapshots
  -> Pipeline probability -> decision -> risk -> ...
```

## Modules concernes

### vision_bot (ACTIF)
- Service: systemd, user=ghost, watch loop
- Script: /opt/trading/modules/vision_bot/app/vision_bot.py watch
- PID: 798, memoire: 51.3M, CPU: 17 min depuis Apr 19
- Entree: /srv/sftp/shared_files/shared/vision_inbox/screen_*.png
- Sortie: /srv/sftp/shared_files/shared/vision_processed/ et vision_outbox/
- Wrappers: cmd-vision_bot, menu-vision_bot, sanity-vision_bot

### bot_vision_step2 (ACTIF)
- Service: systemd, user=ghost, venv dedie
- Script: /opt/trading/modules/bot_vision_step2/app/bot_vision_step2.py serve
- PID: 1463, memoire: 17.3M, CPU: 10 min depuis Apr 19
- Role: Telegram /analyze -> OpenAI Vision -> Desk Pro artifacts
- Wrappers: cmd-bot_vision_step2, menu-bot_vision_step2, sanity-bot_vision_step2
- Config: config/bot_vision.env, config/bot_vision.env.example
- Systemd: service + send.timer (disabled) + prune.timer (enabled)
- Watchdog: scripts/sharex_capture_watchdog.ps1 (Windows)

### bot_vision (LEGACY)
- Skeleton step1, generateur visuel placeholder
- /opt/trading/modules/bot_vision/bot_vision_step1/desk_pro_vision/
- Wrappers: cmd-bot_vision, menu-bot_vision, sanity-bot_vision
- Non survivant. Garde pour trajectoire historique.

### desk_bridge
- Service oneshot, timer 10 min
- Script: /opt/trading/scripts/desk_bridge/bridge_vision_to_desk_inbox.sh
- Wrappers: aucun (systemd uniquement)
- Statut: failed (no screen_*.png found) = normal quand inbox vide

## Problemes identifies

1. **SFTP fragile**: fichiers 0-byte (connection interrompue) -> PIL crash
2. **.uploading partiels**: SFTP ne renomme pas en .png final -> fichiers abandonnes
3. **Pas de garde-fou** dans bridge_vision_to_desk_inbox.sh avant Image.open()
4. **Dependance Windows**: si cursor-ai eteint -> zero capture
5. **vision_inbox vide actuellement**: pipeline deverrouille mais sans input
