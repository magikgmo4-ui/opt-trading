---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01_CAPACITY_MATRIX
doc_type: chantier_inventory
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_CONVERGENCE_TO_CANONICAL_01
status: complete
lifecycle_stage: inventory
topic_keys:
  - opt-trading
  - reseau_ssh
  - runtime
  - capabilities
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/reseau_ssh_cmd.sh
  - modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/scripts/reseau_ssh_cmd.sh
  - scripts/reseau_ssh/reseau_ssh_cmd.sh
---

# Matrice des capacites

## `modules/reseau_ssh`
Capacites de facade :
- `info`
- `readme`
- `menu`
- `sanity`
- commandes WG/firewall deleguees
- commandes `baseline-*` deleguees

Role :
- facade canonique repo-side

## `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2`
Capacites propres :
- `wg-install`
- `wg-genkeys`
- `wg-showpub`
- `wg-render`
- `wg-render-windows`
- `wg-apply`
- `wg-up`
- `wg-down`
- `wg-status`
- `fw-dry-run`
- `fw-apply`

Role :
- implementation interne WireGuard / firewall

## `modules/reseau_ssh_step1b`
Capacites propres :
- `dry-run`
- `apply`
- `hostname`
- `sanity`
- `show-hosts`
- `show-ssh`

Role :
- baseline hosts / ssh config / hostname

## `scripts/reseau_ssh`
Capacites runtime publiees :
- `sanity`
- `bootstrap`
- `ssh-hardening-safe`
- `ssh-lockdown`
- `wg-server-init`
- `wg-client-init`
- `wg-add-peer`
- `wg-up`
- `wg-down`
- `wg-show`

Role :
- backend runtime historique
- publicateur machine-side actuel des alias courts

## Conclusion
Le canonique final ne sera pleinement unique qu'une fois :
- les alias courts republies depuis `modules/reseau_ssh`
- la baseline `step1b` absorbee ou explicitement retiree

## Target
1 module canonique par famille.
