# Start

## Contexte post socle recent

- reprise sur `go/GO_OPT_TRADING_MULTI_AGENTS_CURSOR_AI_PARENT_ALIGNMENT_01`
- base canonique : `origin/sot/mainline`
- closeouts amont relus ou recroises :
  - `GO_OPT_TRADING_DOC_OPS_CHILD_POST_MATRIX_REMAINING_PARENT_ARBITRATION_01` via `e124588`
  - `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01`
  - `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_CLOSEOUT_01`
  - `GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01` via `8225caa`
  - `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_CLOSEOUT_01` via `ec23948`

## Pourquoi cursor-ai vient maintenant

- `db-layer` est deja consolide comme machine d'execution actuelle
- `OpenClaw` reste borne et clos sur `db-layer`
- `LocalCMS` reste parent projet consumer avec `db-layer` comme machine d'execution
- `reseau_ssh` est passe `PASS` pour les machines Linux prioritaires
- le prochain besoin machine-first logique est donc le poste Windows local `cursor-ai`, non comme runtime applicatif, mais comme poste d'orchestration multi-agents

## Role retenu de cursor-ai

- poste Windows local
- point de controle humain + agents + IDE
- surface Git principale pour branches, prompts, lecture repo et continuité locale
- lieu naturel de pilotage `workflow_ai` / Prompt Factory / arbitrage de branches

## Regles de ce lot

- patch strictement documentaire
- aucun changement runtime applicatif
- aucun changement `OpenClaw`
- aucun changement `LocalCMS`
- aucun changement `admin-trading`
- aucun secret expose
- aucun parent machine `cursor-ai` cree sans preuve supplementaire

## Decision directrice

- `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` reste le parent principal de travail pour `cursor-ai`
- ce lot verifie s'il suffit a couvrir le besoin courant
- ce lot ne deplace ni `cursor-ai` vers `db-layer`, ni `OpenClaw` vers `cursor-ai`
