---
doc_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01_SAFE_BUTTONS
doc_type: cockpit_safe_buttons
go_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01
status: draft
---

# 80_SAFE_BUTTONS_AND_KILL_SWITCH.md

## Safe buttons

Tous les boutons d'action dans le cockpit suivent ces règles :

| Principe | Description |
|---|---|
| **Lecture seule par défaut** | Les boutons `VIEW`, `REFRESH`, `EXPORT` sont sans confirmation |
| **Confirmation requise** | `APPROVE`, `REJECT`, `RESTART`, `STOP` nécessulent une modale de confirmation |
| **Dual confirm** | `KILL_SWITCH_ACTIVATE` nécessite dual confirm (2 humains) |
| **Log dans ledger** | Toute action d'écriture est loggée dans le ledger G06 |
| **Undo** | Toute action destructive a une procédure d'undo documentée |

## Kill switch

### Visuel

```text
┌────────────────────────────────────────┐
│  KILL SWITCH                           │
│  État actuel: NORMAL                   │
│                                        │
│  [ACTIVATE FULL STOP]  [ACTIVATE       │
│                        WRITES_SUSPEND] │
│                                        │
│  Dernière activation: 2026-05-20 22:00 │
│  Activé par: human_01                  │
└────────────────────────────────────────┘
```

### Niveaux

| Niveau | Bouton | Confirmation | Effet |
|---|---|---|---|
| L1 Soft | [WRITES_SUSPEND] | Simple | Bloque les écritures, lectures OK |
| L2 Hard | [FULL_STOP] | Dual confirm | Bloque toute action automatisée |
| Reset | [RESET TO NORMAL] | Simple | Réactive tout |

### Périmètre

- Le kill switch affecte TOUS les workers
- L'état est persistant dans `data/runtime_health/kill_switch.state`
- La désactivation est loggée dans le ledger
- Les humains peuvent toujours agir (override)
