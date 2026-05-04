---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01_ARCHITECTURE
doc_type: target_architecture
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01
status: open
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 30_TARGET_ARCHITECTURE — Bot Vision Headless

## Architecture cible

```
┌─────────────────────────────────────────────────────────┐
│ admin-trading                                            │
│                                                          │
│  bot_vision_headless (systemd timer)                     │
│    ├── capture.js (Playwright + Chromium headless)       │
│    │     ├── page.goto(TARGET_URL)                       │
│    │     └── page.screenshot() -> /tmp/capture_*.png     │
│    ├── atomic_write.sh (wrapper)                         │
│    │     ├── mv capture_*.png -> vision_inbox/.uploading │
│    │     ├── verify size > 0                             │
│    │     └── mv .uploading -> screen_YYYY-MM-DD_*.png    │
│    └── sortie -> vision_inbox/screen_*.png               │
│                                                          │
│  vision_bot (watch loop)                                 │
│    ├── detecte screen_*.png dans vision_inbox            │
│    ├── OCR (tesseract) ou fallback                       │
│    ├── deplace vers vision_processed/                    │
│    └── ecrit vision_outbox/*.md                          │
│                                                          │
│  desk_bridge (timer 10 min)                              │
│    ├── crop 2x2 (PIL)                                   │
│    ├── inbox/q_*.png                                     │
│    └── desk_snapshot_ingest                              │
│                                                          │
│  Desk Pro                                                │
│    └── pipeline probability -> decision -> risk          │
│                                                          │
│  /shared/desk_pro/latest/                                │
│    └── sorties consommables par db-layer/student         │
└─────────────────────────────────────────────────────────┘
```

## Composants

### bot_vision_headless (NOUVEAU)

| Propriete | Valeur |
| --- | --- |
| Runtime | Node.js + Playwright + Chromium |
| Machine | admin-trading |
| User | ghost |
| Venv | non (Node.js, pas Python) |
| Timer | systemd, intervalle configurable (ex: 5 min) |
| Sortie | /srv/sftp/shared_files/shared/vision_inbox/screen_*.png |

### Modules conserves (inchanges)

| Module | Role | Modification |
| --- | --- | --- |
| vision_bot | OCR + inbox-outbox | Aucune |
| bot_vision_step2 | Telegram + OpenAI Vision | Aucune |
| desk_bridge | Crop 2x2 + ingest | Aucune (garde-fou optionnel) |
| Desk Pro | Pipeline trading | Aucune |

### Modules obsoletes (apres migration)

| Module | Devenir |
| --- | --- |
| ShareX (Windows) | Optionnel, fallback |
| SFTP upload | Plus necessaire (capture locale) |
| bot_vision (step1) | Reste LEGACY |
