# RUNBOOK MEMORY_BRICKS QUERY V1

## Prerequis

- checkout reel: `/home/fantome/opt-trading`
- branche attendue: `feat/memory-bricks-v1-impl-harden`
- wrapper repo-local: `modules/memory_bricks/scripts/cmd.sh`
- si la source a lire n'est pas la source par defaut, definir `MEMORY_BRICKS_STATE_ROOT`

## Shortcuts optionnels

```bash
bash modules/memory_bricks/scripts/install_shortcuts.sh
```

- mode par defaut: installation dans `~/.local/bin` sans `sudo`
- si besoin systeme explicite: `bash modules/memory_bricks/scripts/install_shortcuts.sh --system`
- si `~/.local/bin` n'est pas dans `PATH`, l'ajouter avant d'appeler `cmd-memory_bricks`, `menu-memory_bricks` ou `sanity-memory_bricks`

### Mode --system: prerequis et validation

- prerequis: accès `sudo` effectif, `/usr/local/bin` existant ou créable
- cible: `/usr/local/bin` (3 symlinks: `cmd-memory_bricks`, `menu-memory_bricks`, `sanity-memory_bricks`)
- validation manuelle après installation:
  - `ls -la /usr/local/bin/*memory_bricks` (symlinks présents et cibles valides)
  - `sanity-memory_bricks` ou `cmd-memory_bricks query status` (exécution effective)
- `smoke_wrappers.sh` ne couvre pas `--system` (local-first uniquement)
- pas de désinstallation automatisée; suppression manuelle des symlinks si besoin

## Validation standard

```bash
python3 -m unittest discover -s modules/memory_bricks/tests -p "test_*.py" -v
bash modules/memory_bricks/scripts/sanity_check.sh
bash modules/memory_bricks/scripts/smoke_wrappers.sh
```

- ordre recommande quand tout s'applique: `unittest` -> `sanity_check.sh` -> `smoke_wrappers.sh`
- `python3 -m unittest ...`: regression logique Python
- `sanity_check.sh`: verifie la validite module, les prerequis et la surface minimale repo-locale
- `smoke_wrappers.sh`: verifie les wrappers reellement exposes apres installation local-first, y compris `cmd-memory_bricks`, `menu-memory_bricks` et `sanity-memory_bricks`

## Politique minimale selon le changement

- lecture/review doc seule: aucune commande obligatoire
- modif doc seule: aucune commande obligatoire si les commandes documentees restent identiques; sinon rejouer les commandes citees
- modif code Python: lancer `python3 -m unittest discover -s modules/memory_bricks/tests -p "test_*.py" -v`, puis `bash modules/memory_bricks/scripts/sanity_check.sh`; ajouter `bash modules/memory_bricks/scripts/smoke_wrappers.sh` si les wrappers ou entrypoints exposes peuvent etre affectes
- modif scripts/wrappers: lancer `bash modules/memory_bricks/scripts/sanity_check.sh`, puis `bash modules/memory_bricks/scripts/smoke_wrappers.sh`; ajouter `python3 -m unittest discover -s modules/memory_bricks/tests -p "test_*.py" -v` si la logique Python ou la CLI peut etre affectee

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
