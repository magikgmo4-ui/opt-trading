---
doc_id: GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02
status: open
lifecycle_stage: execution_machine_01
topic_keys:
  - opt-trading
  - reseau_ssh
  - physical
  - machine_01
  - db_layer
  - rollback
  - smoke_tests
surface: runtime
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/03_decisions.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/00_cadrage.md
  - docs/status/reseau_ssh_canonique.md
---

# GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02 - Cadrage

## Objet

Ouvrir le premier lot physique borne de `reseau_ssh` pour executer une seule machine cible, sans glissement implicite vers une migration globale.

Ce GO est un lot d'execution machine unique.

Il ne vaut pas :

- bascule globale du canon operateur
- extension multi-machine automatique
- retrait differe
- refonte runtime hors perimetre

## Parent et filiation

Parent actif :

`GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`

Prealables documentaires retenus :

- `GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01`
- `GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01`

Etat acquis avant ouverture :

- repo propre sur `sot/mainline`
- tete Git validee : `b35e4d4`
- merge PR `#152` confirme dans l'historique reel : `bcee8fe`
- cible finale documentaire retenue : `modules/reseau_ssh_step2`
- contrat operateur final vise : alias courts `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh`
- `scripts/reseau_ssh/` reste le canon operateur actuel avant validation machine

## Machine 01 retenue

Machine 01 de ce lot initial :

`db-layer`

Justification :

- `db-layer` possede deja la compat `*_reseau_ssh_step2`
- la machine permet de valider une transition avec preuve de compat existante
- le risque est plus borne que `student`
- elle evite de commencer par le cas sans compat preexistante de `admin-trading`

Inventaire canonique associe :

- LAN actif : `192.168.0.100`
- WG : `10.66.66.2`

## Perimetre autorise

Ce GO autorise uniquement, pour `db-layer` :

- inventaire initial frais
- capture de baseline
- capture des preuves rollback
- validation de presence de `modules/reseau_ssh_step2`
- repointage eventuel des alias courts de la machine 01 seulement
- execution des smoke tests avant et apres
- verdict `PASS` ou `FAIL` documente pour la machine 01

Ce GO n'autorise pas :

- action sur `admin-trading`
- action sur `student`
- action sur `cursor-ai` / WSL
- retrait des alias `*_reseau_ssh_step2`
- retrait de `scripts/reseau_ssh/`
- retrait des wrappers racine
- retrait de `modules/reseau_ssh_step1b`
- migration simultanee de plusieurs machines
- extension implicite du resultat machine 01 aux autres machines
- modification de `fantome`
- patchs hors famille `reseau_ssh`

## Baseline obligatoire avant action

Avant toute mutation sur `db-layer`, capturer et consigner :

- `command -v menu-reseau_ssh`
- `command -v cmd-reseau_ssh`
- `command -v sanity-reseau_ssh`
- `readlink -f /usr/local/bin/menu-reseau_ssh`
- `readlink -f /usr/local/bin/cmd-reseau_ssh`
- `readlink -f /usr/local/bin/sanity-reseau_ssh`
- `command -v menu-reseau_ssh_step2 || true`
- `command -v cmd-reseau_ssh_step2 || true`
- `command -v sanity-reseau_ssh_step2 || true`
- `readlink -f /usr/local/bin/menu-reseau_ssh_step2 || true`
- `readlink -f /usr/local/bin/cmd-reseau_ssh_step2 || true`
- `readlink -f /usr/local/bin/sanity-reseau_ssh_step2 || true`
- `test -d /opt/trading/scripts/reseau_ssh`
- `test -d /opt/trading/modules/reseau_ssh_step2`
- `test -e /opt/trading/scripts/reseau_ssh_cmd.sh`
- `test -e /opt/trading/scripts/reseau_ssh_menu.sh`

Preuve complementaire obligatoire :

- hash ou snapshot des wrappers racine presents
- cible exacte pre-migration des alias courts
- cible exacte pre-migration des alias `*_step2`

Aucune action n'est admissible si cette baseline est incomplete.

## Mutation admissible sur machine 01

La seule mutation admissible dans ce GO est :

- repointer les alias courts `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh` de `db-layer` vers la cible `modules/reseau_ssh_step2`

Conditions strictes avant mutation :

- baseline complete
- rollback ecrit et verifiable
- smoke initial `PASS`
- presence effective de la cible `modules/reseau_ssh_step2`
- aucun doute sur la cible resolue par `readlink -f`

Les elements suivants doivent rester intacts pendant tout le lot :

- `scripts/reseau_ssh/`
- wrappers racine
- alias `*_reseau_ssh_step2`
- `modules/reseau_ssh_step1b`

## Plan d'execution borne

Sequence imposee :

