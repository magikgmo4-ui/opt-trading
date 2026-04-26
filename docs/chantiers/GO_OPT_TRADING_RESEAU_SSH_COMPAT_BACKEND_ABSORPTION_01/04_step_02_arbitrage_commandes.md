---
doc_id: GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01_STEP_02_COMMAND_ARBITRATION
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
  - commands
  - arbitration
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_COMPAT_BACKEND_ABSORPTION_01/01_matrice_commandes.md
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/scripts/sanity_check.sh
---

# Step 02 - arbitrage commande par commande

## Absorb

### `sanity` profond
- decision : `absorb`
- motif : le `sanity` canonique ne doit plus dependre du backend compat pour sa lecture systeme de base

### `wg-show`
- decision : `absorb`
- motif : equivalent fonctionnel defensable de `wg-status` dans la couche step2

## Deprecate

### `wg-server-init`
- decision : `deprecate`
- remplacement vise :
  - `wg-genkeys`
  - `wg-render`
  - `wg-apply`
  - `wg-up`
  - `wg-status`
- motif : workflow direct `wg0.conf` legacy, non aligne avec l'inventaire et le rendu step2

### `wg-client-init`
- decision : `deprecate`
- remplacement vise :
  - `wg-genkeys`
  - `wg-render`
  - `wg-apply`
  - `wg-up`
  - `wg-status`
- motif : meme raison que `wg-server-init`

### `wg-add-peer`
- decision : `deprecate`
- remplacement vise :
  - gestion des peers via inventaire et pubkeys dans la couche step2
- motif : ecriture imperative legacy dans `wg0.conf`

## Keep-transition

### `bootstrap`
- decision : `keep-transition`
- motif : pas de remplacement canonique strict aujourd'hui ; fonction encore utile mais trop invasive pour absorption immediate

### `ssh-hardening-safe`
- decision : `keep-transition`
- motif : utile, mais releve d'un lot de durcissement explicite plutot que d'une absorption opportuniste

### `ssh-lockdown`
- decision : `keep-transition`
- motif : operation sensible ; pas d'absorption sans runbook de securite dedie

## Effet retenu pour cette passe

On implemente maintenant seulement :
- absorption du `deep sanity`
- absorption de `wg-show` vers `wg-status`
- marquage deprecie / transition dans la facade canonique pour le reste

## Target
1 module canonique par famille.
