# WORKFLOW MEMORY_BRICKS V1

## Source d'etat

- source par defaut: `_state/memory_bricks`
- override local possible via `MEMORY_BRICKS_STATE_ROOT`
- source read-only validee sur fantome: `/home/fantome/opt-trading/_state/memory_bricks_localcms_source`

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

## Garde-fous OT

- utiliser `query` pour la consultation read-only
- ne pas prendre LocalCMS comme source de verite
- ne pas lancer `new`, `status`, `link` ou `index rebuild` sur une source ciblee en lecture seule
- ne pas ajouter `_state/` au commit
- ne pas rouvrir V1 sans ecart reel prouve

Voir aussi `modules/memory_bricks/docs/RUNBOOK_MEMORY_BRICKS_QUERY_V1.md`.
