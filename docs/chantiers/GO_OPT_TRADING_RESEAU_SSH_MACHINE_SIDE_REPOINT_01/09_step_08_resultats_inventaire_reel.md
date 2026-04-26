---
doc_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01_STEP_08_ACTUAL_INVENTORY
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
  - inventory
  - runtime
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/08_step_07_probe_connectivite.md
---

# Step 08 - resultats d'inventaire reel

## `db-layer`
- SSH reachable depuis la session courante : oui
- alias courts installes : oui
- cibles alias courts :
  - `menu-reseau_ssh` -> `/opt/trading/scripts/reseau_ssh/reseau_ssh_menu.sh`
  - `cmd-reseau_ssh` -> `/opt/trading/scripts/reseau_ssh/reseau_ssh_cmd.sh`
  - `sanity-reseau_ssh` -> `/opt/trading/scripts/reseau_ssh/sanity_reseau_ssh.sh`
- alias `*_reseau_ssh_step2` installes : oui
- cibles `*_step2` :
  - `/opt/trading/modules/reseau_ssh_step2/scripts/menu.sh`
  - `/opt/trading/modules/reseau_ssh_step2/scripts/cmd.sh`
  - `/opt/trading/modules/reseau_ssh_step2/scripts/sanity_check.sh`
- `sanity-reseau_ssh` : PASS

## `admin-trading`
- SSH reachable depuis la session courante : oui
- alias courts installes : oui
- cibles alias courts :
  - `menu-reseau_ssh` -> `/opt/trading/scripts/reseau_ssh/reseau_ssh_menu.sh`
  - `cmd-reseau_ssh` -> `/opt/trading/scripts/reseau_ssh/reseau_ssh_cmd.sh`
  - `sanity-reseau_ssh` -> `/opt/trading/scripts/reseau_ssh/sanity_reseau_ssh.sh`
- alias `*_reseau_ssh_step2` installes : non
- `sanity-reseau_ssh` : PASS

## `fantome`
- SSH reachable depuis la session courante : oui
- alias courts installes : non
- alias `*_reseau_ssh_step2` installes : non
- chemins repo presents :
  - `/opt/trading/scripts/reseau_ssh`
  - `/opt/trading/modules/reseau_ssh`
  - `/opt/trading/modules/reseau_ssh_step1b`
  - `/opt/trading/modules/reseau_ssh_step2`

## `student`
- SSH reachable depuis la session courante : oui
- alias courts installes : oui
- cibles alias courts :
  - `menu-reseau_ssh` -> `/opt/trading/scripts/reseau_ssh/reseau_ssh_menu.sh`
  - `cmd-reseau_ssh` -> `/opt/trading/scripts/reseau_ssh/reseau_ssh_cmd.sh`
  - `sanity-reseau_ssh` -> `/opt/trading/scripts/reseau_ssh/sanity_reseau_ssh.sh`
- alias `*_reseau_ssh_step2` installes : oui
- cibles `*_step2` :
  - `/opt/trading/modules/reseau_ssh_step2/scripts/menu.sh`
  - `/opt/trading/modules/reseau_ssh_step2/scripts/cmd.sh`
  - `/opt/trading/modules/reseau_ssh_step2/scripts/sanity_check.sh`
- `sanity-reseau_ssh` : PASS

## Conclusion
Etat reel avant repointage :
- `db-layer` = bon candidat de preuve
- `admin-trading` = bon candidat de repointage, mais sans compat `step2` preexistante
- `fantome` = cas simple d'installation des alias canoniques
- `student` = meme profil de migration que `db-layer`, avec compat `step2` preexistante

## Target
1 module canonique par famille.
