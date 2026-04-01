# SPEC MEMORY_BRICKS V1

## Etat et stockage

- module durable local, source de verite par defaut sous `_state/memory_bricks`
- override local possible via `MEMORY_BRICKS_STATE_ROOT`
- frontmatter stable sans dependance externe, ID `MB-00001`, statuts/types figes

## Surface livree

- commandes mutation: `new`, `list`, `show`, `status`, `link`, `index rebuild`, `export`, `merge`, `handoff`
- commandes read-only: `query status`, `query list`, `query show --id`, `query find --text`

## Acces operateur

- acces repo-local direct: `modules/memory_bricks/scripts/cmd.sh`, `modules/memory_bricks/scripts/menu.sh`, `modules/memory_bricks/scripts/sanity_check.sh`
- installation optionnelle des shortcuts via `modules/memory_bricks/scripts/install_shortcuts.sh`
- mode par defaut: installation dans `~/.local/bin` sans `sudo`
- mode systeme explicite: `--system` vers `/usr/local/bin`
- mode dossier explicite: `--bin-dir PATH`
- si `~/.local/bin` n'est pas dans `PATH`, l'operateur doit l'ajouter pour appeler `cmd-memory_bricks`, `menu-memory_bricks`, `sanity-memory_bricks`

## Validation livree

- validation Python: `python3 -m unittest discover -s modules/memory_bricks/tests -p "test_*.py" -v`
- validation shell repo-locale: `bash modules/memory_bricks/scripts/sanity_check.sh`
- smoke wrappers dedie: `bash modules/memory_bricks/scripts/smoke_wrappers.sh`

## Limites reelles

- le mode systeme explicite `--system` repose toujours sur `sudo`
- le smoke wrappers couvre le mode local-first par defaut, pas le mode `--system`
- LocalCMS, UI, API active, cloud, mobile: hors perimetre V1
- `_state/` reste hors Git
