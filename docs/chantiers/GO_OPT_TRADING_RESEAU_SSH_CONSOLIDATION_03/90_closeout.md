---
doc_id: OPT_TRADING_GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03_CLOSEOUT
doc_type: chantier_closeout
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03
status: closed
lifecycle_stage: closeout
topic_keys:
  - opt-trading
  - reseau_ssh
  - consolidation
  - closeout
surface: modules
source_kind: canonical
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_STEP1B_ARCHIVE_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_STEP1B_MACHINE_CLEANUP_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_FANTOME_PYYAML_FIX_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_STEP2_COMPAT_RETIREMENT_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_FLATTENING_01/90_closeout.md
  - docs/status/reseau_ssh_canonique.md
---

# GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 — Closeout

## Resultat final

La famille `reseau_ssh*` est closee autour d'une seule surface active :

- module top-level actif unique : `modules/reseau_ssh`
- logique publiee unique : `modules/reseau_ssh/scripts/*`
- payload WireGuard interne : `modules/reseau_ssh/wireguard/*`
- payload baseline interne : `modules/reseau_ssh/baseline/*`
- interface publiee unique : `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh`

## Etat archive

- `step1` archive repo-side
- `step1b` archive machine-side ; capacites utiles absorbees dans `modules/reseau_ssh/baseline/*`
- runtime legacy `scripts/reseau_ssh` archive repo-side
- compat suffixee `step2` retiree du registre, des machines et archivee machine-side
- ancien backend `step2` flatten dans `modules/reseau_ssh/wireguard/*` ; plus aucun sous-module executable separe

## Validation finale

- `db-layer` : PASS
- `admin-trading` : PASS
- `student` : PASS
- `fantome` : PASS

## Decision

Le stream `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` est clos.

## Target
1 module canonique par famille.
