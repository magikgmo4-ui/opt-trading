---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01_CADRAGE
doc_type: chantier_child
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - reseau_ssh
  - modules
  - canonical
  - archive
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01/01_grille_decision.md
  - docs/chantiers/GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01/03_priorisation_familles.md
  - docs/status/reseau_ssh_canonique.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md
  - modules/reseau_ssh/README.md
  - modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/README.md
  - modules/reseau_ssh_step1b/README.md
  - scripts/reseau_ssh/README.md
  - _archive/legacy_modules/reseau_ssh_step1/README.md
---

# GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01

## Objet
Fixer la lecture canonique de la famille `reseau_ssh*` dans la doctrine :
- `canonique`
- `compat_temporaire`
- `legacy_fige`
- `archive_backup`

## Portee
- `modules/reseau_ssh`
- `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2`
- `modules/reseau_ssh_step1b`
- `scripts/reseau_ssh`
- `_archive/legacy_modules/reseau_ssh_step1`

## Etat reel pris comme base
Le move physique principal est deja execute :
- l'ancien occupant legacy `modules/reseau_ssh` est sorti vers `_archive/legacy_modules/reseau_ssh_step1`
- l'ancienne base `modules/reseau_ssh_step2` a ete promue en `modules/reseau_ssh`

Le present lot ne redecide donc pas la cible.

Il fige la qualification de famille et son point de reprise.

## Sortie attendue
- `reseau_ssh` = canonique
- `reseau_ssh_step2` = implementation interne utile
- `reseau_ssh_step1b` = compat temporaire
- `scripts/reseau_ssh` = compat runtime temporaire
- `reseau_ssh_step1` = archive backup

## Point de reprise
Le blocage principal n'est plus le nom du module.

Le blocage principal est le runtime machine-side :
- alias courts encore publies depuis `scripts/reseau_ssh`
- baseline `step1b` encore gardee en compat

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
