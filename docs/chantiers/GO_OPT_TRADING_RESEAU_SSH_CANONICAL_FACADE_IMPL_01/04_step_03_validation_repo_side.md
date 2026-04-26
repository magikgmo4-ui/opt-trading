---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_FACADE_IMPL_01_STEP_03_VALIDATION
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
  - validation
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/scripts/sanity_check.sh
---

# Step 03 - validation repo-side

## Verifications attendues
- `bash -n` sur la facade top-level
- `bash -n` sur l'implementation interne et les compatibilites touchees
- `modules/reseau_ssh/scripts/cmd.sh info`
- `modules/reseau_ssh/scripts/cmd.sh readme`
- `modules/reseau_ssh/scripts/cmd.sh baseline-show-hosts`
- `modules/reseau_ssh/scripts/cmd.sh baseline-show-ssh`
- `RESEAU_SSH_SKIP_DEEP_SANITY=1 modules/reseau_ssh/scripts/sanity_check.sh`

## Limite connue
Le test via vrai symlink Windows reste a rejouer dans un environnement qui autorise la creation du lien.

## Point de vigilance
La sanity profonde delegue encore vers le backend compat si present.

C'est voulu tant que le lot machine-side n'est pas execute.

## Target
1 module canonique par famille.
