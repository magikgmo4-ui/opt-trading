---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01
status: open
lifecycle_stage: cadrage_execution_future
topic_keys:
  - opt-trading
  - reseau_ssh
  - runtime
  - compat
  - retirement
  - rollback
surface: docs
source_kind: canonical
updated_at: 2026-04-20
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/03_decisions.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01/00_cadrage.md
  - docs/status/reseau_ssh_canonique.md
---

# GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01 - Cadrage

## Objet

Ouvrir le cadrage documentaire du futur lot physique de convergence runtime et compatibilites pour `reseau_ssh`.

Ce document prepare l'execution future. Il n'est pas l'application du lot physique.

Ce GO devra permettre, dans un temps d'execution separe, de converger vers :

- cible module unique : `modules/reseau_ssh_step2`
- contrat operateur final : alias courts stables `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh`
- compatibilites legacy/transitoires maintenues ou retirees seulement selon criteres explicites

## Etat de depart retenu

Etat repo apres publication du commit :

`c063ac1 docs: add reseau ssh target decision doc-only pack`

Etat canonique retenu :

- `GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01` a fige la cible finale unique : `modules/reseau_ssh_step2`
- le runtime final vise conserve les alias courts : `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh`
- `scripts/reseau_ssh/` reste le canon operateur actuel tant que la migration physique n'est pas executee
- `modules/reseau_ssh_step2` est la cible de convergence future, pas encore la cible runtime des alias courts partout
- `modules/reseau_ssh_step1b` reste legacy / compat a risque
- wrappers racine encore presents sur les machines Linux auditees
- alias `*_reseau_ssh_step2` presents sur certaines machines seulement
- `NO_GO_PHYSICAL` reste actif tant que ce cadrage n'est pas transforme en execution validee

## Regle de securite du present cadrage

Ce lot de cadrage est doc-only.

Interdits dans ce lot :

- aucun patch runtime
- aucun retrait effectif
- aucun renommage
- aucun repointage
- aucune modification de symlink
- aucune modification d'alias
- aucune modification liee a `fantome`
- aucune modification des wrappers racine
- aucune execution machine

Ce cadrage ne donne pas, a lui seul, feu vert a l'application physique.

## Perimetre futur

Le futur lot physique sera borne a la famille `reseau_ssh`.

Surfaces concernees par l'execution future :

| Surface | Role cible | Statut dans ce cadrage |
| --- | --- | --- |
| `modules/reseau_ssh_step2` | cible module unique finale | cible retenue, non appliquee ici |
| alias courts `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh` | contrat operateur final | noms conserves |
| `scripts/reseau_ssh/` | runtime operateur actuel puis compat/rollback | a conserver intact au debut |
| alias `*_reseau_ssh_step2` | compat transitoire | retrait differe seulement |
| wrappers racine `scripts/reseau_ssh_cmd.sh`, `scripts/reseau_ssh_menu.sh` | candidate-retire-later | retrait interdit en premiere phase |
| `modules/reseau_ssh_step1b` | legacy / compat a risque | gel, pas de retrait initial |
| `modules/reseau_ssh` | legacy historique | hors execution initiale sauf preuve explicite |

Hors perimetre :

- `fantome`
- autres familles module
- shims runtime non `reseau_ssh`
- refonte documentaire globale des index
- retrait d'archives historiques
- migration implicite non tracee machine par machine

## Bornage machine par machine

| Machine | Etat retenu | Action future admise | Action interdite en premiere phase |
| --- | --- | --- | --- |
| `admin-trading` | alias courts vers `scripts/reseau_ssh/`; compat `step2` absente ; wrappers racine presents | valider presence cible `step2`, puis repointage alias courts seulement si rollback pret | retirer wrappers, retirer `scripts/reseau_ssh/`, retirer legacy |
| `db-layer` | alias courts vers `scripts/reseau_ssh/`; compat `step2` presente ; wrappers racine presents | utiliser la compat `step2` comme preuve de transition et repointer alias courts apres smoke | retirer alias `*_step2` avant stabilite |
| `student` | alias courts vers `scripts/reseau_ssh/`; compat `step2` presente ; usage historique `step1b` prouve ; wrappers racine presents | traiter comme machine a risque fort, valider sans retrait et garder rollback complet | retirer `step1b` ou wrappers racine |
| `cursor-ai` / WSL | aucune surface locale exploitable retenue dans l'audit courant | audit local dedie seulement si une surface Linux locale devient pertinente | appliquer une migration par supposition |

