---
doc_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01_STEP_07_CONNECTIVITY
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - machine
  - ssh
  - connectivity
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/02_step_01_inventaire_et_rollback.md
---

# Step 07 - probe de connectivite

## Resolution locale des aliases
- `db-layer` -> `ghost@192.168.0.100`
- `admin-trading` -> `ghost@192.168.0.111`
- `student` -> `student@192.168.0.142`
- `fantome` -> `fantome@192.168.0.191`

## Tests lances
Depuis la session courante, en lecture seule :

```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 <host> hostname
```

## Resultat
Probe initial :
- `db-layer` : timeout port 22
- `admin-trading` : timeout port 22
- `student` : timeout port 22
- `fantome` : timeout port 22

Probe rejoue ensuite :
- `db-layer` : SSH reachable
- `admin-trading` : SSH reachable
- `student` : SSH reachable
- `fantome` : SSH reachable

## Conclusion
Le blocage initial etait conjoncturel :
- reachability reseau variable selon le moment
- `student` etait eteint au premier passage

Au final, la session courante a bien pu atteindre les 4 hotes du lot.

## Point de reprise
Le probe est suffisant pour preuve.

La suite a bien pu etre executee :
- inventaire reel
- deploiement du payload canonique
- repointage machine-side

## Target
1 module canonique par famille.
