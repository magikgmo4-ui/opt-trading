# OT-STARTERPACK-AUDIT-01 — REPORT (AUDIT STARTER PACK)

Date (America/Montreal) : 2026-03-14

## 1. RÉSUMÉ EXÉCUTIF (COURT)
- Le “starter pack canonique” existe, mais il est **distribué** entre `docs/master_pack/`, `workflow_ai/`, le kanban repo, et des packs TRAE parallèles.
- Points solides (ÉTABLI) : master pack “état canonique”, matrices runtime/entrypoints, kanban source of truth présent, et règle de clôture (doc+kanban+reprise) désormais écrite dans le workflow.
- Gaps principaux : **une référence de fichier manquante**, **naming de clôture incohérent** entre templates et la pratique OT_*.txt, et **absence d’un index unique** qui dise clairement “pour ouvrir une session, lire A→B→C”.
- Le starter pack est **utilisable**, mais pas encore “machine-first + opérationnel” au sens strict (réhydratation robuste après changement de session) sans intégrer explicitement la continuité (dernière clôture + kanban + point de reprise) dans le pack d’ouverture.

## 2. CORPUS AUDITÉ (PÉRIMÈTRE RÉEL)

### 2.1 Starter pack (Master Pack)
- [00_current_state_and_standards.md](file:///c:/Users/ghost/opt-trading/docs/master_pack/00_current_state_and_standards.md)
- [00_mission_start_guide.md](file:///c:/Users/ghost/opt-trading/docs/master_pack/mission_starter_pack/00_mission_start_guide.md)
- [01_mission_template.md](file:///c:/Users/ghost/opt-trading/docs/master_pack/mission_starter_pack/01_mission_template.md)
- [02_validation_checklist.md](file:///c:/Users/ghost/opt-trading/docs/master_pack/mission_starter_pack/02_validation_checklist.md)

### 2.2 Workflow (AI)
- [WORKFLOW.md](file:///c:/Users/ghost/opt-trading/workflow_ai/WORKFLOW.md)
- [specs.md](file:///c:/Users/ghost/opt-trading/workflow_ai/templates/specs.md)
- [tasks.md](file:///c:/Users/ghost/opt-trading/workflow_ai/templates/tasks.md)

### 2.3 Kanban/Roadmap/Index
- [opt_trading_kanban_source_of_truth_2026-03-13_updated.md](file:///c:/Users/ghost/opt-trading/opt_trading_kanban_source_of_truth_2026-03-13_updated.md)
- [docs/INDEX.md](file:///c:/Users/ghost/opt-trading/docs/INDEX.md)
- [docs/ROADMAP.md](file:///c:/Users/ghost/opt-trading/docs/ROADMAP.md)

### 2.4 Docs transverses explicitement appelées par le starter pack
- [OT_OPS_05_RUNTIME_EXCEPTION_MATRIX.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_OPS_05_RUNTIME_EXCEPTION_MATRIX.md)
- [OT_OPS_05B_DESK_PRO_ENTRYPOINT_MATRIX.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_OPS_05B_DESK_PRO_ENTRYPOINT_MATRIX.md)
- [OT_SVC_01_CANONICAL_RUNTIME_MAP.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_SVC_01_CANONICAL_RUNTIME_MAP.md)
- [OT_SVC_01_CLOSING.txt](file:///c:/Users/ghost/opt-trading/docs/ot/closings/OT_SVC_01_CLOSING.txt)

### 2.5 Packs TRAE (continuité / ouverture / clôture)
- [TRAE_SESSION_OPENING_PACK_V1.1.txt](file:///c:/Users/ghost/opt-trading/docs/ot/trae/trae_pack_texts/trae_pack/TRAE_SESSION_OPENING_PACK_V1.1.txt)
- [TRAE_CLOSURE_TEMPLATE_V1.1.txt](file:///c:/Users/ghost/opt-trading/docs/ot/trae/trae_pack_texts/trae_pack/TRAE_CLOSURE_TEMPLATE_V1.1.txt)

## 3. ÉTABLI (OPPOSABLE AU REPO)

### 3.1 Ce qui constitue le starter pack canonique aujourd’hui
- Noyau “projet” : `docs/master_pack/00_current_state_and_standards.md`.
- Pack “démarrage de mission” : `docs/master_pack/mission_starter_pack/*`.
- Workflow “gated” (AI) : `workflow_ai/WORKFLOW.md` + templates `specs.md` / `tasks.md`.
- Continuité “kanban” : un fichier kanban versionné et référencé : `opt_trading_kanban_source_of_truth_2026-03-13_updated.md`.

### 3.2 Indispensables pour ouvrir une session proprement (machine-first minimal)
Indispensables “ouverture / contexte / règles” :
- [00_mission_start_guide.md](file:///c:/Users/ghost/opt-trading/docs/master_pack/mission_starter_pack/00_mission_start_guide.md)
- [00_current_state_and_standards.md](file:///c:/Users/ghost/opt-trading/docs/master_pack/00_current_state_and_standards.md)
- [OT_OPS_05_RUNTIME_EXCEPTION_MATRIX.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_OPS_05_RUNTIME_EXCEPTION_MATRIX.md)
- [OT_OPS_05B_DESK_PRO_ENTRYPOINT_MATRIX.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_OPS_05B_DESK_PRO_ENTRYPOINT_MATRIX.md)

Indispensables “continuité / reprise” :
- [opt_trading_kanban_source_of_truth_2026-03-13_updated.md](file:///c:/Users/ghost/opt-trading/opt_trading_kanban_source_of_truth_2026-03-13_updated.md)
- Dernier fichier `OT_*_CLOSING*.txt` pertinent (selon le chantier) : non unique au repo, dépend de la mission.

### 3.3 Règle workflow “clôture = doc + kanban + point de reprise”
La règle est désormais explicitée dans :
- [WORKFLOW.md](file:///c:/Users/ghost/opt-trading/workflow_ai/WORKFLOW.md) (Gate Clôture)
- [specs.md](file:///c:/Users/ghost/opt-trading/workflow_ai/templates/specs.md) (DONE inclut doc/kanban/reprise)
- [tasks.md](file:///c:/Users/ghost/opt-trading/workflow_ai/templates/tasks.md) (Gate 6 = clôture)
- [00_mission_start_guide.md](file:///c:/Users/ghost/opt-trading/docs/master_pack/mission_starter_pack/00_mission_start_guide.md) (format de clôture inclut kanban)

### 3.4 Doctrine shared (état repo)
La doctrine “shared = surface canonique inter-machines” et l’UX `cmd-shared` sont intégrées au repo (master pack + module `shared` + kanban).

## 4. À CONFIRMER (BESOIN DE PREUVE OU D’ARBITRAGE)
- “GO/STOP” opérationnel : le workflow_ai décrit un gating humain systématique. À confirmer si c’est une règle réellement appliquée à chaque mission, ou un guide.
- Noyau d’ouverture de session : les packs TRAE (opening/closure) existent mais ne sont pas désignés comme sources obligatoires par le master pack. À confirmer : veut-on les rendre canoniques au niveau projet, ou les garder “hors bande”.
- Nommage canonique unique des livrables de clôture : à confirmer si on standardise `OT_*_CLOSING.txt` (observé) ou `OT_*_CLOSING_REPORT.txt` (template mission starter pack).

## 5. OBSOLÈTE / REDONDANT / NON ALIGNÉ

### 5.1 Non aligné (naming)
- [01_mission_template.md](file:///c:/Users/ghost/opt-trading/docs/master_pack/mission_starter_pack/01_mission_template.md) demande `OT_[ID]_CLOSING_REPORT.txt`, alors que le repo contient massivement des `OT_*_CLOSING.txt`.
- [00_mission_start_guide.md](file:///c:/Users/ghost/opt-trading/docs/master_pack/mission_starter_pack/00_mission_start_guide.md) mentionne `OT_XXX_CLOSING_REPORT.txt` (même écart).

### 5.2 Redondance structurelle
- `workflow_ai/templates/specs.md` et `docs/master_pack/mission_starter_pack/01_mission_template.md` se recouvrent (objectifs/contraintes/DONE/risques/plan), sans index canonique qui dit quel template prime.
- Les packs TRAE (opening/closure) fournissent aussi un modèle de continuité, mais ils ne sont pas intégrés au starter pack projet.

## 6. MANQUANTS (AU SENS STARTER PACK)
- Référence non alignée dans le master pack : `OT_OPS_04B_STUDENT_RUNTIME_FREEZE_NOTE.md` est référencé sans chemin canonique (voir [00_current_state_and_standards.md](file:///c:/Users/ghost/opt-trading/docs/master_pack/00_current_state_and_standards.md)). Le doc existe au repo et vit désormais sous `docs/ot/trae/OT_OPS_04B_STUDENT_RUNTIME_FREEZE_NOTE.md`.
- Index unique de starter pack : aucun fichier “STARTER_PACK_INDEX.md” qui impose un ordre de lecture unique incluant kanban + dernière clôture + reprise.
- Checklist fin de mission : [02_validation_checklist.md](file:///c:/Users/ghost/opt-trading/docs/master_pack/mission_starter_pack/02_validation_checklist.md) ne mentionne pas explicitement la mise à jour du kanban comme étape de clôture.

## 7. PROPOSITION DE STRUCTURE CIBLE (SANS REFACTOR IMMÉDIAT)
Structure cible minimale (documentaire) :
- `docs/master_pack/STARTER_PACK_INDEX.md` (nouveau) : ordre canonique “ouvrir session”.
- Référencer explicitement :
  - master pack (état canonique)
  - matrices runtime/entrypoints
  - workflow_ai (gates + templates)
  - kanban source of truth
  - la règle “clôture = doc + kanban + reprise”
  - la convention de nommage OT (report/closing/gap)

Objectif : réduire à **1 index** + **4–6 fichiers pivots** et rendre la reprise “compression proof”.

## 8. RÉPONSES EXPLICITES AUX QUESTIONS

### 1) Quel est exactement le starter pack canonique aujourd’hui ?
- `docs/master_pack/*` + `workflow_ai/*` + `opt_trading_kanban_source_of_truth_2026-03-13_updated.md` (et, selon le cas, les matrices OT_* appelées).

### 2) Quels fichiers sont indispensables pour ouvrir une session proprement ?
- `00_mission_start_guide.md`, `00_current_state_and_standards.md`, `OT_OPS_05*`, kanban source of truth, puis la dernière clôture OT pertinente.

### 3) Quels fichiers sont en double/flous/verbeux/non alignés ?
- Mission template vs specs/tasks workflow_ai (recouvrement).
- Nommage de clôture (CLOSING_REPORT vs CLOSING).
- Packs TRAE d’ouverture/clôture non raccordés au starter pack projet (parallèles).

### 4) Qu’est-ce qui manque pour être “machine-first + opérationnel” ?
- Un index unique “ouvrir session” incluant explicitement : kanban + dernière clôture + point de reprise + scan du réel.
- Une convention de nommage OT unique et appliquée dans templates.

### 5) La reprise après compression/changement de session est-elle robuste ?
- Partiellement : les éléments existent (kanban + packs TRAE), mais ils ne sont pas intégrés comme un noyau obligatoire dans le starter pack projet.

### 6) Le starter pack doit-il intégrer kanban+clôture+reprise comme noyau obligatoire ?
- Oui en doctrine workflow ; le repo l’a déjà commencé (workflow_ai + mission start guide), mais il manque l’index canonique d’ouverture et l’alignement des templates/checklists.

### 7) Structure cible plus simple ?
- Oui : un `STARTER_PACK_INDEX.md` unique qui référence les 4–6 pivots et impose un ordre de lecture.

## 9. POINT DE REPRISE RECOMMANDÉ
- Produire un patch documentaire minimal “OT-STARTERPACK-PATCH-01” :
  - ajouter l’index unique du starter pack,
  - corriger la référence OT_OPS_04B manquante,
  - aligner le naming des clôtures dans templates/checklists,
  - relier explicitement kanban + clôture + reprise à l’ouverture de session.
