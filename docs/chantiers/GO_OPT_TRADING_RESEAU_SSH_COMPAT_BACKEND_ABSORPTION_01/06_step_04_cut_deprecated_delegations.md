---
doc_id: GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01_STEP_04_CUT_DEPRECATED
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
  - deprecated
  - wireguard
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/cmd.sh
  - scripts/reseau_ssh/reseau_ssh_cmd.sh
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01/01_matrice_commandes.md
---

# Step 04 - cut deprecated delegations

## Execution

La facade canonique `modules/reseau_ssh/scripts/cmd.sh` ne delegue plus :
- `wg-server-init`
- `wg-client-init`
- `wg-add-peer`

Ces commandes retournent maintenant une erreur explicite et renvoient vers :
- le workflow canonique `wg-genkeys` -> `wg-render` -> `wg-apply` -> `wg-up` -> `wg-status`
- ou un appel legacy explicite au backend `scripts/reseau_ssh/reseau_ssh_cmd.sh`

## Resultat

`scripts/reseau_ssh` ne reste plus requis via la facade canonique que pour :
- `bootstrap`
- `ssh-hardening-safe`
- `ssh-lockdown`

Le backend compat n'est donc plus `compat_active_backend`.
Le statut retenu passe a :
- `keep-transition`

## Validation

- `bash -n modules/reseau_ssh/scripts/cmd.sh` : `SYNTAX_OK`
- commande d'aide relue pour verifier le retrait des trois commandes deprecated

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
