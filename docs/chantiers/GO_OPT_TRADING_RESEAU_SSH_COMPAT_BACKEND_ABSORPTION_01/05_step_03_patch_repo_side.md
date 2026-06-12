---
doc_id: GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01_STEP_03_PATCH
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - compat
  - patch
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01/04_step_02_arbitrage_commandes.md
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/scripts/sanity_check.sh
---

# Step 03 - patch repo-side

## Patch applique

### `modules/reseau_ssh/scripts/sanity_check.sh`
- le `deep sanity` est maintenant porte par la facade canonique
- la delegation automatique a `scripts/reseau_ssh/sanity_reseau_ssh.sh` est retiree

### `modules/reseau_ssh/scripts/cmd.sh`
- `wg-show` devient un alias canonique vers `wg-status`
- `wg-server-init`, `wg-client-init`, `wg-add-peer` restent alors supportees temporairement mais marquees `deprecated`
- `bootstrap`, `ssh-hardening-safe`, `ssh-lockdown` restent deleguees en `keep-transition`

## Resultat

Le backend `scripts/reseau_ssh` reste encore requis, mais avec une dependance reduite :
- le `deep sanity` n'en depend plus
- `wg-show` n'en depend plus
- il reste encore requis pour :
  - `bootstrap`
  - `ssh-hardening-safe`
  - `ssh-lockdown`

La coupe des trois commandes WireGuard legacy est traitee ensuite par le `Step 04`.

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
