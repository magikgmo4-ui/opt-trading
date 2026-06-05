---
doc_id: GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01_COMMAND_MATRIX
doc_type: chantier_inventory
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01
status: open
lifecycle_stage: inventory
topic_keys:
  - opt-trading
  - reseau_ssh
  - compat
  - commands
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/reseau_ssh_cmd.sh
  - scripts/reseau_ssh/reseau_ssh_cmd.sh
---

# Matrice de commandes

| Commande facade `cmd-reseau_ssh` | Backend actuel | Classe proposee |
| --- | --- | --- |
| `info`, `path`, `readme`, `ls`, `menu`, `sanity` | facade canonique | `canonique` |
| `wg-install`, `wg-genkeys`, `wg-showpub`, `wg-render`, `wg-render-windows`, `wg-apply`, `wg-up`, `wg-down`, `wg-status`, `fw-dry-run`, `fw-apply` | implementation nested `step2` | `canonique_interne` |
| `bootstrap` | `scripts/reseau_ssh` | `keep-transition` |
| `ssh-hardening-safe` | `scripts/reseau_ssh` | `keep-transition` |
| `ssh-lockdown` | `scripts/reseau_ssh` | `keep-transition` |
| `wg-server-init` | backend legacy explicite seulement | `deprecated_cut_from_facade` |
| `wg-client-init` | backend legacy explicite seulement | `deprecated_cut_from_facade` |
| `wg-add-peer` | backend legacy explicite seulement | `deprecated_cut_from_facade` |
| `wg-show` | alias canonique vers `wg-status` | `absorbe` |
| `baseline-*` | `modules/reseau_ssh_step1b` | `transition` |

## Point dur

Le `sanity` profond a maintenant ete absorbe dans la facade canonique.

Le backend compat reste encore requis seulement pour :
- `bootstrap`
- `ssh-hardening-safe`
- `ssh-lockdown`

Les commandes suivantes ont ete retirees de la facade canonique et ne restent accessibles qu'en appel legacy explicite :
- `wg-server-init`
- `wg-client-init`
- `wg-add-peer`

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
