---
doc_id: GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01_PLAN
doc_type: chantier_execution_plan
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01
status: open
lifecycle_stage: execution_plan
topic_keys:
  - opt-trading
  - reseau_ssh
  - compat
  - backend
  - plan
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01/01_matrice_commandes.md
---

# Plan operationnel step-by-step

## Step 01 - matrice de commandes
- statut : complete
- objectif : fixer exactement ce que la facade canonique porte encore via le backend compat

## Step 02 - arbitrage commande par commande
- statut : complete
- objectif : classer chaque commande `scripts/reseau_ssh` en :
  - `absorb`
  - `deprecate`
  - `keep-transition`

## Step 03 - plan de patch repo-side
- statut : complete
- objectif : definir les edits minimaux sur `modules/reseau_ssh/scripts/*`

## Step 04 - retrait des delegations deprecated
- statut : complete
- objectif : couper `wg-server-init`, `wg-client-init`, `wg-add-peer` de la facade canonique

## Step 05 - preparation Git
- statut : complete
- objectif : preparer commits et PR sans execution

## Point de reprise

Le prochain step utile est un lot d'execution borne :
- traiter les commandes `keep-transition` restantes :
  - `bootstrap`
  - `ssh-hardening-safe`
  - `ssh-lockdown`
- puis requalifier `scripts/reseau_ssh` de `keep-transition` vers `rollback_only` ou `archive_backup`

## Target
1 module canonique par famille.
