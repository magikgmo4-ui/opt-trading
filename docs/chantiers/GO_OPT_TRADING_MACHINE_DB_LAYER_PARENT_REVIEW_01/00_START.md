# GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01

## Contexte
- Reprise apres le PASS du GO `GO_OPT_TRADING_DOC_OPS_CHILD_POST_MATRIX_REMAINING_PARENT_ARBITRATION_01`.
- Base canonique de travail : `sot/mainline`.
- Commit de closeout connu du GO precedent : `e124588` (`docs: arbitrate remaining parents after matrix closeout`).

## Pourquoi db-layer est prioritaire
- `db-layer` reste la machine runtime/app immediate a clarifier avant toute ouverture reelle de `admin-trading`.
- `db-layer` est l'hote actuel confirme pour les surfaces `LocalCMS` et `OpenClaw`.
- L'objectif reste de garder idealement un chantier principal ouvert par machine.

## Invariants
- `db-layer` est une machine d'execution, pas le parent projet de `LocalCMS`.
- `db-layer` est une machine d'execution, pas le parent runtime de `OpenClaw`.
- Les parents ouverts restent distincts :
  - `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01`
  - `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01`
- Aucun changement runtime ou code applicatif n'est realise dans ce GO.

## RISKS

- À qualifier.
