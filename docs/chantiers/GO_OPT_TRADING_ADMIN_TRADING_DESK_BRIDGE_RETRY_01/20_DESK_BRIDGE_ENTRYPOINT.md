---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01_ENTRYPOINT
doc_type: entrypoint_identification
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 20_DESK_BRIDGE_ENTRYPOINT

## Entrypoint identifie

| Propriete | Valeur |
| --- | --- |
| Service | desk_bridge.service |
| Type | oneshot |
| User | ghost |
| Group | ghost |
| WorkingDirectory | /opt/trading |
| ExecStart | /opt/trading/scripts/desk_bridge/bridge_vision_to_desk_inbox.sh |
| Timer | desk_bridge.timer (every 10 min) |
| Unit file | /etc/systemd/system/desk_bridge.service |

## Preuves

- `systemctl cat desk_bridge.service` confirme le ExecStart
- `ls /opt/trading/scripts/desk_bridge/` contient un seul script: bridge_vision_to_desk_inbox.sh (3868 B, executable)
- Aucun wrapper dans /usr/local/bin — l'entrypoint est systemd uniquement
- Pas d'ambiguite : un seul script, un seul service

## Methode de retry

```bash
sudo systemctl start desk_bridge.service
```

Justification: le service oneshot est l'entrypoint canonique, avec WorkingDirectory et User correctement configures dans le unit file.

## Note

Le timer desk_bridge.timer declenche automatiquement le service toutes les 10 minutes. Le retry manuel est equivalent au declenchement automatique du timer.
