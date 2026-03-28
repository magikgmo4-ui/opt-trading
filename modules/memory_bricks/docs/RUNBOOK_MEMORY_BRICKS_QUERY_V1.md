# RUNBOOK MEMORY_BRICKS QUERY V1

## Prerequis

- checkout reel: `/home/fantome/opt-trading`
- branche attendue: `feat/memory-bricks-v1-impl-harden`
- wrapper repo-local: `modules/memory_bricks/scripts/cmd.sh`
- si la source a lire n'est pas la source par defaut, definir `MEMORY_BRICKS_STATE_ROOT`

## Source read-only validee

```bash
STATE_ROOT="/home/fantome/opt-trading/_state/memory_bricks_localcms_source"
CMD="/home/fantome/opt-trading/modules/memory_bricks/scripts/cmd.sh"
```

## Commandes exactes

```bash
MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" "$CMD" query status
MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" "$CMD" query list
MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" "$CMD" query list --ia claude
MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" "$CMD" query show --id MB-00001
MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" "$CMD" query find --text "localcms"
```

## Ce que fait chaque commande

- `query status`: resume la source ciblee, le nombre de briques et la presence des index/meta
- `query list`: liste les briques disponibles, avec filtres simples si besoin
- `query show --id`: affiche une brique markdown precise
- `query find --text`: recherche texte simple sur id, titre, resume, reprise, tags et contenu markdown

## Exemples utiles

```bash
MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" "$CMD" query list --status open
MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" "$CMD" query list --machine fantome
MEMORY_BRICKS_STATE_ROOT="$STATE_ROOT" "$CMD" query find --text "read-only"
```

## Erreurs usuelles

- `ROOT_EXISTS: no`: la racine ciblee n'existe pas
- sortie vide sur `query list` ou `query find`: aucun resultat pour cette source ou ce filtre
- `ERROR: Brick not found`: l'ID demande n'existe pas dans la source ciblee
- `ERROR: Query text cannot be empty`: le texte de recherche est vide

## Ce qu'il ne faut pas faire

- ne pas utiliser `new`, `status`, `link` ou `index rebuild` sur une source ciblee en lecture seule
- ne pas confondre surface de lecture et source de verite
- ne pas ajouter `_state/` au commit
- ne pas rouvrir LocalCMS dans cette passe
