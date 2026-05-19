---
doc_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01_STEP_01_INVENTORY
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
  - rollback
  - inventory
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/capture_shortcuts_snapshot.sh
  - modules/reseau_ssh/scripts/install_canonical_shortcuts.sh
---

# Step 01 - inventaire et rollback

## Snapshot avant action
Commande de base à lancer sur chaque machine :

```bash
/opt/trading/modules/reseau_ssh/scripts/capture_shortcuts_snapshot.sh
```

## Donnees à capturer
- `command -v menu-reseau_ssh`
- `command -v cmd-reseau_ssh`
- `command -v sanity-reseau_ssh`
- `command -v menu-reseau_ssh_step2`
- `command -v cmd-reseau_ssh_step2`
- `command -v sanity-reseau_ssh_step2`
- `readlink -f` des 6 alias
- présence de `/opt/trading/scripts/reseau_ssh`
- présence de `/opt/trading/modules/reseau_ssh`
- présence de `/opt/trading/modules/reseau_ssh_step1b`

## Mapping SSH local résolu
- `db-layer` -> user `ghost`, host `192.168.0.100`
- `admin-trading` -> user `ghost`, host `192.168.0.111`
- `student` -> user `student`, host `192.168.0.142`
- `fantome` -> user `fantome`, host `192.168.0.191`

## Rollback minimal
Si le repointage échoue :
- restaurer les trois alias courts sur leurs cibles capturées avant action
- ne pas toucher à `scripts/reseau_ssh`
- ne pas toucher à `step1b`
- ne pas toucher aux alias `*_reseau_ssh_step2`

## Critère d’arrêt
Ne rien repointer si :
- le snapshot est incomplet
- `sanity-reseau_ssh` échoue déjà avant action
- `modules/reseau_ssh/scripts/*` est absent sur la machine

## Target
1 module canonique par famille.
