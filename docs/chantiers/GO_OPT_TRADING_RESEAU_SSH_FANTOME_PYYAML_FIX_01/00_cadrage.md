---
doc_id: GO_OPT_TRADING_RESEAU_SSH_FANTOME_PYYAML_FIX_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_FANTOME_PYYAML_FIX_01
status: open
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - fantome
  - pyyaml
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_STEP1B_MACHINE_CLEANUP_01/03_step_02_execution_cleanup.md
  - docs/status/reseau_ssh_canonique.md
---

# GO_OPT_TRADING_RESEAU_SSH_FANTOME_PYYAML_FIX_01 - Cadrage

## Objet

Corriger le gap d'environnement Python sur `fantome` qui bloquait le deep sanity complet de `reseau_ssh`.

## Etat de depart

- `fantome` passait `baseline-*`
- `fantome` passait `sanity-reseau_ssh` seulement avec `RESEAU_SSH_SKIP_DEEP_SANITY=1`
- cause prouvee : `ModuleNotFoundError: No module named 'yaml'`

## Cible

- installer `PyYAML` pour `/usr/bin/python3`
- revalider `sanity-reseau_ssh` sans contournement

## Target
1 module canonique par famille.
