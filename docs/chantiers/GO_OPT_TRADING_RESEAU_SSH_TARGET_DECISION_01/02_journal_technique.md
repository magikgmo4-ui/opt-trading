---
doc_id: GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01_JOURNAL_TECHNIQUE
doc_type: chantier_journal_technique
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01
status: open
lifecycle_stage: decision_doc_only
topic_keys:
  - opt-trading
  - reseau_ssh
  - target_decision
  - journal
  - no_go_physical
surface: docs
source_kind: canonical
updated_at: 2026-04-20
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/03_decisions.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01/00_cadrage.md
  - docs/status/reseau_ssh_canonique.md
---

# GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01 - Journal technique

## Etat de depart retenu

Lecture repo-first du GO doc-only ouvert :
- dossier de chantier : `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/`
- cadrage present : `00_cadrage.md`
- fichiers completes dans ce lot : `02_journal_technique.md`, `03_decisions.md`

Etat Git observe avant intervention :
- branche de travail : `sot/mainline`
- suivi distant : `origin/sot/mainline`
- dossier `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/` non suivi au depart
- modifications existantes hors perimetre conservees intactes

Perimetre applique :
- documentation uniquement
- aucun retrait
- aucun renommage
- aucun repointage
- aucun patch machine
- aucun runtime touche
- aucun wrapper, symlink, alias ou surface `fantome` touche
- `NO_GO_PHYSICAL` maintenu

## Constats repris du cadrage

Etat acquis :
- canon operateur actuel : `scripts/reseau_ssh/`
- survivant de famille : `modules/reseau_ssh_step2`
- `modules/reseau_ssh_step2` n'est pas encore canon operateur
- `modules/reseau_ssh_step1b` reste legacy / compat a risque
- wrappers racine presents sur les machines Linux auditees
- compat `*_reseau_ssh_step2` deployee sur `db-layer` et `student`
- compat `*_reseau_ssh_step2` absente sur `admin-trading`

Cette etape ne transforme aucun de ces constats en mutation physique.

## Cible finale unique

La cible finale unique de la famille `reseau_ssh` est :

`modules/reseau_ssh_step2`

Ancrage :
- `modules/reseau_ssh_step2` est la cible de convergence future
- `modules/reseau_ssh_step1b` ne devient pas cible finale
- `modules/reseau_ssh` ne devient pas cible finale
- aucune nouvelle cible unifiee n'est creee dans ce GO

## Runtime final vise

Le runtime final vise reste centre sur les alias courts stables :
- `menu-reseau_ssh`
- `cmd-reseau_ssh`
- `sanity-reseau_ssh`

Ancrage :
- les alias courts restent le contrat operateur stable
- l'implementation future visee est issue de `modules/reseau_ssh_step2`
- `scripts/reseau_ssh/` reste canon operateur actuel tant que la migration physique separee n'est pas ouverte et validee
- les alias `*_reseau_ssh_step2` restent des compatibilites transitoires, pas le contrat final

## Statuts finals vises

| Surface | Statut actuel retenu | Statut final vise | Garde-fou |
| --- | --- | --- | --- |
| `modules/reseau_ssh_step2` | survivant de famille / compat transitoire | cible module unique finale | promotion physique seulement dans GO separe |
| `modules/reseau_ssh_step1b` | legacy / compat a risque | legacy gele puis archive possible | aucun retrait dans ce GO |
| `scripts/reseau_ssh/` | canon operateur actuel | compat runtime transitoire puis archive/legacy apres migration validee | conserver pour rollback |
| wrappers racine `scripts/reseau_ssh_cmd.sh`, `scripts/reseau_ssh_menu.sh` | candidate-retire-later | retrait differe possible | aucun retrait avant preuve d'absence de callers |
| alias courts | canon operateur actuel | interface operateur finale | conserver comme contrat utilisateur |
| alias `*_reseau_ssh_step2` | compat transitoire sur certaines machines | retrait ou gel apres bascule stable | retrait differe machine par machine |

## Mapping actuel vers final

