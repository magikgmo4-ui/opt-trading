---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01_HARD_POINTS
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - modules
  - blockers
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/status/reseau_ssh_canonique.md
  - scripts/reseau_ssh/README_RUNTIME_STATUS.md
  - registry/modules_registry.yaml
  - registry/wrappers_registry.yaml
---

# Points durs

## 1. Le canonique repo-side existe, pas encore le runtime canonique machine-side
`modules/reseau_ssh` est le bon proprietaire top-level dans le repo.

Mais les alias courts installes sur machine restent encore publies depuis `scripts/reseau_ssh`.

## 2. `step1b` garde une baseline utile
La baseline hosts / ssh config / hostname reste utile tant qu'elle n'est ni absorbee, ni explicitement retiree.

Consequence :
- `step1b` reste `compat_temporaire`
- il ne peut pas encore sortir en archive

## 3. `reseau_ssh_step2` doit rester une implementation interne, pas un deuxieme survivant
La couche nested `reseau_ssh_step2` reste utile.

Mais elle ne doit plus etre lue comme un candidat de nom canonique final.

## 4. Le registre est aligne repo-side, pas encore prouve machine-side
`registry/modules_registry.yaml` et `registry/wrappers_registry.yaml` sont maintenant prets pour `reseau_ssh`.

Le repointage reel des alias courts reste a prouver sur les machines cibles.

## Decision de travail
Le prochain lot utile n'est plus un debat de classification.

Le prochain lot utile est :
- alignement repo-side final
- puis repointage machine-side separe

## Target
1 module canonique par famille.
