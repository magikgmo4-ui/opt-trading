---
doc_id: GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02_DECISIONS
doc_type: chantier_decisions
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
  - blocked
  - rollback
  - step2
surface: runtime
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02/02_journal_technique.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/03_decisions.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/00_cadrage.md
---

# GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02 - Decisions

## Verdict

Verdict du GO physique courant :

`BLOQUE`

Formulation canonique :

- `FAIL` de bascule
- `PASS` de baseline

Le blocage porte sur la bascule des alias courts vers `step2`, pas sur la validite de la baseline elle-meme.

## Decisions immediates

Decisions retenues maintenant :

- ne pas repointer `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh` vers `step2`
- ne pas toucher les wrappers racine sur `db-layer`
- ne faire aucune mutation machine supplementaire dans ce GO
- ancrer le constat documentaire de baseline bloquante dans ce lot physique
- conserver le rollback prepare comme filet de securite non utilise

## Non-autorisations explicites

Restent non autorises dans ce GO :

- toute bascule des alias courts vers `modules/reseau_ssh_step2`
- tout patch physique immediat sur `db-layer`
- toute extension a une machine 02
- tout retrait de `scripts/reseau_ssh/`
- tout retrait des wrappers racine
- tout retrait des alias `*_reseau_ssh_step2`

## Cause decisionnelle retenue

La cause retenue pour bloquer la bascule est :

- `sanity-reseau_ssh_step2` echoue en condition operateur reelle
- la resolution de root module de `step2` est incorrecte sous symlink
- le defaut est un defaut de forme runtime

Hypothese forte a valider dans un lot separe :

- la correction minimale probable porte sur la logique de resolution du chemin reel du script execute
- la correction devra partir du chemin reel du fichier et non du chemin du symlink invoque

Cette hypothese oriente le futur correctif, mais ne vaut pas patch valide dans ce GO.

## Suite correcte

La suite correcte est l'ouverture d'un lot separe de correction minimale `step2` avant toute reprise physique de la consolidation.

Mission de ce lot separe :

- corriger la resolution de chemin du script `step2`
- prouver que `step2` fonctionne comme operateur reel quand il est appele via alias ou wrapper installe
- revalider `sanity-reseau_ssh_step2` sur machine reelle

Point de reprise du GO physique courant :

- republier le correctif minimal
- revenir sur `db-layer`
- rejouer les smokes `step2`
- si `PASS`, requalifier seulement alors la question du repointage des alias courts

## Statut final de ce document

Ce document fige le cadre suivant :

- baseline machine `db-layer` : faite
- methode de baseline : valide
- bascule des alias courts : non autorisable
- rollback : pret et non utilise
- suite correcte : lot separe de correction minimale runtime `step2`

## RISKS

- À qualifier.
