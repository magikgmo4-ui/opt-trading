---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP2_RUNTIME_PATH_IMPL_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP2_RUNTIME_PATH_IMPL_01
status: open
lifecycle_stage: implementation_repo_only
topic_keys:
  - opt-trading
  - reseau_ssh
  - step2
  - runtime
  - path_resolution
  - symlink
  - implementation
surface: runtime
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_STEP2_RUNTIME_PATH_CADRAGE_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02/02_journal_technique.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02/03_decisions.md
  - docs/status/reseau_ssh_canonique.md
---

# GO_OPT_TRADING_RESEAU_SSH_STEP2_RUNTIME_PATH_IMPL_01 - Cadrage

## Objet

Ouvrir le lot d'implementation minimale necessaire pour corriger la resolution de path runtime de `reseau_ssh_step2`.

Ce lot est repo-side uniquement.

Ce lot ne vaut pas reprise du GO physique bloque.

L'objet exact est de produire un patch minimal sur les wrappers `step2` necessaires pour que le root module soit resolu depuis le chemin reel du script execute, y compris sous invocation via symlink installe.

## Etat de depart retenu

HEAD publie de reference :

`5180cc4 docs: add reseau ssh step2 runtime path cadrage`

Etat canonique acquis :

- `GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02` reste `BLOQUE`
- la baseline lecture seule sur `db-layer` est validee
- `sanity-reseau_ssh` = `PASS`
- `cmd-reseau_ssh sanity` = `PASS`
- `sanity-reseau_ssh_step2` = `FAIL`
- la cause retenue est un defaut de resolution de root module sous symlink

Constat repo-side utile :

- `modules/reseau_ssh_step2/scripts/sanity_check.sh` calcule actuellement `MOD` depuis `${0%/*}/..`
- `modules/reseau_ssh_step2/scripts/cmd.sh` calcule actuellement `MOD` depuis `${0%/*}/..`
- `modules/reseau_ssh_step2/scripts/menu.sh` calcule actuellement `MOD` depuis `${0%/*}/..`
- cette forme est compatible avec une invocation directe, mais pas operateur-reelle via wrapper/symlink installe

## Surface autorisee explicite

Surface autorisee dans ce lot :

- `modules/reseau_ssh_step2/scripts/sanity_check.sh`
- `modules/reseau_ssh_step2/scripts/cmd.sh`
- `modules/reseau_ssh_step2/scripts/menu.sh`
- eventuellement un helper shell local strictement dedie a la resolution de chemin, uniquement si cela permet de garder le patch minimal et plus robuste
- documentation minimale strictement necessaire pour expliquer la validation repo-side du correctif

Regle de surface :

- toucher le moins de fichiers possible
- ne modifier que la logique de resolution de chemin necessaire au runtime `step2`
- ne rien etendre au-dela des wrappers `step2` effectivement concernes sans preuve de necessite

## Exclusions explicites

Sont explicitement exclus de ce lot :

- toute bascule des alias courts `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh`
- toute mutation machine sur `db-layer` ou toute autre machine
- tout patch physique hors repo
- toute extension multi-machine
- tout retrait de `scripts/reseau_ssh/`
- tout retrait des wrappers racine
- tout retrait des alias `*_reseau_ssh_step2`
- tout retrait de `modules/reseau_ssh_step1b`
- tout refactor global de la famille `reseau_ssh`
- toute harmonisation large entre copies `modules/*/scripts/*` sans preuve qu'elle est necessaire au correctif minimal
- toute modification reseau, SSH, WireGuard ou firewall

## Correctif minimal vise

Le patch minimal vise doit :

- resoudre le chemin reel du script execute
- deriver `MOD` depuis ce chemin reel et non depuis le chemin du symlink invoque
- rester compatible avec une execution directe du script
- rester compatible avec une execution via symlink installe
- conserver le comportement fonctionnel existant hors resolution de path

Le patch minimal vise ne doit pas :

- changer le contrat des commandes exposees
- changer les noms d'alias
- introduire une nouvelle architecture de wrappers
- embarquer de nettoyage hors sujet

## Strategie d'implementation admise

Strategie admise dans ce lot :

1. identifier la forme minimale de resolution du chemin reel adaptee aux scripts Bash concernes
2. appliquer cette logique uniquement aux wrappers `step2` necessaires
3. verifier que `MOD` pointe vers le module reel meme sous symlink
4. verifier qu'aucun autre comportement des wrappers n'est touche

Formes attendues comme candidates raisonnables :

- `readlink -f "$0"`
- `readlink -f "${BASH_SOURCE[0]}"`
- une variante equivalente strictement justifiee

Le choix final doit privilegier :

- simplicite
- robustesse sous symlink
- faible surface de changement

## Checklist de validation explicite

Checklist de validation repo-side avant publication :

1. les scripts cibles modifies sont identifies explicitement
2. la logique `${0%/*}/..` n'est plus le point de verite final sous symlink
3. la logique retenue resolve bien le chemin reel du fichier execute
4. `MOD` derive bien vers `modules/reseau_ssh_step2`
5. `sanity_check.sh` continue de verifier `scripts/menu.sh` et `scripts/cmd.sh` sans regression
6. `cmd.sh info` continue d'afficher un `path` coherent
7. `menu.sh` continue d'afficher un `path` coherent
8. aucune autre surface `reseau_ssh` n'est modifiee sans necessite documentee
9. aucune mutation machine n'est introduite dans ce lot
10. aucune bascule d'alias courts n'est introduite dans ce lot

Checklist de smokes repo attendus :

1. execution directe de `modules/reseau_ssh_step2/scripts/sanity_check.sh`
2. execution via symlink local de test pointant vers `modules/reseau_ssh_step2/scripts/sanity_check.sh`
3. verification que la sortie `path=` n'est plus resolue vers `/usr/local`
4. execution directe de `modules/reseau_ssh_step2/scripts/cmd.sh info`
5. execution via symlink local de test de `modules/reseau_ssh_step2/scripts/cmd.sh info`
6. verification que `cmd.sh menu` continue de viser le bon `menu.sh`

Checklist de smokes machine attendus avant retour au GO physique :

1. `command -v sanity-reseau_ssh_step2`
2. `readlink -f /usr/local/bin/sanity-reseau_ssh_step2`
3. `sanity-reseau_ssh_step2`
4. `command -v cmd-reseau_ssh_step2`
5. `cmd-reseau_ssh_step2 info`
6. verification que le `path=` retourne le module reel et non `/usr/local`

## Critere de validation du lot

Le lot est valide seulement si :

- le patch reste minimal et borne
- le runtime `step2` devient operateur-reel sous symlink au moins au niveau des smokes definis
- aucune mutation machine n'a ete necessaire pour produire le correctif repo-side
- aucune reouverture prematuree du GO physique n'est faite

Le lot est invalide si :

- il derive vers un refactor global
- il embarque des changements hors wrappers `step2` sans justification stricte
- il modifie le contrat operateur des alias courts
- il suppose une validation machine non encore executee

## Point de reprise explicite

Le point de reprise apres ce lot est strictement le suivant :

1. publier le patch minimal repo-side
2. rejouer les smokes repo de `step2`
3. revenir ensuite sur `db-layer` pour rejouer les smokes machine `step2`
4. seulement si ces smokes machine passent, requalifier la question du retour a `GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02`

Jusqu'a cette validation, le cadre reste :

- GO physique : `BLOQUE`
- aucune bascule des alias courts
- aucune mutation machine dans ce lot d'implementation
