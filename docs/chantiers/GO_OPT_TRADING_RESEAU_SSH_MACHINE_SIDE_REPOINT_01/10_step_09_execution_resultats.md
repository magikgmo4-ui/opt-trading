---
doc_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01_STEP_09_EXECUTION
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
  - execution
  - results
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/09_step_08_resultats_inventaire_reel.md
  - modules/reseau_ssh/scripts/install_canonical_shortcuts.sh
---

# Step 09 - resultats d'execution

## `db-layer`
- payload canonique repo-side deploye
- alias courts repointes vers :
  - `/opt/trading/modules/reseau_ssh/scripts/menu.sh`
  - `/opt/trading/modules/reseau_ssh/scripts/cmd.sh`
  - `/opt/trading/modules/reseau_ssh/scripts/sanity_check.sh`
- `sanity-reseau_ssh` : PASS
- `cmd-reseau_ssh sanity` : PASS

## `admin-trading`
- payload canonique repo-side deploye
- alias courts repointes vers :
  - `/opt/trading/modules/reseau_ssh/scripts/menu.sh`
  - `/opt/trading/modules/reseau_ssh/scripts/cmd.sh`
  - `/opt/trading/modules/reseau_ssh/scripts/sanity_check.sh`
- `sanity-reseau_ssh` : PASS
- `cmd-reseau_ssh sanity` : PASS

## `fantome`
- payload canonique repo-side deploye
- alias courts crees vers :
  - `/home/fantome/opt-trading/modules/reseau_ssh/scripts/menu.sh`
  - `/home/fantome/opt-trading/modules/reseau_ssh/scripts/cmd.sh`
  - `/home/fantome/opt-trading/modules/reseau_ssh/scripts/sanity_check.sh`
- `sanity-reseau_ssh` : PASS
- `cmd-reseau_ssh sanity` : PASS

## `student`
- payload canonique repo-side deploye
- alias courts repointes vers :
  - `/opt/trading/modules/reseau_ssh/scripts/menu.sh`
  - `/opt/trading/modules/reseau_ssh/scripts/cmd.sh`
  - `/opt/trading/modules/reseau_ssh/scripts/sanity_check.sh`
- `sanity-reseau_ssh` : PASS
- `cmd-reseau_ssh sanity` : PASS

## Point important
Le lot machine-side a revele un gap supplementaire :
- le canonique repo-side n'etait pas deploye tel quel sur les machines
- un payload minimal a ete copie sur `db-layer`, `admin-trading`, `student`, `fantome` avant repointage

## Etat atteint
- 4 machines migrees avec PASS
- alias courts `reseau_ssh` repointes sur tout le parc joignable cible
- `scripts/reseau_ssh` et `step1b` restent encore presents uniquement comme surfaces de compatibilite / rollback

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
