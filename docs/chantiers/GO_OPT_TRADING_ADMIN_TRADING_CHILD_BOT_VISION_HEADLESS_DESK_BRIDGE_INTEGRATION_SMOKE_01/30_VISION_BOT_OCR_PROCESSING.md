---
doc_id: INTEGRATION_SMOKE_01_VISION_BOT
doc_type: vision_bot_processing
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 30_VISION_BOT_OCR_PROCESSING

## vision_bot watch loop

- **Statut**: active (running since Apr 19)
- **Traitement**: Chaque capture headless est detectee, OCR applique, deplacee vers vision_processed
- **Sorties**: .md (Markdown OCR) + .txt (plain text) dans vision_outbox
- **Latence**: < 10 secondes apres apparition du PNG

## OCR outputs (derniers)

| Timestamp | .md | .txt |
| --- | --- | --- |
| 18:20 | 943 B | 427 B |
| 18:30 | 578 B | 427 B |
| 18:40 | 577 B | 426 B |
| 18:51 | 940 B | 789 B |
| 19:01 | 760 B | 609 B |
| 19:11 | 840 B | 689 B |
| 19:21 | 925 B | 774 B |
| 19:31 | 398 B | 247 B |

## bot_vision_step2

- **Statut**: active (running since Apr 19)
- **Erreur**: TimeoutError SSL read (mai 4 14:48) — isolee, non recurrente
- **Impact**: Aucun sur le flux headless. Telegram polling intermittent.

## Verdict OCR

**PASS** — vision_bot traite automatiquement chaque capture headless.
Aucun fichier ignore, aucun blocage.
