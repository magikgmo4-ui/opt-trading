# Start

## Contexte post socle recent

- reprise sur `go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`
- base canonique : `origin/sot/mainline`
- closeouts amont relus ou recroises :
  - `GO_OPT_TRADING_DOC_OPS_CHILD_POST_MATRIX_REMAINING_PARENT_ARBITRATION_01` via `e124588`
  - `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_CLOSEOUT_01` via `ec23948`
  - `GO_OPT_TRADING_MULTI_AGENTS_CURSOR_AI_PARENT_ALIGNMENT_01` via `7ef370d`

## Pourquoi AI Team / fantome vient maintenant

- `db-layer` est deja consolide pour `OpenClaw` et `LocalCMS`
- `reseau_ssh` est passe `PASS` et `fantome` repond en lecture seule
- `cursor-ai` est deja aligne comme poste Windows local d'orchestration multi-agents
- la machine suivante logique pour maintenir idealement `1` chantier principal par machine est donc `fantome`

## Rappel sur strict workers

- `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` existe deja comme surface documentaire et `DRAFT_ONLY`
- le besoin de ce lot est de le consolider sous `AI Team` pour la carte machine `fantome`
- ce lot ne transforme pas `strict workers` en parent machine autonome

## Role retenu de ce GO

- confirmer que `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` reste le parent principal
- documenter `fantome` comme machine candidate `AI Team / strict workers`
- clarifier la frontiere `cursor-ai` orchestration vs `fantome` execution parallele candidate

## Regles de ce lot

- patch strictement documentaire
- aucun changement runtime
- aucun changement code applicatif
- aucun changement `OpenClaw`
- aucun changement `LocalCMS`
- aucun changement `admin-trading`
- aucun secret expose
