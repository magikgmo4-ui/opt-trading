---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01_30_EXECUTION_GATES
doc_type: chantier/gates
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01
status: active
scope: doc-only
---

# 30_EXECUTION_GATES

## Gates avant action machine

1. Confirmer que le realignement vise uniquement `admin-trading`.
2. Confirmer qu'aucun besoin `db-layer` / OpenClaw n'entre dans la manoeuvre.
3. Qualifier la strategie Git:
   - switch sur `sot/mainline` local machine
   - fetch
   - reset de travail interdit sans demande explicite
   - creation d'une branche de travail explicite si necessaire
4. Documenter toute divergence locale avant correction.

## Gates de refus

- ne pas agir si le repo n'est plus propre
- ne pas agir si la branche locale porte des changements non documentes
- ne pas agir si le realignement exigerait une modification runtime
- ne pas agir si la manoeuvre implique `db-layer`

## Output attendu du lot suivant

- etat Git final de `admin-trading`
- branche de depart canonique pour la suite `tmux-ide`
- preuve que la machine est prete pour `tmux-ide` sans toucher au runtime

## RISKS

- À qualifier.
