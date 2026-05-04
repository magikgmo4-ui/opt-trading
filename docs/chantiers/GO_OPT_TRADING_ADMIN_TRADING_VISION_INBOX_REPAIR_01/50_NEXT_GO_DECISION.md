---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01_NEXT_GO
doc_type: next_go_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 50_NEXT_GO_DECISION — Vision Inbox Repair

## Verdict

**PASS** — 14 fichiers corrompus en quarantaine, inbox propre, macro-xau.timer desactive. Services critiques intacts.

## Resume des actions

- **Phase 2**: 14 fichiers deplaces en quarantaine (9 x 0-byte PNG + 5 x .uploading)
- **Phase 3**: macro-xau.timer desactive (enabled->disabled, active->inactive)
- **Phase 4**: Post-checks tous OK

## Prochain GO recommande (P1)

### GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01

**Objectif**: Relancer desk_bridge pour deverrouiller le pipeline Vision -> Desk.

L'inbox est propre. desk_bridge peut etre relance. Un GO dedie est necessaire car il implique un `systemctl start` (action runtime).

**Actions**:
1. Verifier inbox toujours propre
2. Relancer desk_bridge: `sudo systemctl start desk_bridge.service`
3. Verifier le resultat (success ou nouvelle erreur)
4. Si success: pipeline Vision deverrouille
5. Si echec: nouvelle analyse

## Prochains GO

### P1: GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01
Relancer desk_bridge, deverrouiller pipeline

### P2: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01
Lancer un run Desk Pro frais (PAPER mode)

### P3: GO_OPT_TRADING_ADMIN_TRADING_BRIDGE_GUARD_ADD_01
Ajouter garde-fou `[ -s "$file" ]` dans bridge_vision_to_desk_inbox.sh
