---
doc_id: GO_AUTOMATION_SECURITY_SECRETS_PERMISSIONS_01_KILL_SWITCH
doc_type: security_kill_switch
go_id: GO_AUTOMATION_SECURITY_SECRETS_PERMISSIONS_01
status: draft
---

# 40_KILL_SWITCH.md

## Coupe-circuit général

### Déclencheurs

| Niveau | Déclencheur | Action |
|---|---|---|
| **L1 — Soft** | Détection d'anomalie (write in read-only mode) | Bloque l'action, log dans ledger |
| **L2 — Medium** | 3+ échecs d'approval en 5 min | Suspend les écritures automatisées 15 min |
| **L3 — Hard** | Secret leak détecté dans un output | Coupe TOUTES les écritures, notifie humain |
| **L4 — Critical** | Attaque ou compromission suspectée | Kill switch total + rollback si applicable |

### Implémentation

```yaml
kill_switch:
  enabled: true
  state_file: "data/runtime_health/kill_switch.state"
  states:
    - NORMAL          # tout autorisé
    - WRITES_SUSPENDED  # lectures only
    - FULL_STOP       # aucune action automatisée
  auto_reset:
    L1: 5 min
    L2: 15 min
    L3: humain requis
    L4: humain requis
```

### Procédure manuelle

```bash
# Activer kill switch
echo "FULL_STOP" > data/runtime_health/kill_switch.state

# Réactiver
echo "NORMAL" > data/runtime_health/kill_switch.state
```

Tous les workers lisent l'état du kill switch avant chaque action. Si FULL_STOP, toute action est refusée.
