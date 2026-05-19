---
doc_id: OPT_TRADING_ARCHIVE_RESEAU_SSH_ROOT_WRAPPERS_LEGACY
doc_type: archive_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
status: archived
lifecycle_stage: archive
updated_at: 2026-04-25
---

# reseau_ssh_root_wrappers_legacy

Contient les anciens wrappers racine :
- `reseau_ssh_cmd.sh`
- `reseau_ssh_menu.sh`

Motif d'archivage :
- plus aucun role canonique
- implementation locale cassée dans le repo courant
- alias courts machine-side déjà repointés vers `modules/reseau_ssh/scripts/*`

Archive appliquée dans le lot :
- `GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01`

## Target
1 module canonique par famille.
