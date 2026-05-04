---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_PARENT_REALIGNMENT_01_CURRENT
doc_type: current_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_PARENT_REALIGNMENT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 10_CURRENT_STATE — Etat avant realignement

## admin-trading — GO chain (tous PASS)

| # | GO | Verdict |
| --- | --- | --- |
| 1 | GO_PARENT_REVIEW_01 | PASS — Machine auditee |
| 2 | GO_DESK_PRO_RUNTIME_REVIEW_01 | PASS — Desk Pro audite |
| 3 | GO_VISION_INBOX_REPAIR_01 | PASS — 14 fichiers quarantaines |
| 4 | GO_DESK_BRIDGE_RETRY_01 | PASS — Pipeline deverrouille |
| 5 | GO_DESK_PRO_SMOKE_01 | PASS — Smoke 11/11 OK |

## Parents admin-trading dans les index (sot/mainline)

### Parent machine (canonique)

`GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01`
- GO_INDEX.md: OPEN (ligne 91, entree 132)
- GO_PARENT_THREAD_MAP.md: THREAD_MACHINE_ADMIN_TRADING
- Dossier: docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/ (3 fichiers)

### Parent specialise (non canonise)

`GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01`
- GO_INDEX.md: **ABSENT**
- GO_CLOSED_INDEX.md: **ABSENT**
- GO_PARENT_THREAD_MAP.md: **ABSENT**
- Existe uniquement sur branche non mergee (go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01)
- Dossier: present sur cette branche seulement (8 fichiers)
- inbox/: present sur cette branche seulement

### Child review (non canonise)

`GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01`
- Meme statut: branche non mergee
- Dossier: 7 fichiers
- inbox: 1 fichier

## Etat admin-trading runtime

| Service | Statut |
| --- | --- |
| tv-webhook | active |
| tv-perf | active |
| vision_bot | active |
| bot_vision_step2 | active |
| ngrok-tv | active |
| macro-xau.timer | disabled + inactive |
| desk_bridge.timer | active (clean fail si inbox vide) |
| vision_inbox | clean (0 fichiers) |
| Desk Pro runner | OK (PAPER mode) |

## Constat

- Le parent machine canonique est bien en place
- Le parent specialise headless n'a jamais ete ajoute aux indexes
- Aucun patch d'index necessaire
- Seul le chantier de realignment documentaire est requis
