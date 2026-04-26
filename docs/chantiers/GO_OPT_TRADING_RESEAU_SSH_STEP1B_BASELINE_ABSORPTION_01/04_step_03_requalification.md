---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_BASELINE_ABSORPTION_01_REQUALIFICATION
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_BASELINE_ABSORPTION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - step1b
  - archive_candidate
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh_step1b/README.md
  - modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/README.md
  - docs/status/reseau_ssh_canonique.md
---

# Step 03 - requalification

## Decision

`reseau_ssh_step1b` n'est plus une transition active pour les commandes publiees par le canonique.

Nouveau statut retenu :
- `archive_candidate`

## Motif

- le canonique `modules/reseau_ssh` porte maintenant les commandes `baseline-*`
- `step1b` n'est plus appele par le canonique
- les scripts restants de `step1b` sont non publies ou legacy

## Target
1 module canonique par famille.
