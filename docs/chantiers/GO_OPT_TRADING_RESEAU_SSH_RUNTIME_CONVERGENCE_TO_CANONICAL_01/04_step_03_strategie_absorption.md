---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01_STEP_03_ABSORPTION
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - runtime
  - canonical
  - absorption
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01/01_matrice_capacites.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01/03_step_02_matrice_alias_wrappers.md
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/reseau_ssh_cmd.sh
  - modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/scripts/reseau_ssh_cmd.sh
  - scripts/reseau_ssh/reseau_ssh_cmd.sh
---

# Step 03 - strategie d'absorption

## Decision directrice
La famille `reseau_ssh` ne doit publier qu'une seule facade canonique finale :
- `modules/reseau_ssh/scripts/*`

## Repartition retenue
- facade publique canonique finale : `modules/reseau_ssh/scripts/*`
- implementation interne specialisee : `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/*`
- compat baseline : `modules/reseau_ssh_step1b`
- backend compat runtime : `scripts/reseau_ssh`

## Absorption retenue

### Ce qui reste dans le canonique
- entree `menu`
- entree `cmd`
- entree `sanity`
- delegation WG/firewall
- exposition explicite des commandes `baseline-*`

### Ce qui reste interne
- logique WG/firewall detaillee `reseau_ssh_step2`

### Ce qui reste en compat
- baseline hosts / ssh config / hostname de `step1b`
- backend operateur historique `scripts/reseau_ssh`

## Regle
Les compatibilites peuvent encore etre deleguees.

Elles ne doivent plus etre lues comme surfaces proprietaires de la famille.

## Target
1 module canonique par famille.
