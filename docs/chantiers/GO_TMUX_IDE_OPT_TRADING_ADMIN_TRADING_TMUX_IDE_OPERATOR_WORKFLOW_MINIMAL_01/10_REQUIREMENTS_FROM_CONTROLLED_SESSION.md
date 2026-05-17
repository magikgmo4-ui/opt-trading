# 10_REQUIREMENTS_FROM_CONTROLLED_SESSION

## 1_MASTER_TARGET

Extraire les exigences minimales imposees par la session controlee `tmux-ide` deja validee.

## 2_PROVEN_INPUT

Le GO precedent a etabli :

```text
PASS_CONTROLLED_SESSION
```

Elements prouves :

- `npx -y tmux-ide@1.3.1 validate --json` a retourne `valid=true` ;
- une session `opt-trading-admin-trading` a ete creee ;
- `status --json` a observe une session running avec 3 panes ;
- `inspect --json` a observe une config valide avec 2 rows et 3 panes ;
- `stop` a ferme la session ;
- `/opt/trading/ide.yml` a ete supprime ;
- aucune installation globale n'a ete effectuee ;
- aucun index global n'a ete modifie.

## 3_REQUIRED_INVARIANTS

Le workflow operateur minimal doit conserver ces invariants :

- utiliser uniquement `npx -y tmux-ide@1.3.1` ;
- refuser de demarrer si `/opt/trading/ide.yml` existe deja ;
- refuser de demarrer si `tmux has-session -t opt-trading-admin-trading` reussit ;
- borner l'attache TUI avec `timeout` ;
- verifier la session par `status --json` et `inspect --json` ;
- appeler `stop` avant la fin du protocole ;
- supprimer tout `ide.yml` temporaire cree par le protocole ;
- supprimer le script temporaire distant ;
- ne pas executer de commande de trading, webhook, paper ou live ;
- ne pas corriger les deltas preexistants du repo distant.

## 4_OPERATOR_REQUIREMENTS

Le premier workflow operateur doit rester un dry-run d'observation.

Il doit permettre a l'operateur de constater :

- le repertoire courant ;
- l'etat Git local du repo distant ;
- la presence des dossiers chantier `tmux-ide` disponibles localement ;
- la structure de panes exposee par `tmux-ide` ;
- la capacite de fermeture propre.

Il ne doit pas permettre de conclure :

- qu'un usage long est valide ;
- qu'une configuration durable peut etre commitee ;
- que le repo distant est pret pour production ;
- qu'un workflow applicatif reel peut etre lance.

## 5_REMOTE_REPO_REQUIREMENT

Le repo distant `admin-trading:/opt/trading` peut contenir des deltas preexistants et peut etre en retard de `origin/sot/mainline`.

Consequence :

- le dry-run ne doit pas faire `git pull`, `git reset`, `git clean`, `git stash` ou checkout distant ;
- les panes doivent utiliser des commandes de lecture tolerantes a un repo non realigne ;
- le verdict ne doit pas transformer le dry-run en decision de realignement.

## 6_TEMP_FILE_REQUIREMENT

Un `ide.yml` temporaire n'est acceptable que dans un GO de dry-run operateur autorise par gate.

Conditions minimales :

- le fichier doit etre cree seulement apres `test ! -e /opt/trading/ide.yml` ;
- le contenu doit etre strictement minimal et read-only ;
- le cleanup doit supprimer `/opt/trading/ide.yml` si le protocole l'a cree ;
- le cleanup doit verifier que la session cible n'existe plus.

## 7_STOP_REQUIREMENTS

Le protocole doit stopper immediatement si :

- `admin-trading:/opt/trading` est inaccessible ;
- `/opt/trading/ide.yml` existe avant le test ;
- une session `opt-trading-admin-trading` existe deja ;
- `tmux-ide validate --json` echoue ;
- une commande non autorisee est requise pour continuer ;
- la session ne peut pas etre arretee proprement ;
- le cleanup laisse un `ide.yml` ou une session cible.

## 8_ALLOWED_GATE_OUTPUTS

Les sorties gate possibles sont :

```text
ALLOW_OPERATOR_DRY_RUN
HOLD
BLOCKED
```

Definition :

- `ALLOW_OPERATOR_DRY_RUN` : le protocole est assez borne pour un dry-run operateur non destructif ;
- `HOLD` : il manque une decision operatoire, notamment sur le repo distant, mais aucun blocage dur n'est prouve ;
- `BLOCKED` : un invariant de securite est incompatible avec l'execution.

## 17_RESUME_POINT

```text
REPRISE:
Les exigences imposent un dry-run read-only, ephemeral et stoppable.

NEXT:
Lire 20_OPERATOR_WORKFLOW_MINIMAL.md pour le workflow concret.
```
