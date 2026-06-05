# Start

## Contexte post cycles amont

- reprise sur `go/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_CLOSEOUT_01`
- base canonique : `origin/sot/mainline`
- closeouts amont relus :
  - `GO_OPT_TRADING_DOC_OPS_CHILD_POST_MATRIX_REMAINING_PARENT_ARBITRATION_01`
  - `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01` via `6519f36`
  - `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_CLOSEOUT_01` via `fcabd3d`
  - `GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01` via `8225caa`

## Etat etabli retenu

- `db-layer` reste la machine d'execution reelle la plus validee du cycle recent
- `OpenClaw` gateway est deja clos sur `db-layer` sans reouverture runtime
- `LocalCMS` reste un parent projet consumer, distinct du parent machine `db-layer`
- `reseau_ssh` reste un chantier transverse multi-machine
- objectif organisationnel conserve : idealement `1` chantier principal ouvert par machine

## Objectif du closeout

- verifier les alias SSH utiles
- verifier les hostnames repondus
- verifier les chemins repo reels
- distinguer `modules/reseau_ssh`, `modules/reseau_ssh_step1b`, la surface `compat` et `scripts/reseau_ssh`
- produire un verdict `PASS` / `GAP` sans modifier le runtime

## Regles de ce lot

- lot documentaire minimal
- probes SSH strictement read-only
- pas de patch runtime applicatif
- pas de changement `OpenClaw`, `LocalCMS` ou `admin-trading`
- pas d'exposition de cle SSH, token, secret ou IP sensible non necessaire
- si une divergence existe, la documenter avant toute correction future

## Nature du chantier

- `reseau_ssh` reste transverse
- ce closeout ne cree pas un nouveau parent machine
- ce closeout fige l'etat physique constate pour preparer la reprise suivante

## RISKS

- À qualifier.
