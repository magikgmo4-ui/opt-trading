---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01_PLAN
doc_type: chantier_execution_plan
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01
status: open
lifecycle_stage: execution_plan
topic_keys:
  - opt-trading
  - reseau_ssh
  - facade
  - runtime
  - plan
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/01_plan_operationnel_step_by_step.md
---

# Plan operationnel step-by-step

## Step 01 - surface autorisee
- statut : complete
- objectif : borner les fichiers code/doc du lot repo-side

## Step 02 - implementation facade
- statut : complete
- objectif : specialiser `modules/reseau_ssh/scripts/*` avec delegation interne et path fix

## Step 03 - verification repo-side
- statut : complete
- objectif : verifier la resolution de path et la delegation sur le nouveau chemin canonique

## Step 04 - preparation commits et PR
- statut : complete
- objectif : preparer le decoupage Git sans execution

## Point de reprise
Le lot facade est termine.

Le lot repo-side complementaire est :
- `GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01`

Puis :
- lot machine-side separe pour les alias courts

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
