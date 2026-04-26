---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_BASELINE_ABSORPTION_01_AUDIT
doc_type: chantier_inventory
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_BASELINE_ABSORPTION_01
status: complete
lifecycle_stage: inventory
topic_keys:
  - opt-trading
  - reseau_ssh
  - step1b
  - baseline
  - audit
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/scripts/apply_linux.sh
  - modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/scripts/apply_hostname_linux.sh
  - modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/scripts/sanity_check.sh
---

# Audit capacites step1b

## Capacites encore publiees

Les seules capacités `step1b` encore publiées via le canonique sont :
- `baseline-dry-run`
- `baseline-apply`
- `baseline-hostname`
- `baseline-sanity`
- `baseline-show-hosts`
- `baseline-show-ssh`

## Capacites non publiees

Restent non publiées par le canonique :
- `install_shortcuts_linux.sh`
- `make_keys_bundle_admin.sh`
- `windows/apply_cursor_ai.ps1`

## Conclusion

Le coeur utile publie est borne et absorbable dans `modules/reseau_ssh`.

Le reste de `step1b` ressemble a :
- support legacy non publie
- aide de migration / bootstrap historique
- candidat d'archive apres absorption des commandes `baseline-*`

## Target
1 module canonique par famille.
