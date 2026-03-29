# WORKFLOW MEMORY_BRICKS V1

## Source d'etat

- source par defaut: `_state/memory_bricks`
- override local possible via `MEMORY_BRICKS_STATE_ROOT`
- source read-only validee sur fantome: `/home/fantome/opt-trading/_state/memory_bricks_localcms_source`

## Acces operateur

- acces repo-local direct toujours possible via `modules/memory_bricks/scripts/cmd.sh`, `modules/memory_bricks/scripts/menu.sh` et `modules/memory_bricks/scripts/sanity_check.sh`
- installation optionnelle des shortcuts via `bash modules/memory_bricks/scripts/install_shortcuts.sh`
- mode par defaut: installation dans `~/.local/bin` sans `sudo`
- mode systeme explicite disponible via `bash modules/memory_bricks/scripts/install_shortcuts.sh --system`
- ajouter `~/.local/bin` a `PATH` si les shortcuts installes ne sont pas resolus directement

## Flux mutation

1. creer une brique via `modules/memory_bricks/scripts/cmd.sh new`
2. relire via `list` ou `show`, puis ajuster `status` ou `link`
3. reconstruire les index via `index rebuild`
4. produire `export`, `merge` ou `handoff` selon le besoin de reprise

## Flux read-only recommande

1. verifier la source cible via `query status`
2. lister les briques via `query list`
3. afficher une brique via `query show --id MB-00001`
4. rechercher via `query find --text "localcms"`

## Exemples minimaux

```bash
STATE_ROOT="/home/fantome/opt-trading/_state/memory_bricks_localcms_source"
CMD="/home/fantome/opt-trading/modules/memory_bricks/scripts/cmd.sh"

MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" "$CMD" query status
MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" "$CMD" query list
MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" "$CMD" query show --id MB-00001
MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" "$CMD" query find --text "localcms"
```

## Validation standard

1. lancer `python3 -m unittest discover -s modules/memory_bricks/tests -p "test_*.py" -v` pour la regression logique Python
2. verifier la validite module et les prerequis via `bash modules/memory_bricks/scripts/sanity_check.sh`
3. verifier les wrappers et entrypoints exposes via `bash modules/memory_bricks/scripts/smoke_wrappers.sh`

- ordre recommande quand les trois niveaux s'appliquent: `unittest` -> `sanity_check.sh` -> `smoke_wrappers.sh`
- `python3 -m unittest ...`: validation fonctionnelle Python et regression logique
- `sanity_check.sh`: valide la surface minimale du module sur un etat temporaire repo-local
- `smoke_wrappers.sh`: valide l'installation local-first et l'execution reelle de `cmd-memory_bricks`, `menu-memory_bricks` et `sanity-memory_bricks`

## Politique de validation

- lecture/review doc seule: aucune commande obligatoire
- modif doc seule: aucune commande obligatoire si les commandes documentees ne changent pas; sinon rejouer au minimum les commandes citees
- modif code Python: lancer `python3 -m unittest discover -s modules/memory_bricks/tests -p "test_*.py" -v`, puis `bash modules/memory_bricks/scripts/sanity_check.sh`; ajouter `bash modules/memory_bricks/scripts/smoke_wrappers.sh` si les entrypoints exposes ou les wrappers peuvent etre impactes
- modif scripts/wrappers: lancer `bash modules/memory_bricks/scripts/sanity_check.sh`, puis `bash modules/memory_bricks/scripts/smoke_wrappers.sh`; ajouter `python3 -m unittest discover -s modules/memory_bricks/tests -p "test_*.py" -v` si la regression logique Python ou la CLI peut etre affectee

## Garde-fous OT

- utiliser `query` pour la consultation read-only
- ne pas prendre LocalCMS comme source de verite
- ne pas lancer `new`, `status`, `link` ou `index rebuild` sur une source ciblee en lecture seule
- ne pas ajouter `_state/` au commit
- ne pas rouvrir V1 sans ecart reel prouve

Voir aussi `modules/memory_bricks/docs/RUNBOOK_MEMORY_BRICKS_QUERY_V1.md`.
