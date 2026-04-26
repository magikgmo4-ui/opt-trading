---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01_STEP_04_SWITCH_PLAN
doc_type: chantier_execution_plan
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01
status: complete
lifecycle_stage: execution_plan
topic_keys:
  - opt-trading
  - reseau_ssh
  - runtime
  - aliases
  - switch_plan
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01/01_plan_operationnel_step_by_step.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/01_plan_operationnel_step_by_step.md
---

# Step 04 - plan de bascule des alias courts

## Sequence retenue

### Phase 1 - facade repo-side
Statut :
- complete

Resultat :
- `modules/reseau_ssh/scripts/*` est la facade canonique repo-side
- `reseau_ssh_step2` reste implementation interne

### Phase 2 - rename et registre repo-side
Statut :
- complete

Resultat :
- nom final `modules/reseau_ssh` recupere
- ancien occupant legacy sorti en archive
- registre aligne sur `reseau_ssh`

### Phase 3 - bascule machine-side
Statut :
- pending

Objectif :
- repointer `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh`
- capturer rollback et smoke tests

### Phase 4 - retrait des compatibilites
Statut :
- pending

Objectif :
- reduire puis retirer `scripts/reseau_ssh` comme publicateur
- requalifier `step1b`
- garder `reseau_ssh_step2` comme detail interne seulement

## Preparation Git retenue
- lot repo-side : prepares seulement, sans execution Git
- lot machine-side : separe

## Target
1 module canonique par famille.
