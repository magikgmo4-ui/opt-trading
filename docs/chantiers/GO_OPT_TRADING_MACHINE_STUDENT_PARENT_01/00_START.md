---
doc_id: GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01_START
doc_type: start
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01
status: open
lifecycle_stage: start
topic_keys:
  - opt-trading
  - machine_parent
  - student
  - local_ollama
  - openclaw_lab
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/10_MACHINE_SCOPE.md
point_de_reprise: "7_CANONICAL_STATE"
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/10_MACHINE_SCOPE.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/20_EXISTING_BRANCHES_INVENTORY.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/30_CHILDREN_INDEX.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/40_LOCAL_OLLAMA_LINK.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/90_CLOSEOUT.md
  - docs/index/inbox/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01.md
---

# GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01 — 00_START

## 1_MASTER_TARGET

Ouvrir le parent machine `student` en doc-only, sur la base de l'arbitrage etabli :
`student = Local Ollama / Student OpenClaw Lab / modeles locaux / experimentation machine`.

## 2_INITIAL_PROJECT_DOC

Document de reference initial pour ce chantier parent machine :
`docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/10_MACHINE_SCOPE.md`

## 3_INITIAL_NEED

Le split machine avait differe `student` car la frontiere machine/famille etait ambigue.
L'arbitrage actuel leve l'ambiguite :
- `OLLAMA = student`
- `student = Local Ollama / Student OpenClaw Lab`

Il faut donc ouvrir un parent machine `student` qui :
- cadre la machine et ses children ;
- inventorie les branches existantes (Local Ollama + Student OpenClaw Lab) ;
- ne fait aucune implementation runtime dans ce GO.

## 4_MASTER_PROJECT_PLAN

Direction validee :
1. Creer le parent machine student doc-only.
2. Inventorier les branches existantes de la famille.
3. Cadrer les children sans les ouvrir.
4. Referencer le parent Local Ollama.
5. Preparer le GO de reconciliation comme prochaine etape.
6. Fermer le parent une fois l'ouverture validee.

## 5_GO_PLAN

Workstreams derives du parent machine student :
- GO_CHILD_01 : reconciliation Local Ollama avec parent machine student ;
- GO_CHILD_02 : reprise implementation Ollama / OpenClaw Lab ;
- GO_CHILD_03 : evaluation modeles locaux ;
- GO_CHILD_04 : experimentation machine.

## 6_FINAL_TARGET

Livrable de cette phase :
- un parent machine student doc-only ;
- un inventaire complet des branches existantes ;
- des children cadres et proposes ;
- un lien explicite vers le parent Local Ollama ;
- une inbox atomique pour l'agregation future.

## 7_CANONICAL_STATE

Etat canonique courant retenu :
- le parent machine student est ouvert en doc-only ;
- `GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` existe comme branche active ;
- de nombreux enfants `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_*` existent ;
- aucun GO enfant machine student n'est encore ouvert ;
- la reconciliation Local Ollama + machine student est le prochain GO logique.

NEXT_GO logique :
- `GO_OPT_TRADING_STUDENT_LOCAL_OLLAMA_PARENT_RECONCILIATION_01`

## 8_VALIDATED_PLAN

Etapes validees vers la cible de phase :
1. Ouvrir le parent machine student.
2. Creer le set documentaire d'ouverture.
3. Inventorier les branches existantes.
4. Cadrer les children.
5. Referencer le parent Local Ollama.
6. Commiter et pousser.

## 9_SELECTED_SOLUTION

Approche retenue :
- parent machine doc-only sur branche dediee ;
- set documentaire : `00_START.md`, `10_MACHINE_SCOPE.md`, `20_EXISTING_BRANCHES_INVENTORY.md`, `30_CHILDREN_INDEX.md`, `40_LOCAL_OLLAMA_LINK.md`, `90_CLOSEOUT.md` ;
- inbox atomique dans `docs/index/inbox/` ;
- aucune modification des index globaux.

## 10_SELECTED_SETUP

Setup documentaire retenu pour le parent :
- `00_START.md` : cadre canonique complet ;
- `10_MACHINE_SCOPE.md` : perimetre de la machine student ;
- `20_EXISTING_BRANCHES_INVENTORY.md` : inventaire des branches existantes ;
- `30_CHILDREN_INDEX.md` : index des children proposes ;
- `40_LOCAL_OLLAMA_LINK.md` : lien vers le parent Local Ollama ;
- `90_CLOSEOUT.md` : closeout du parent.

## 11_KEY_DECISIONS

- Le parent machine student est ouvert maintenant, la frontiere etant claire.
- `student = Local Ollama / Student OpenClaw Lab / modeles locaux / experimentation machine`.
- Le parent est strictement doc-only.
- La reconciliation Local Ollama est le premier child recommande.
- Aucune installation Ollama, aucune modification runtime dans ce GO.

## 12_INVARIANTS

- Ne pas modifier les index globaux sauf inbox atomique.
- Ne pas modifier Local Ollama runtime.
- Ne pas installer Ollama.
- Ne pas modifier OpenClaw.
- Ne pas toucher admin-trading.
- Ne pas toucher cursor-ai.
- Ne pas creer de parent fourre-tout.

## 13_ESTABLISHED

- Le besoin d'un parent machine student est prouve par les branches existantes.
- La frontiere `OLLAMA = student` est arbitree.
- `GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` est la branche parent Local Ollama existante.
- De nombreux enfants `STUDENT_OPENCLAW_LAB_*` existent deja.

## 14_HYPOTHESIS

- La reconciliation Local Ollama / machine student sera simple (branches deja existantes).
- L'implementation Ollama pourra reprendre apres reconciliation.

## 15_REMAINING_GAP

Il manque encore :
- la reconciliation des branches Local Ollama avec le parent machine ;
- la reprise de l'implementation Ollama / OpenClaw Lab ;
- l'evaluation des modeles locaux ;
- le batch d'agregation des index globaux.

## 16_TODO

Actions suivantes concretes :
1. Creer le set documentaire complet.
2. Commiter et pousser la branche.
3. Inboxer l'entree atomique.
4. Preparer le GO de reconciliation.

## 17_RESUME_POINT

Reprendre depuis `7_CANONICAL_STATE`, puis rappeler `1_MASTER_TARGET`, `4_MASTER_PROJECT_PLAN`, replacer `5_GO_PLAN` et `6_FINAL_TARGET`, puis ouvrir le GO de reconciliation `GO_OPT_TRADING_STUDENT_LOCAL_OLLAMA_PARENT_RECONCILIATION_01`.

## 19_TO_REMEMBER

TAGS :
- `NO_MEMORY`

Blocs :
- `AUCUN_AJOUT_MEMOIRE_DURABLE_AUTOMATIQUE`
