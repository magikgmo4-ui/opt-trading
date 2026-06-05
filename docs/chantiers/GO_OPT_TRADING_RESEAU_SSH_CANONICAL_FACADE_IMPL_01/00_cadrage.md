---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01_CADRAGE
doc_type: chantier_child
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - reseau_ssh
  - facade
  - canonical
  - runtime
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01/04_step_03_strategie_absorption.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01/05_step_04_plan_bascule_alias_courts.md
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/scripts/menu.sh
  - modules/reseau_ssh/scripts/sanity_check.sh
---

# GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01

## Objet
Tracer le lot repo-side qui a specialise la facade canonique `reseau_ssh`.

## But
Documenter une facade top-level qui :
- resout correctement son path reel
- expose une surface `reseau_ssh` specialisee
- delegue vers l'implementation interne `reseau_ssh_step2`
- garde les compatibilites `step1b` et `scripts/reseau_ssh` sous controle

## Portee
- `modules/reseau_ssh/scripts/*`
- `modules/reseau_ssh/README.md`
- documentation de lot

## Hors-scope
- repointage machine-side des alias courts
- retrait de `step1b`
- retrait de `scripts/reseau_ssh`
- execution Git

## Sortie attendue
- facade top-level specialisee
- validation repo-side
- preparation des commits/PR sans execution

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
