# GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_REVIEW_01

## Contexte
- Reprise apres le PASS du GO `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01`.
- Base canonique de travail : `sot/mainline`.
- Commit de closeout connu du GO precedent : `6519f36` (`docs: review db-layer machine parent`).

## Pourquoi ce GO vient maintenant
- Le GO precedent a etabli que `db-layer` est la machine prioritaire actuelle.
- Il a aussi etabli que `OpenClaw` est installe sur `db-layer`, mais que le gateway et `127.0.0.1:18789` etaient arretes au moment du controle.
- Le prochain pas logique est donc une revue runtime `OpenClaw` borne, en lecture seule, avant tout GO d'application.

## Invariants
- `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` reste le parent runtime existant.
- `db-layer` reste seulement l'hote actuel d'execution.
- `admin-trading` reste differe pour l'integration trading future.
- Aucun changement runtime n'est autorise dans ce GO.

## RISKS

- À qualifier.
