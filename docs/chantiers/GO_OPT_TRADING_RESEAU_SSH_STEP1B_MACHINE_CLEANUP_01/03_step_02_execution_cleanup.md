---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_MACHINE_CLEANUP_01_EXECUTION
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_MACHINE_CLEANUP_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - step1b
  - machine_cleanup
  - execution
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/status/reseau_ssh_canonique.md
  - modules/reseau_ssh/scripts/capture_shortcuts_snapshot.sh
---

# Step 02 - execution cleanup

## Execution

Moves machine-side executes :

- `db-layer`
  - source : `/opt/trading/modules/reseau_ssh_step1b`
  - archive : `/opt/trading/_archive/legacy_modules/reseau_ssh_step1b_machine_2026-04-25`
- `admin-trading`
  - source : `/opt/trading/modules/reseau_ssh_step1b`
  - archive : `/opt/trading/_archive/legacy_modules/reseau_ssh_step1b_machine_2026-04-25`
- `student`
  - source : `/opt/trading/modules/reseau_ssh_step1b`
  - archive : `/opt/trading/_archive/legacy_modules/reseau_ssh_step1b_machine_2026-04-25`
- `fantome`
  - source : `/home/fantome/opt-trading/modules/reseau_ssh_step1b`
  - archive : `/home/fantome/opt-trading/_archive/legacy_modules/reseau_ssh_step1b_machine_2026-04-25`

Le cleanup a expose un drift machine-side :
- les hotes n'avaient pas encore la version canonique absorbant `baseline-*`

Correctif applique :
- backup du module canonique distant :
  - `.../reseau_ssh_canonical_before_step1b_cleanup_sync_2026-04-25`
- resynchronisation des repertoires :
  - `modules/reseau_ssh/scripts`
  - `modules/reseau_ssh/baseline`

## Validation

- `db-layer` : `baseline-*` OK, `sanity-reseau_ssh` OK
- `admin-trading` : `baseline-*` OK, `sanity-reseau_ssh` OK
- `student` : `baseline-*` OK, `sanity-reseau_ssh` OK
- `fantome` : `baseline-*` OK, `RESEAU_SSH_SKIP_DEEP_SANITY=1 sanity-reseau_ssh` OK

## Limite restante

`fantome` echoue encore au deep sanity complet avec :
- `ModuleNotFoundError: No module named 'yaml'`

Le point est borne comme gap d'environnement Python, pas comme echec du cleanup `step1b`.

## Target
1 module canonique par famille.
