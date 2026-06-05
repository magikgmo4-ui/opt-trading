---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01_PLAN
doc_type: chantier_execution_plan
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01
status: open
lifecycle_stage: execution_plan
topic_keys:
  - opt-trading
  - reseau_ssh
  - compat
  - retirement
  - plan
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/01_inventaire_surfaces_compat.md
---

# Plan operationnel step-by-step

## Step 01 - realignement du lot
- statut : complete
- objectif : remettre le GO de compat en coherence avec le canonique actuel `modules/reseau_ssh`

## Step 02 - garde-fou sur l'installeur legacy
- statut : complete
- objectif : empecher que `scripts/reseau_ssh/install_reseau_ssh.sh` republie les alias courts vers le backend legacy quand le canonique est disponible

## Step 03 - qualification des wrappers racine
- statut : complete
- objectif : prouver s'il reste des callers repo-side ou usages operatoriels sur `scripts/reseau_ssh_cmd.sh` et `scripts/reseau_ssh_menu.sh`

## Step 04 - arbitrage de sortie du dossier compat
- statut : complete
- objectif : decider entre :
  - maintien `compat_active_backend`
  - puis maintien `rollback_only`
  - ou reclassement `archive_backup`

## Step 05 - execution wrappers racine
- statut : complete
- objectif : sortir les wrappers racine historiques du flux actif par archivage borne

## Step 06 - preparation Git
- statut : complete
- objectif : preparer le decoupage des commits et la PR sans lancer de commit ni de push

## Step 07 - blocage backend compat
- statut : complete
- objectif : prouver si `scripts/reseau_ssh` peut deja sortir du flux actif ou si la facade canonique en depend encore

## Point de reprise

La prochaine action utile est un lot d'execution separe :
- absorber ou deprecated les commandes encore deleguees a `scripts/reseau_ssh`
- puis decider si `scripts/reseau_ssh` peut passer de `compat_active_backend` a `rollback_only`, puis `archive_backup`
- puis qualifier la sortie progressive de `reseau_ssh_step1b`

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
