---
doc_id: GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_FLATTENING_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_FLATTENING_01
status: closed
lifecycle_stage: closeout
topic_keys:
  - opt-trading
  - reseau_ssh
  - flattening
  - physical
surface: modules
source_kind: canonical
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/90_closeout.md
  - docs/status/reseau_ssh_canonique.md
---

# Cadrage

Objectif du lot :
- absorber la logique exécutable `step2` dans `modules/reseau_ssh/scripts/*`
- supprimer la dépendance à un sous-arbre `modules/.../reseau_ssh_step2`
- conserver les artefacts utiles comme payloads internes (`wireguard`, `baseline`)
- revalider la surface publiée sur les 4 machines

## Target
1 module canonique par famille.