1. confirmer que le lot ne cible que `db-layer`
2. capturer la baseline complete
3. executer les smoke tests avant changement
4. valider la cible `modules/reseau_ssh_step2`
5. preparer les commandes de rollback exactes
6. repointer les trois alias courts de `db-layer`
7. executer les smoke tests apres changement
8. consigner le verdict `PASS` ou `FAIL`
9. si `FAIL`, executer le rollback immediat
10. ne pas passer a une autre machine dans ce GO

## Rollback explicite

Le rollback est obligatoire, immediat et machine-local.

Avant mutation, ecrire les commandes de restauration permettant de remettre `db-layer` a son etat pre-migration.

Rollback minimal attendu :

- restaurer `/usr/local/bin/menu-reseau_ssh` vers sa cible pre-migration capturee
- restaurer `/usr/local/bin/cmd-reseau_ssh` vers sa cible pre-migration capturee
- restaurer `/usr/local/bin/sanity-reseau_ssh` vers sa cible pre-migration capturee
- conserver ou restaurer les alias `*_reseau_ssh_step2` selon l'etat capture
- verifier que `scripts/reseau_ssh/` est toujours present
- verifier que les wrappers racine sont toujours presents
- verifier que `modules/reseau_ssh_step1b` n'a subi aucune mutation

Le rollback est repute valide seulement si les smoke tests post-rollback reviennent a l'etat `PASS` sur les cibles pre-migration.

## Smoke tests obligatoires

Smoke tests avant et apres mutation sur `db-layer` :

```bash
command -v menu-reseau_ssh
command -v cmd-reseau_ssh
command -v sanity-reseau_ssh
readlink -f /usr/local/bin/menu-reseau_ssh
readlink -f /usr/local/bin/cmd-reseau_ssh
readlink -f /usr/local/bin/sanity-reseau_ssh
sanity-reseau_ssh
cmd-reseau_ssh sanity
```

Smoke tests de compat `step2` a conserver :

```bash
command -v menu-reseau_ssh_step2
command -v cmd-reseau_ssh_step2
command -v sanity-reseau_ssh_step2
sanity-reseau_ssh_step2
```

Smoke tests de conservation des surfaces de rollback :

```bash
test -d /opt/trading/scripts/reseau_ssh
test -d /opt/trading/modules/reseau_ssh_step2
test -e /opt/trading/scripts/reseau_ssh_cmd.sh
test -e /opt/trading/scripts/reseau_ssh_menu.sh
```

Les tests destructifs, les changements reseau globaux et les actions touchant plusieurs machines sont exclus.

## Critere PASS / FAIL

### PASS machine 01

Le verdict `PASS` ne peut etre pose que si :

- la baseline initiale est complete
- les alias courts sur `db-layer` resolvent vers la cible attendue apres mutation
- `sanity-reseau_ssh` passe apres mutation
- `cmd-reseau_ssh sanity` passe apres mutation
- les alias `*_reseau_ssh_step2` restent fonctionnels si presents
- `scripts/reseau_ssh/` reste disponible pour rollback
- wrappers racine et `step1b` restent intacts
- aucune autre machine n'a ete touchee

### FAIL machine 01

Le verdict `FAIL` est obligatoire si :

- baseline incomplete
- rollback non verifiable
- divergence de cible dans `readlink -f`
- echec d'un smoke test avant mutation
- echec d'un smoke test apres mutation
- doute sur l'integrite de `scripts/reseau_ssh/`
- doute sur les wrappers racine
- mutation hors perimetre machine 01

En cas de `FAIL` :

- rollback immediat
- aucun passage machine 02
- documentation de l'etat observe
- maintien du blocage sur toute extension physique

## Regle de non-extension

Le resultat de ce GO ne se propage pas automatiquement a `admin-trading` ni a `student`.

Meme si `db-layer` est `PASS` :

- aucun lot machine 02 n'est implicitement ouvert
- aucune bascule globale du canon operateur n'est validee
- aucun retrait differe ne devient admissible par simple succes de la machine 01

Toute extension devra faire l'objet d'un arbitrage explicite et d'un lot separe ou d'une suite documentaire validee.

## Point de reprise

```text
GO ouvert :
GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02

Machine 01 :
db-layer

Etat de depart :
- repo propre sur sot/mainline
- HEAD valide : b35e4d4
- merge PR #152 confirme : bcee8fe
- cible finale documentaire : modules/reseau_ssh_step2
- canon operateur actuel avant validation machine : scripts/reseau_ssh/

Prochaine action admissible :
1) capturer baseline et rollback exacts sur db-layer
2) executer les smoke tests avant changement
3) repointer les alias courts de db-layer seulement si baseline et rollback sont complets
4) executer les smoke tests apres changement
5) conclure PASS ou FAIL avant toute suite
```

## Verdict du cadrage

`GO_PHYSIQUE_MACHINE_01_OUVERT`

Le lot physique est ouvert pour `db-layer` uniquement.

Aucune extension multi-machine ni aucun retrait differe n'est autorise par ce document seul.
