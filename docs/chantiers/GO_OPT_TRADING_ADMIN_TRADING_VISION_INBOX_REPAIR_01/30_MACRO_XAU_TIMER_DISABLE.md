---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01_MACRO_XAU
doc_type: timer_disable_log
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 30_MACRO_XAU_TIMER_DISABLE

## Etat avant

| Propriete | Valeur |
| --- | --- |
| Unite | macro-xau.timer |
| is-enabled | enabled |
| is-active | active |
| Trigger | every 30 min |
| Last trigger | 2026-05-04 15:03:31 |
| Service associe | macro-xau.service (failed, 203/EXEC) |
| Cause echec | /opt/trading/jobs/macro_xau/run.sh absent |

## Action

```bash
sudo systemctl disable --now macro-xau.timer
```

## Etat apres

| Propriete | Valeur |
| --- | --- |
| is-enabled | disabled |
| is-active | inactive |

## Justification

- macro-xau est OBSOLETE (decision GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01)
- Module /opt/trading/jobs/macro_xau/run.sh absent
- Timer relancait inutilement toutes les 30 minutes
- Aucun impact fonctionnel (service echouait deja)

## Non modifie

- macro-xau.service non supprime (juste deja disabled)
- Fichiers systemd conserves
- Aucun autre timer touche
