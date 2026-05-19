# GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01

## Contexte
- Reprise apres le PASS du closeout `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_CLOSEOUT_01`.
- Base canonique : `sot/mainline`.
- Commit de closeout `OpenClaw/db-layer` connu : `fcabd3d` (`docs: close OpenClaw runtime db-layer cycle`).

## Pourquoi LocalCMS vient maintenant
- `db-layer` reste la machine prioritaire actuelle.
- Le cycle `OpenClaw` sur `db-layer` est clos et sorti du perimetre actif de ce GO.
- Le prochain besoin documentaire est de realigner `LocalCMS consumer` avec `db-layer` comme machine d'execution reelle.

## Invariants
- `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` reste le parent projet.
- `db-layer` reste seulement le parent machine / hote d'execution.
- `opt-trading` reste le producer canonique.
- Aucun changement runtime n'est realise dans ce GO.
