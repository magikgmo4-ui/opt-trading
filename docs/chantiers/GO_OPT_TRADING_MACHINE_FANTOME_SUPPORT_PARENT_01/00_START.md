---
doc_id: GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01_START
doc_type: start
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01
status: open
lifecycle_stage: start
topic_keys:
  - opt-trading
  - machine_parent
  - fantome
  - ai_team
  - strict_workers
  - support
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/10_MACHINE_SCOPE.md
point_de_reprise: "7_CANONICAL_STATE"
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/10_MACHINE_SCOPE.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/20_EXISTING_BRANCHES_INVENTORY.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/30_CHILDREN_INDEX.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/40_AI_TEAM_LINK.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/50_STRICT_WORKERS_LINK.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/90_CLOSEOUT.md
  - docs/index/inbox/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01.md
---

# GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01 — 00_START

## 1_MASTER_TARGET

Ouvrir le parent machine/support `fantome` en doc-only, sur la base de l'arbitrage etabli :
`fantome = AI Team + Strict Workers / workspace support agents`.

## 2_INITIAL_PROJECT_DOC

Document de reference initial pour ce chantier parent machine :
`docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/10_MACHINE_SCOPE.md`

## 3_INITIAL_NEED

Le split machine avait differe `fantome` car le role support durable n'etait pas assez prouve.
L'arbitrage actuel leve l'ambiguite :
- `AI_TEAM + STRICT_WORKERS = fantome`
- `fantome = AI Team / Strict Workers / workspace support agents`

Il faut donc ouvrir un parent machine/support `fantome` qui :
- cadre la machine et ses children ;
- inventorie les branches/parents existants (AI_TEAM, STRICT_WORKERS) ;
- ne recree pas les parents existants (AI_TEAM est deja KEEP_ACTIVE) ;
- ne promeut pas STRICT_WORKERS sans audit ;
- ne fait aucune implementation runtime dans ce GO.

## 4_MASTER_PROJECT_PLAN

Direction validee :
1. Creer le parent machine/support fantome doc-only.
2. Inventorier les branches/parents existants (AI_TEAM, STRICT_WORKERS, save/fantome).
3. Cadrer les children sans les ouvrir.
4. Referencer AI_TEAM et STRICT_WORKERS comme liens explicites.
5. Preparer le GO de reconciliation comme prochaine etape.
6. Fermer le parent une fois l'ouverture validee.

## 5_GO_PLAN

Workstreams derives du parent machine fantome :
- GO_CHILD_01 : reconciliation AI Team + Strict Workers avec parent machine fantome ;
- GO_CHILD_02 : reprise implementation Strict Workers ou AI Team worker runtime review ;
- GO_CHILD_03 : audit complet Strict Workers avant promotion.

## 6_FINAL_TARGET

Livrable de cette phase :
- un parent machine fantome doc-only ;
- un inventaire complet des branches/parents existants ;
- des children cadres et proposes ;
- des liens explicites vers AI_TEAM et STRICT_WORKERS ;
- une inbox atomique pour l'agregation future.

## 7_CANONICAL_STATE

Etat canonique courant retenu :
- le parent machine fantome est ouvert en doc-only ;
- `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` existe comme parent actif (KEEP_ACTIVE) ;
- `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` existe mais reste a auditer avant promotion ;
- `save/fantome-YYYY-MM-DD` existe comme branche de sauvegarde ;
- aucun GO enfant machine fantome n'est encore ouvert ;
- la reconciliation AI Team + Strict Workers est le prochain GO logique.

NEXT_GO logique :
- `GO_OPT_TRADING_FANTOME_AI_TEAM_STRICT_WORKERS_RECONCILIATION_01`

## 8_VALIDATED_PLAN

Etapes validees vers la cible de phase :
1. Ouvrir le parent machine fantome.
2. Creer le set documentaire d'ouverture.
3. Inventorier les branches/parents existants.
4. Cadrer les children.
5. Referencer AI_TEAM et STRICT_WORKERS.
6. Commiter et pousser.

