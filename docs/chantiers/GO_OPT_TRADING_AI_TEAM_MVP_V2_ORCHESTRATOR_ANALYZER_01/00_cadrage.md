---
doc_id: GO_OPT_TRADING_AI_TEAM_MVP_V2_ORCHESTRATOR_ANALYZER_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_MVP_V2_ORCHESTRATOR_ANALYZER_01
status: open
lifecycle_stage: cadrage
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01/01_architecture_cible.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_OBSERVER_DOC_DRAFT_01/90_CLOSEOUT.md
---

# GO_OPT_TRADING_AI_TEAM_MVP_V2_ORCHESTRATOR_ANALYZER_01 — 00_cadrage

## 1_MASTER_TARGET

Etendre le MVP AI Team en v2 avec les roles Analyzer et Orchestrator, en ajoutant la tache ANALYZE_INVENTORY et une chaine orchestrator bornée, sans sortir du cadre Strict Workers.

## 3_INITIAL_NEED

Le runner supporte deja READ_INVENTORY et DOC_DRAFT. Les 5 roles de l'Architecture Canon sont definis mais seuls 3 sont implementes (Observer, Documenter, Gatekeeper). Les 2 roles manquants (Analyzer, Orchestrator) doivent etre ajoutes pour completer la chaine de travail MVP.

## 4_MASTER_PROJECT_PLAN

1. Definir le contrat de chaine Orchestrator.
2. Ajouter le task type ANALYZE_INVENTORY.
3. Ajouter le task type ORCHESTRATOR_CHAIN.
4. Etendre le runner avec les 2 nouveaux handlers.
5. Creer le task packet analyze_inventory.json.
6. Creer le task packet orchestrator_chain_v2.json (chaîne des 3).
7. Executer la chaîne complète.
8. Valider smoke v2.
9. Documenter les limites.

## 5_GO_PLAN

```
Workers MVP v2:
  Observer (READ_INVENTORY) → Analyzer (ANALYZE_INVENTORY) → Documenter (DOC_DRAFT)
                                  ↑                              ↑
                            Orchestrator (chaine les 3, pas de git write)
                                  ↑
                            Gatekeeper (validation HITL, bloque denied_commands)
```

## 7_CANONICAL_STATE

- Parent : GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 (OPEN)
- MVP v1 (3 workers, READ_INVENTORY + DOC_DRAFT) : PASS
- Runner supporte : READ_INVENTORY, DOC_DRAFT
- Type : doc-only + runner write limité à drafts/

## 11_KEY_DECISIONS

- Analyzer produit une ANALYZE_INVENTORY (classification, stats, patterns).
- Orchestrator est un meta-task qui chaîne des sous-tâches sans git write.
- La chaîne v2 est : READ_INVENTORY → ANALYZE_INVENTORY → DOC_DRAFT.
- Gatekeeper reste validation humaine.
- Aucun git write depuis le runner.
- ClickUp différé.

## 12_INVARIANTS

- Doc-only, write limité à drafts/.
- Ne pas ouvrir ClickUp.
- Ne pas restaurer ni drop le stash reseau_ssh.
- Aucun write runtime trading.
- Aucun secret, .env, token, credential.
- Aucun git write depuis le runner.

## 16_TODO

1. Rediger `01_v2_spec.md`.
2. Rediger `02_chain_contract.md`.
3. Creer `modules/ai_team_mvp/tasks/analyze_inventory.json`.
4. Creer `modules/ai_team_mvp/tasks/orchestrator_chain_v2.json`.
5. Etendre `modules/ai_team_mvp/runner.py` (ANALYZE_INVENTORY + ORCHESTRATOR_CHAIN).
6. Executer la chaîne complète.
7. Rediger `03_smoke_report.md`.
8. Rediger `90_CLOSEOUT.md`.

## 17_RESUME_POINT

Reprendre depuis `01_v2_spec.md`, étendre le runner, exécuter la chaîne, valider.
