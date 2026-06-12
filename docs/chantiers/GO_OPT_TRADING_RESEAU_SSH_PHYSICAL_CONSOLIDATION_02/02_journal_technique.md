---
doc_id: GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02_JOURNAL_TECHNIQUE
doc_type: chantier_journal_technique
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02
status: blocked
lifecycle_stage: execution_machine_01_blocked
topic_keys:
  - opt-trading
  - reseau_ssh
  - physical
  - db_layer
  - smoke_tests
  - rollback
  - blocked
surface: runtime
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02/03_decisions.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/03_decisions.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/00_cadrage.md
  - docs/status/reseau_ssh_canonique.md
---

# GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02 - Journal technique

## Etat reel etabli sur machine 01

Machine 01 de ce GO :

`db-layer`

Baseline reelle executee en lecture seule.

Etat operateur reel constate avant toute mutation :

- `menu-reseau_ssh` pointe vers `/opt/trading/scripts/reseau_ssh/reseau_ssh_menu.sh`
- `cmd-reseau_ssh` pointe vers `/opt/trading/scripts/reseau_ssh/reseau_ssh_cmd.sh`
- `sanity-reseau_ssh` pointe vers `/opt/trading/scripts/reseau_ssh/sanity_reseau_ssh.sh`

Etat `step2` constate present sur la machine :

- `menu-reseau_ssh_step2` pointe vers `/opt/trading/modules/reseau_ssh_step2/scripts/menu.sh`
- `cmd-reseau_ssh_step2` pointe vers `/opt/trading/modules/reseau_ssh_step2/scripts/cmd.sh`
- `sanity-reseau_ssh_step2` pointe vers `/opt/trading/modules/reseau_ssh_step2/scripts/sanity_check.sh`

Conclusion de baseline :

- `db-layer` est joignable et auditable
- les alias courts operateur reels pointent encore vers le canon actuel `scripts/reseau_ssh`
- les wrappers racine sur `db-layer` restent intacts
- le rollback a ete prepare et reste disponible
- aucune mutation machine n'a ete appliquee dans cette sequence

## Resultats des smokes avant bascule

Smokes executes avant toute tentative de repointage :

- `sanity-reseau_ssh` = `PASS`
- `cmd-reseau_ssh sanity` = `PASS`
- `sanity-reseau_ssh_step2` = `FAIL`

Interpretation retenue :

- la baseline a reussi
- la methode de verification avant mutation a fonctionne
- le blocage ne concerne pas le GO de baseline lui-meme
- le blocage concerne la bascule des alias courts vers `step2`

## Cause bloquante observee

Cause fonctionnelle observee sur le runtime `step2` :

- le wrapper `step2` appele via `/usr/local/bin/sanity-reseau_ssh_step2` resout son root de module vers `/usr/local`
- la logique actuelle de calcul a partir de `${0%/*}/..` n'est pas operateur-reelle lorsqu'elle est invoquee via symlink
- la resolution de chemin derive donc vers un faux module root
- l'execution echoue ensuite sur `FAIL: scripts missing`

Ancrage de cause :

- ce n'est pas un probleme reseau
- ce n'est pas un probleme SSH
- ce n'est pas un probleme machine
- c'est un defaut fonctionnel de forme runtime sur `reseau_ssh_step2`

## Portee du blocage

Le lot physique `GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02` est bloque en bascule.

Etat exact du GO a ce stade :

- `PASS` de baseline machine
- `PASS` des commandes operateur actuelles
- `FAIL` du smoke `step2` operateur reel
- rollback pret mais non utilise
- aucune mutation des alias courts effectuee

Ce journal ancre donc le constat suivant :

- la baseline machine est valide
- la bascule des alias courts vers `step2` n'est pas autorisable a ce stade
- le verdict correct du GO physique courant est `BLOQUE`

## Suite correcte retenue

La suite correcte n'est pas un patch physique immediat sur `db-layer`.

La suite correcte est separee en deux temps :

1. cloturer la baseline bloquante dans le GO physique courant
2. ouvrir un lot separe de correction minimale de forme runtime pour `reseau_ssh_step2`

Point de reprise avant toute requalification de bascule :

- corriger en repo la resolution de chemin de `step2`
- republier le correctif
- rejouer `sanity-reseau_ssh_step2` sur machine reelle via alias/wrapper installe
- requalifier ensuite seulement le repointage des alias courts

## Tags documentaires

- `ETABLI`
- `BLOQUE`
- `RESEAU_SSH`
- `DB_LAYER`
- `SMOKE_TEST`
- `ROLLBACK`
- `NO_MEMORY`

## RISKS

- À qualifier.
