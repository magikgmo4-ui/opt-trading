---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP2_RUNTIME_PATH_CADRAGE_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP2_RUNTIME_PATH_CADRAGE_01
status: open
lifecycle_stage: cadrage_doc_only
topic_keys:
  - opt-trading
  - reseau_ssh
  - step2
  - runtime
  - path_resolution
  - symlink
  - doc_only
surface: runtime
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02/02_journal_technique.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02/03_decisions.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/03_decisions.md
  - docs/status/reseau_ssh_canonique.md
---

# GO_OPT_TRADING_RESEAU_SSH_STEP2_RUNTIME_PATH_CADRAGE_01 - Cadrage

## Objet

Ouvrir un lot documentaire separe pour cadrer le correctif minimal de forme runtime de `reseau_ssh_step2`.

Ce lot ne vaut pas correction appliquee.

Ce lot ne vaut pas reprise du GO physique bloque.

L'objet exact est de cadrer la correction minimale de resolution de path runtime necessaire pour rendre `step2` operateur-reel lorsqu'il est invoque via alias ou wrapper installe.

## Etat de depart retenu

Etat repo retenu apres figement du constat bloquant :

`0b5946e docs: anchor db-layer baseline blockage for reseau ssh physical consolidation`

Etat canonique acquis :

- le GO actif `GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02` porte maintenant correctement le constat bloquant
- aucune mutation machine n'a ete faite sur `db-layer`
- la baseline lecture seule sur `db-layer` est validee
- `sanity-reseau_ssh` = `PASS`
- `cmd-reseau_ssh sanity` = `PASS`
- `sanity-reseau_ssh_step2` = `FAIL`
- la bascule physique des alias courts reste `BLOQUEE`

Cause retenue a cadrer :

- `step2` n'est pas operateur-reel sous symlink
- la resolution de path actuelle derive le root module depuis le chemin invoque au lieu du chemin reel du script execute
- l'execution via `/usr/local/bin/sanity-reseau_ssh_step2` aboutit a une resolution vers `/usr/local`
- l'echec observe est `FAIL: scripts missing`

## Regle de securite du present lot

Ce lot est doc-only au stade courant.

Interdits dans ce lot :

- aucune mutation machine
- aucun repointage d'alias courts
- aucun changement sur `db-layer`
- aucune reprise du GO physique bloque
- aucun patch runtime applique dans ce document
- aucune modification de symlink sur machine
- aucune extension multi-machine

Ce cadrage prepare le correctif minimal. Il ne l'autorise pas encore.

## Perimetre exact

Perimetre retenu :

- logique de resolution de chemin des scripts `reseau_ssh_step2`
- comportement des wrappers `step2` lorsqu'ils sont invoques via alias ou symlink installes
- preuve repo-first de la correction minimale
- definition des smokes cibles a rejouer ensuite sur machine reelle

Surfaces explicitement hors perimetre :

- bascule des alias courts `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh`
- suppression de `scripts/reseau_ssh/`
- suppression des wrappers racine
- retrait des alias `*_reseau_ssh_step2`
- retrait de `modules/reseau_ssh_step1b`
- toute correction reseau, SSH ou machine

## Hypothese forte a valider

Hypothese forte de correction minimale :

- le chemin reel du script `step2` doit etre resolu a partir du fichier execute reel
- le root module doit ensuite etre derive depuis ce chemin reel
- la logique ne doit plus dependre du chemin du symlink invoque

Formes de solution possibles a evaluer dans le lot correctif :

- `readlink -f \"$0\"`
- `BASH_SOURCE[0]` combine a `readlink -f`
- toute variante equivalente qui prouve la meme propriete de resolution reelle

Cette hypothese oriente le lot. Elle ne vaut pas validation technique finale tant que les preuves attendues ne sont pas produites.

## Correctif minimal vise

Le correctif minimal vise doit :

- corriger uniquement la resolution de path runtime necessaire a `step2`
- conserver le contrat operateur existant des alias courts
- ne pas introduire de refonte structurelle du module
- ne pas embarquer de nettoyage hors sujet
- rester publiable independamment de toute mutation machine

Le lot devra rester strictement minimal et bornable.

## Preuves attendues avant retour au GO physique

Avant toute reprise de `GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02`, il faudra disposer de preuves explicites :

1. identification exacte du ou des scripts `step2` responsables de la mauvaise resolution
2. description du calcul actuel menant a `/usr/local`
3. correctif repo applique sur la seule logique de resolution necessaire
4. verification locale ou repo-first que le root module cible devient celui du fichier reel
5. definition ou mise a jour des smokes cibles a rejouer sur machine reelle
6. absence de derive vers une bascule d'alias dans ce lot

## Validation attendue du futur correctif

Le futur correctif ne pourra etre considere comme pret a republier que si :

- la resolution du root module se fait depuis le chemin reel du script
- l'invocation via symlink ne derive plus vers `/usr/local`
- `sanity_reseau_ssh_step2` trouve ses scripts attendus
- aucun autre contrat runtime `reseau_ssh` n'est modifie sans necessite
- le correctif reste separe de toute mutation machine

## Point de reprise vers le GO physique bloque

Le retour vers `GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02` ne pourra etre reouvert qu'apres :

1. publication du correctif minimal de path runtime `step2`
2. revalidation de `sanity-reseau_ssh_step2` sur machine reelle via wrapper installe
3. confirmation explicite que `step2` est devenu operateur-reel sous symlink
4. requalification seulement alors de la bascule des alias courts

Jusqu'a cette preuve, le verdict du GO physique courant reste :

`BLOQUE`

## RISKS

- À qualifier.