## 9_SELECTED_SOLUTION

Approche retenue :
- parent machine doc-only sur branche dediee ;
- set documentaire : `00_START.md`, `10_MACHINE_SCOPE.md`, `20_EXISTING_BRANCHES_INVENTORY.md`, `30_CHILDREN_INDEX.md`, `40_AI_TEAM_LINK.md`, `50_STRICT_WORKERS_LINK.md`, `90_CLOSEOUT.md` ;
- inbox atomique dans `docs/index/inbox/` ;
- aucune modification des index globaux ;
- aucun parent existant modifie (AI_TEAM conserve, STRICT_WORKERS reference sans promotion).

## 10_SELECTED_SETUP

Setup documentaire retenu pour le parent :
- `00_START.md` : cadre canonique complet ;
- `10_MACHINE_SCOPE.md` : perimetre de la machine fantome ;
- `20_EXISTING_BRANCHES_INVENTORY.md` : inventaire des branches/parents existants ;
- `30_CHILDREN_INDEX.md` : index des children proposes ;
- `40_AI_TEAM_LINK.md` : lien vers le parent AI Team ;
- `50_STRICT_WORKERS_LINK.md` : lien vers le parent Strict Workers ;
- `90_CLOSEOUT.md` : closeout du parent.

## 11_KEY_DECISIONS

- Le parent machine fantome est ouvert maintenant comme parent support/AI-workspace, pas comme runtime trading.
- `fantome = AI Team + Strict Workers`.
- `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` est deja KEEP_ACTIVE, on ne le recree pas.
- STRICT_WORKERS reste a auditer avant promotion complete.
- Le parent est strictement doc-only.
- La reconciliation AI Team + Strict Workers est le premier child recommande.

## 12_INVARIANTS

- Ne pas recreer AI_TEAM.
- Ne pas promouvoir STRICT_WORKERS sans audit.
- Ne pas modifier runtime.
- Ne pas toucher admin-trading.
- Ne pas toucher cursor-ai.
- Ne pas toucher student.
- Ne pas creer de parent decoratif.
- Ne pas modifier les index globaux sauf inbox atomique.

## 13_ESTABLISHED

- Le besoin d'un parent machine/support fantome est prouve.
- `AI_TEAM + STRICT_WORKERS = fantome` est arbitre.
- `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` est un parent actif et documente.
- `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` existe comme branche avec documents.
- Une branche `save/fantome-YYYY-MM-DD` existe.

## 14_HYPOTHESIS

- La reconciliation AI Team + Strict Workers pourra etre faite sans conflit.
- L'audit Strict Workers est necessaire mais peut etre differe au GO_CHILD_03.

## 15_REMAINING_GAP

Il manque encore :
- la reconciliation AI Team + Strict Workers avec le parent machine ;
- l'audit complet de STRICT_WORKERS avant promotion ;
- la decision sur le prochain GO d'implementation (Strict Workers reprise ou AI Team worker runtime review) ;
- le batch d'agregation des index globaux.

## 16_TODO

Actions suivantes concretes :
1. Creer le set documentaire complet.
2. Commiter et pousser la branche.
3. Inboxer l'entree atomique.
4. Preparer le GO de reconciliation.

## 17_RESUME_POINT

Reprendre depuis `7_CANONICAL_STATE`, puis rappeler `1_MASTER_TARGET`, `4_MASTER_PROJECT_PLAN`, replacer `5_GO_PLAN` et `6_FINAL_TARGET`, puis ouvrir le GO de reconciliation `GO_OPT_TRADING_FANTOME_AI_TEAM_STRICT_WORKERS_RECONCILIATION_01`.

## 19_TO_REMEMBER

TAGS :
- `NO_MEMORY`

Blocs :
- `AUCUN_AJOUT_MEMOIRE_DURABLE_AUTOMATIQUE`
