---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01_INVENTORY
doc_type: chantier_inventory
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01
status: complete
lifecycle_stage: inventory
topic_keys:
  - opt-trading
  - reseau_ssh
  - modules
  - inventory
  - canonical
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/status/reseau_ssh_canonique.md
  - modules/reseau_ssh/README.md
  - modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/README.md
  - modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/README.md
  - scripts/reseau_ssh/README.md
  - _archive/legacy_modules/reseau_ssh_step1/README.md
---

# Inventaire et classement initial

## Lecture brute

### 1. `modules/reseau_ssh`
- nature : facade canonique top-level
- contenu : wrappers top-level specialises, helper de resolution de path, README canonique
- role : proprietaire actuel de la famille cote `modules/`

### 2. `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2`
- nature : implementation interne historique `step2`
- contenu : WireGuard, firewall, inventory recent, templates, docs techniques
- role : couche interne utile, non survivant top-level

### 3. `modules/reseau_ssh_step1b`
- nature : baseline hosts / ssh config / hostname
- contenu : scripts Linux/Windows, templates, inventory propre
- role : prerequis intermediaire encore garde pour compat

### 4. `scripts/reseau_ssh`
- nature : runtime machine-side encore actif
- contenu : installateur des alias courts, backend operateur historique
- role : compat runtime temporaire, non canon durable

### 5. `_archive/legacy_modules/reseau_ssh_step1`
- nature : ancien occupant top-level archive
- contenu : step1 documentaire et scripts pre-step
- role : archive backup

## Classement retenu
| Surface | Classement retenu | Justification |
| --- | --- | --- |
| `modules/reseau_ssh` | `canonique` | proprietaire top-level de la famille apres promotion repo-side |
| `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2` | `utile_prouve` | implementation interne WG/firewall encore necessaire |
| `modules/reseau_ssh_step1b` | `compat_temporaire` | baseline utile non absorbee ni retiree |
| `scripts/reseau_ssh` | `compat_temporaire` | publicateur actuel des alias courts, a retirer de la publication |
| `_archive/legacy_modules/reseau_ssh_step1` | `archive_backup` | ancien occupant top-level deja sorti des flux actifs |

## Point dur restant
La promesse `1 module canonique par famille` est satisfaite cote repo-side.

Elle ne l'est pas encore cote runtime machine-side tant que :
- `menu-reseau_ssh`
- `cmd-reseau_ssh`
- `sanity-reseau_ssh`

restent installes depuis `scripts/reseau_ssh`.

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
