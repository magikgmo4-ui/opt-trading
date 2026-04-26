---
doc_id: GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_FLATTENING_01_PLAN
doc_type: chantier_plan
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_FLATTENING_01
status: closed
lifecycle_stage: closeout
topic_keys:
  - opt-trading
  - reseau_ssh
  - plan
surface: modules
source_kind: canonical
updated_at: 2026-04-26
---

# Plan

1. Renommer l'ancien sous-arbre `reseau_ssh_step2` en payload interne `wireguard/`.
2. Absorber la logique WireGuard dans `modules/reseau_ssh/scripts/_reseau_ssh_wireguard.sh`.
3. Rebrancher `cmd.sh`, `menu.sh`, `sanity_check.sh`, `_reseau_ssh_common.sh`.
4. Internaliser les artefacts baseline utiles sous `modules/reseau_ssh/baseline/`.
5. Retirer les scripts internes `wireguard/scripts/*` devenus redondants.
6. Réaligner la documentation de closeout et de statut.
7. Revalider repo-side et machine-side.

## Target
1 module canonique par famille.