## Prerequis d'execution

Avant toute execution physique, le futur GO devra disposer de preuves fraiches, datees et machine par machine :

1. branche Git et docs canoniques a jour
2. inventaire `command -v` des alias courts
3. inventaire `readlink -f` des alias courts
4. inventaire des alias `*_reseau_ssh_step2` quand presents
5. inventaire des wrappers racine
6. inventaire de `scripts/reseau_ssh/`
7. inventaire de `modules/reseau_ssh_step2`
8. preuve que `modules/reseau_ssh_step2` couvre les fonctions attendues
9. plan de rollback ecrit avant application
10. smoke tests ecrits avant application
11. ordre machine par machine valide
12. critere d'arret accepte avant changement

Aucune machine ne doit etre modifiee si son inventaire initial est incomplet.

## Mapping actuel vers final

| Actuel | Final vise | Mode d'application future | Condition |
| --- | --- | --- | --- |
| `/usr/local/bin/menu-reseau_ssh` | alias court conserve vers cible `step2` | repointage explicite | smoke menu OK + rollback pret |
| `/usr/local/bin/cmd-reseau_ssh` | alias court conserve vers cible `step2` | repointage explicite | `cmd-reseau_ssh sanity` OK |
| `/usr/local/bin/sanity-reseau_ssh` | alias court conserve vers cible `step2` | repointage explicite | `sanity-reseau_ssh` OK |
| `/usr/local/bin/menu-reseau_ssh_step2` | compat transitoire | maintien puis retrait differe possible | alias courts stabilises |
| `/usr/local/bin/cmd-reseau_ssh_step2` | compat transitoire | maintien puis retrait differe possible | alias courts stabilises |
| `/usr/local/bin/sanity-reseau_ssh_step2` | compat transitoire | maintien puis retrait differe possible | alias courts stabilises |
| `/opt/trading/scripts/reseau_ssh/` | compat / rollback apres migration | maintien obligatoire initial | retour arriere disponible |
| `/opt/trading/modules/reseau_ssh_step2/` | cible module unique | validation puis cible runtime | completude prouvee |
| `/opt/trading/scripts/reseau_ssh_cmd.sh` | candidate-retire-later | aucun retrait initial | absence de callers prouvee ulterieurement |
| `/opt/trading/scripts/reseau_ssh_menu.sh` | candidate-retire-later | aucun retrait initial | absence de callers prouvee ulterieurement |
| `/opt/trading/modules/reseau_ssh_step1b/` | legacy gele | maintien initial | historique classe et rollback conserve |

## Ordre d'application futur

L'application physique devra etre sequencee, sans retrait initial :

1. confirmer l'inventaire machine cible
2. capturer les snapshots rollback
3. valider `modules/reseau_ssh_step2` sans changer les alias courts
4. executer les smoke tests sur l'etat courant
5. repointer les alias courts d'une seule machine
6. executer les smoke tests apres repointage
7. documenter PASS/FAIL machine
8. passer a la machine suivante seulement si la machine courante est PASS
9. conserver `scripts/reseau_ssh/`, wrappers racine, alias `*_step2` et `step1b`
10. ouvrir un lot separe ulterieur pour tout retrait differe

Ordre machine recommande :

1. `db-layer`
2. `admin-trading`
3. `student`

Raison :

- `db-layer` possede deja la compat `step2`
- `admin-trading` valide le cas sans compat `step2` preexistante
- `student` garde le plus fort risque historique `step1b`

## Rollback attendu

Le rollback doit etre executable machine par machine.

Avant tout changement, capturer :

- `command -v menu-reseau_ssh`
- `command -v cmd-reseau_ssh`
- `command -v sanity-reseau_ssh`
- `readlink -f /usr/local/bin/menu-reseau_ssh`
- `readlink -f /usr/local/bin/cmd-reseau_ssh`
- `readlink -f /usr/local/bin/sanity-reseau_ssh`
- `command -v menu-reseau_ssh_step2 || true`
- `command -v cmd-reseau_ssh_step2 || true`
- `command -v sanity-reseau_ssh_step2 || true`
- presence et hash des wrappers racine
- presence de `scripts/reseau_ssh/`
- presence de `modules/reseau_ssh_step2/`

Rollback minimal :

