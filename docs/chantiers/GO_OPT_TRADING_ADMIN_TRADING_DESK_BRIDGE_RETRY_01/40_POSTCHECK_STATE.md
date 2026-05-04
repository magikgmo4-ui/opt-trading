---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01_POSTCHECK
doc_type: postcheck_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 40_POSTCHECK_STATE — Etat apres retry

## Services critiques

| Service | Statut |
| --- | --- |
| tv-webhook | active |
| tv-perf | active |
| vision_bot | active |
| bot_vision_step2 | active |
| ngrok-tv | active |

Aucun service perturbe par le retry.

## desk_bridge

| Propriete | Valeur |
| --- | --- |
| Statut | failed (exit-code, status=2) |
| Erreur | no screen_*.png found |
| Classification | COMPORTEMENT NORMAL (pas d'input) |
| Cause precedente (PIL) | RESOLUE |

## Inbox et vision

| Dossier | Fichiers | Etat |
| --- | --- | --- |
| vision_inbox | 0 | CLEAN |
| vision_processed | 0 | CLEAN |
| inbox | - | Inchanged |

## macro-xau.timer

**DISABLED + INACTIVE** — confirme non reactive.

## Desk Pro /shared

5 fichiers dans /shared/desk_pro/latest/ — intacts, inchanges.

## Quarantaine

14 fichiers toujours presents dans la quarantaine precedente. Intacts.