| Surface actuelle | Final vise | Action future admissible | Rollback attendu | Smoke minimal |
| --- | --- | --- | --- | --- |
| `/usr/local/bin/menu-reseau_ssh` | alias court conserve vers cible `step2` | repointage en GO physique uniquement | restaurer cible vers `scripts/reseau_ssh/reseau_ssh_menu.sh` | `menu-reseau_ssh` ouvre le menu |
| `/usr/local/bin/cmd-reseau_ssh` | alias court conserve vers cible `step2` | repointage en GO physique uniquement | restaurer cible vers `scripts/reseau_ssh/reseau_ssh_cmd.sh` | `cmd-reseau_ssh sanity` |
| `/usr/local/bin/sanity-reseau_ssh` | alias court conserve vers cible `step2` | repointage en GO physique uniquement | restaurer cible vers `scripts/reseau_ssh/sanity_reseau_ssh.sh` | `sanity-reseau_ssh` |
| `/usr/local/bin/*_reseau_ssh_step2` | compat temporaire | conserver pendant migration | restaurer symlink `step2` si besoin | smoke `*_reseau_ssh_step2` avant/apres |
| `/opt/trading/scripts/reseau_ssh/` | runtime actuel puis compat/archive | conserver pendant migration initiale | laisser intact | smoke scripts directs |
| `/opt/trading/modules/reseau_ssh_step2/` | cible finale | installer/valider comme cible unique | revenir aux alias courts vers `scripts/reseau_ssh/` | sanity module et commandes non destructives |
| `/opt/trading/scripts/reseau_ssh_cmd.sh` | retrait differe possible | aucun retrait initial | restaurer depuis backup si retrait futur valide | verifier absence de callers |
| `/opt/trading/scripts/reseau_ssh_menu.sh` | retrait differe possible | aucun retrait initial | restaurer depuis backup si retrait futur valide | verifier absence de callers |
| `modules/reseau_ssh_step1b` | legacy gele / archive future | geler, ne pas retirer initialement | conserver copie intacte | verifier absence d'appel actif |

## Rollback a exiger du futur GO physique

Le futur GO physique devra documenter avant execution :
- snapshot des alias courts
- snapshot des alias `*_reseau_ssh_step2` quand presents
- cibles `readlink -f` avant mutation
- copie ou hash des wrappers racine avant toute action
- commande de restauration par machine
- critere d'abandon si un smoke echoue

Rollback minimal :
- restaurer les alias courts vers `scripts/reseau_ssh/`
- conserver `scripts/reseau_ssh/` intact
- conserver les wrappers racine
- conserver `modules/reseau_ssh_step1b`
- annuler toute promotion de `modules/reseau_ssh_step2` si smoke KO

## Smoke tests a exiger du futur GO physique

Par machine :
- `command -v menu-reseau_ssh`
- `command -v cmd-reseau_ssh`
- `command -v sanity-reseau_ssh`
- `readlink -f /usr/local/bin/menu-reseau_ssh`
- `readlink -f /usr/local/bin/cmd-reseau_ssh`
- `readlink -f /usr/local/bin/sanity-reseau_ssh`
- `sanity-reseau_ssh`
- `cmd-reseau_ssh sanity`
- test menu non destructif
- verification de presence de `scripts/reseau_ssh/` pour rollback

Pour les machines avec compat `step2` :
- `command -v menu-reseau_ssh_step2`
- `command -v cmd-reseau_ssh_step2`
- `command -v sanity-reseau_ssh_step2`
- `sanity-reseau_ssh_step2`

## Criteres de retrait differe

Un retrait futur ne devient admissible que si :
- les alias courts fonctionnent sur la cible finale pendant une periode de stabilite definie
- aucun caller actif des wrappers racine n'est prouve
- `modules/reseau_ssh_step1b` est classe historique seulement, sans usage actif
- rollback teste
- chaque machine a un etat final documente
- le parent `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` accepte explicitement la suite physique

Retraits explicitement differes :
- wrappers racine
- alias `*_reseau_ssh_step2`
- surfaces `step1b`
- surfaces `modules/reseau_ssh`

## Reprise

Le futur GO physique separe reste :

`GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01`

Ce journal n'ouvre aucun droit d'execution. Il consolide la decision doc-only et maintient `NO_GO_PHYSICAL`.

## RISKS

- À qualifier.