| Surface | Restauration attendue |
| --- | --- |
| `menu-reseau_ssh` | restaurer la cible pre-migration capturee |
| `cmd-reseau_ssh` | restaurer la cible pre-migration capturee |
| `sanity-reseau_ssh` | restaurer la cible pre-migration capturee |
| alias `*_step2` | restaurer ou conserver l'etat pre-migration |
| `scripts/reseau_ssh/` | conserver intact pour retour arriere |
| wrappers racine | conserver intact ou restaurer depuis snapshot si lot futur les touche |
| `step1b` | conserver intact |

Rollback accepte seulement si les smoke tests reviennent a l'etat PASS sur la cible pre-migration.

## Smoke tests operatoires

Smoke tests avant et apres action, par machine :

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

Smoke tests compat `step2` quand presentes :

```bash
command -v menu-reseau_ssh_step2
command -v cmd-reseau_ssh_step2
command -v sanity-reseau_ssh_step2
sanity-reseau_ssh_step2
```

Smoke tests de conservation rollback :

```bash
test -d /opt/trading/scripts/reseau_ssh
test -d /opt/trading/modules/reseau_ssh_step2
test -e /opt/trading/scripts/reseau_ssh_cmd.sh
test -e /opt/trading/scripts/reseau_ssh_menu.sh
```

Les tests destructifs ou modifiant la configuration reseau sont exclus de ce cadrage.

## Criteres d'arret

Arret immediat si :

- inventaire initial incomplet sur une machine
- cible `modules/reseau_ssh_step2` absente ou incomplete
- rollback non ecrit ou non verifiable
- `sanity-reseau_ssh` echoue avant changement
- `cmd-reseau_ssh sanity` echoue avant changement
- smoke post-changement echoue
- divergence entre cible attendue et `readlink -f`
- presence d'un caller actif non classe sur wrapper racine ou `step1b`
- doute sur `student` lie a l'historique `step1b`

En cas d'arret :

- executer rollback sur la machine courante
- ne pas passer a la machine suivante
- consigner l'etat observe
- garder `NO_GO_PHYSICAL` pour les retraits

## Criteres de succes

Succes du futur lot physique initial seulement si :

- chaque machine cible a un inventaire initial documente
- chaque machine cible a un rollback documente
- les alias courts restent fonctionnels
- les alias courts pointent vers la cible finale prevue apres migration
- `modules/reseau_ssh_step2` est valide comme cible runtime effective
- `scripts/reseau_ssh/` reste disponible pour rollback initial
- wrappers racine ne sont pas retires dans la premiere phase
- `step1b` reste gele, non retire
- PASS machine par machine est documente

Ce succes ne vaut pas retrait automatique des compatibilites.

## Criteres de retrait differe

Un retrait ulterieur ne devient admissible qu'apres :

- periode de stabilite definie
- absence prouvee de callers actifs
- validation sur `admin-trading`, `db-layer`, `student`
- rollback teste
- accord documentaire explicite du parent `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
- ouverture d'un lot separe de retrait, si le retrait depasse le perimetre du GO physique initial

Retraits differees :

- wrappers racine
- alias `*_reseau_ssh_step2`
- `modules/reseau_ssh_step1b`
- `modules/reseau_ssh`
- archives historiques

## Exclusions explicites

Sont exclus de ce cadrage et de l'application initiale :

- modification de `fantome`
- refonte globale des scripts runtime
- retrait de wrappers racine
- suppression de compat `*_step2`
- suppression de `step1b`
- retrait de `scripts/reseau_ssh/`
- changement non documente des symlinks
- migration simultanee de plusieurs machines
- changement reseau destructif
- modification des docs hors GO sans lot separe

## Point de reprise

```text
GO ouvert en cadrage doc-only:
GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01

Etat de depart:
- c063ac1 publie
- cible finale unique decidee: modules/reseau_ssh_step2
- runtime final vise: alias courts menu/cmd/sanity
- NO_GO_PHYSICAL maintenu pour tout retrait ou application non preparee

Prochaine action admissible:
1) relire ce cadrage
2) verifier inventaires machine frais
3) valider rollback exact par machine
4) seulement ensuite autoriser une execution physique separee
```

## Verdict du cadrage

`PASS_CADRAGE_DOC_ONLY`

`NO_GO_PHYSICAL` maintenu jusqu'a execution separee, bornee et validee.

Ce document prepare l'application future. Il ne l'applique pas.
