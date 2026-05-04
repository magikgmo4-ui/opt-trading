---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01_SHAREX
doc_type: sharex_sftp_review
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 20_REVIEW_SHAREX_AND_SFTP_PATH

## Flux actuel

```
ShareX (Windows/cursor-ai)
  |
  | SFTP upload
  v
/srv/sftp/shared_files/shared/vision_inbox/screen_*.png
  |
  | vision_bot watch loop (polling)
  v
vision_processed/screen_*.png
  + vision_outbox/screen_*.md (OCR output)
```

## Problemes documentes

### P1: Fichiers 0-byte (RESOLU)

- **Cause**: Connexion SFTP interrompue pendant upload -> fichier cree vide
- **Impact**: PIL crash dans desk_bridge
- **Resolution**: GO_VISION_INBOX_REPAIR_01 (9 fichiers 0-byte -> quarantaine)
- **Recurrence**: Possible si SFTP instable

### P2: Uploads partiels .uploading (RESOLU)

- **Cause**: SFTP utilise .uploading comme suffixe temporaire, mais ne rename pas si interrompu
- **Impact**: Fichiers abandonnes, polluent vision_inbox
- **Resolution**: GO_VISION_INBOX_REPAIR_01 (5 .uploading -> quarantaine)
- **Recurrence**: Possible si SFTP instable

### P3: Dependance Windows (NON RESOLU)

- **Cause**: ShareX ne tourne que sur Windows/cursor-ai
- **Impact**: Si cursor-ai eteint/absent -> zero capture
- **Resolution**: Bot vision headless (ce chantier)

### P4: Pas de garde-fou dans desk_bridge (NON RESOLU)

- **Cause**: bridge_vision_to_desk_inbox.sh appelle Image.open() sans verifier taille > 0
- **Impact**: Crash PIL si fichier 0-byte present
- **Resolution**: A implementer (GO_BRIDGE_GUARD_ADD_01)

## SFTP server

| Propriete | Valeur |
| --- | --- |
| Module | shared_files_sftp |
| Chemin | /srv/sftp/shared_files/shared/ |
| Alias | /shared -> /srv/sftp/shared_files/shared/ |
| Vision inbox | /shared/vision_inbox/ |
| User SFTP | ghost |
| Statut | Operationnel |

## ShareX (Windows)

| Propriete | Valeur |
| --- | --- |
| Configuration | SHAREX_SETUP.md (modules/vision_bot/) |
| Destination | SFTP -> admin-trading:22 |
| Remote folder | /srv/sftp/shared_files/shared/vision_inbox |
| Nommage | screen_{yyyy}-{MM}-{dd}_{HH}-{mm}-{ss}_{rn:6}.png |
| Watchdog | modules/bot_vision_step2/scripts/sharex_capture_watchdog.ps1 |

## Impact headless

La capture headless ecrit directement dans vision_inbox sans SFTP.
ShareX peut rester comme fallback. Les deux sources peuvent coexister
grace au nommage unique (timestamp + random).
