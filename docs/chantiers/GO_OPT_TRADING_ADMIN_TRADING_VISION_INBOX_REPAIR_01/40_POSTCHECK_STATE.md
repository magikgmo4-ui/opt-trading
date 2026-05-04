---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01_POSTCHECK
doc_type: postcheck_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 40_POSTCHECK_STATE — Etat apres reparation

## Inbox vision/SFTP

**CLEAN** — Aucun fichier 0-byte ou .uploading restant dans vision_inbox.

L'inbox est vide. Pret pour nouveaux uploads ShareX.

## macro-xau.timer

**DISABLED + INACTIVE** — Plus de retries inutiles toutes les 30 minutes.

## Services critiques (apres)

| Service | Statut |
| --- | --- |
| tv-webhook | active |
| tv-perf | active |
| vision_bot | active |
| bot_vision_step2 | active |
| ngrok-tv | active |

Aucun service perturbe.

## Desk Pro /shared

5 fichiers dans /shared/desk_pro/latest/ — intacts, inchanges.

## Quarantaine

14 fichiers conserves dans `/srv/sftp/shared_files/shared/quarantine/GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01_20260504T190858Z/`

## Limites restantes

- desk_bridge n'a pas ete relance (necessite un GO dedie pour le redemarrage de service)
- Aucune nouvelle capture ShareX n'a ete testee
- Les timers desactives (trading-heartbeat, bot_vision_step2_send) n'ont pas ete touches
- Le script bridge n'a pas ete modifie (garde-fou `[ -s "$file" ]` non ajoute)
