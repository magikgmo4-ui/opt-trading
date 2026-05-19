---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01_STEP_02_IMPL
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - facade
  - implementation
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/_reseau_ssh_common.sh
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/scripts/menu.sh
  - modules/reseau_ssh/scripts/sanity_check.sh
  - modules/reseau_ssh/README.md
---

# Step 02 - implementation facade

## Changement principal
La surface top-level `modules/reseau_ssh/scripts/*` n'est plus une enveloppe generique.

Elle devient une facade specialisee `reseau_ssh`.

## Patch applique

### Helper commun
Ajout :
- `modules/reseau_ssh/scripts/_reseau_ssh_common.sh`

Role :
- resolution du chemin reel d'entree
- calcul des chemins du module canonique
- calcul des chemins vers :
  - implementation interne `reseau_ssh_step2`
  - backend compat `scripts/reseau_ssh`
  - baseline compat `step1b`

### `cmd.sh`
La facade :
- expose `info`, `path`, `readme`, `ls`, `menu`, `sanity`
- delegue WG/firewall vers l'implementation interne
- delegue certaines commandes historiques vers `scripts/reseau_ssh`
- expose `step1b` sous commandes `baseline-*`

### `menu.sh`
Le menu top-level donne acces a :
- sanity canonique
- menu de l'implementation interne
- menu backend compat
- operations baseline `step1b`
- information de path et README

### `sanity_check.sh`
La sanity top-level :
- verifie la facade locale
- peut etre forcee en preflight repo-side avec `RESEAU_SSH_SKIP_DEEP_SANITY=1`
- delegue sinon vers une sanity plus profonde

## Target
1 module canonique par famille.
