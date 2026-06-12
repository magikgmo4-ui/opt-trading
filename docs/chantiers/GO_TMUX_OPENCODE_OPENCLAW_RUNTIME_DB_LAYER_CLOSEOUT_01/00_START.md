# GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_CLOSEOUT_01

## Contexte
- Reprise apres le PASS de `GO_OPENCLAW_STATE_DIR_REPAIR_10`.
- Base canonique : `sot/mainline`.
- Commit connu du repair : `4017e9f` (`docs: capture openclaw gateway owner-session repair`).

## Pourquoi ce closeout existe
- Le cycle `db-layer -> review runtime -> repair local` est suffisamment etabli pour etre fige proprement.
- L'objectif de ce GO est de clore la sequence locale `OpenClaw` sur `db-layer` avant de repasser sur `LocalCMS`.
- Ce closeout ne ferme pas le parent runtime `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` ; il ferme seulement le cycle borne `db-layer`.

## Invariants
- `OpenClaw` reste porte par le parent runtime `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01`.
- `db-layer` reste seulement l'hote actuel de `OpenClaw`.
- `admin-trading` reste differe.
- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` reste une reference future non activee.
- Aucun changement runtime n'est effectue dans ce GO.

## RISKS

- À qualifier.
