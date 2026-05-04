---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01_NEXT_GO
doc_type: next_go_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 60_NEXT_GO_DECISION — Systemd Automation

## Verdict

**PASS** — Timer systemd operationnel. Capture automatisee toutes les 10 minutes.

## Prochain GO recommande (P1)

### GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01

**Objectif**: Valider le pipeline complet capture -> bridge -> Desk Pro avec le timer actif.

La capture automatique est en place. Le prochain pas est de verifier que:
1. Les captures automatiques arrivent dans vision_inbox
2. vision_bot les traite (OCR -> processed + outbox)
3. desk_bridge les decoupe (crop 2x2 -> inbox)
4. Desk Pro recoit les snapshots

## Backlog

| GO | Priorite | Description |
| --- | --- | --- |
| GO_DESK_BRIDGE_INTEGRATION_SMOKE_01 | P1 | Smoke pipeline complet auto |
| GO_BRIDGE_GUARD_ADD_01 | P2 | Garde-fou [ -s ] dans bridge |
| GO_DESK_PRO_SHARED_REFRESH_01 | P3 | Rafraichir /shared/desk_pro/latest |
| GO_BOT_VISION_HEADLESS_CLOSEOUT_01 | P3 | Closeout du chantier headless |
