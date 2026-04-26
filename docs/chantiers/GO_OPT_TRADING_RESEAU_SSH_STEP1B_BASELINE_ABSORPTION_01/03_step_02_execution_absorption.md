---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_BASELINE_ABSORPTION_01_EXECUTION
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_BASELINE_ABSORPTION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - step1b
  - baseline
  - execution
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/_reseau_ssh_baseline.sh
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/scripts/menu.sh
---

# Step 02 - execution absorption

## Execution

Les commandes `baseline-*` ne sont plus deleguees vers `reseau_ssh_step1b`.

Elles sont maintenant implementees directement dans `modules/reseau_ssh`.

## Resultat

- `reseau_ssh` porte maintenant aussi la baseline hosts / ssh / hostname / sanity
- `reseau_ssh_step1b` n'est plus requis par le canonique
- `reseau_ssh_step1b` devient `archive_candidate`

## Target
1 module canonique par famille.
