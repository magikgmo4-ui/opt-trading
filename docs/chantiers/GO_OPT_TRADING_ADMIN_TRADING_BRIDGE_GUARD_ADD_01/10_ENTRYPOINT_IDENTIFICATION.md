---
doc_id: BRIDGE_GUARD_01_ENTRYPOINT
doc_type: entrypoint_id
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BRIDGE_GUARD_ADD_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 10_ENTRYPOINT_IDENTIFICATION

## Fichier patché

`scripts/desk_bridge/bridge_vision_to_desk_inbox.sh` (151 → ~180 lines)

## Service

desk_bridge.service (oneshot, user=ghost, timer=desk_bridge.timer)
ExecStart=/opt/trading/scripts/desk_bridge/bridge_vision_to_desk_inbox.sh

## Entrypoint

Unique. Aucun wrapper, aucun doublon. Systemd seulement.
