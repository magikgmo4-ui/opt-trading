---
doc_id: GO_OPT_TRADING_AI_TEAM_REGISTRY_CONSOLIDATION_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_REGISTRY_CONSOLIDATION_01
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
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_MVP_V2_ORCHESTRATOR_ANALYZER_01/90_CLOSEOUT.md
---

# GO_OPT_TRADING_AI_TEAM_REGISTRY_CONSOLIDATION_01 — 00_cadrage

## 1_MASTER_TARGET

Consolider un registre canonique AI Team decrivant les workers, task types, contrats d'entree/sortie, garde-fous, outputs et smokes valides, dans des fichiers JSON structurants et un mapping documentaire lisible.

## 3_INITIAL_NEED

Le MVP a produit 4 task types, 4 workers, 4 task packets, des outputs drafts et 3 series de smoke PASS. Ces elements existent mais ne sont pas references dans un registre centralise. Le registre permettra la tracabilite, la reprise et l'extension future.

## 4_MASTER_PROJECT_PLAN

1. Creer `workers.registry.json` (5 roles Architecture Canon).
2. Creer `tasks.registry.json` (4 task types implementes).
3. Creer `outputs.registry.json` (drafts et intermediates).
4. Rediger `01_registry_map.md` (mapping lisible).
5. Rediger `02_smoke_matrix.md` (trace des smokes PASS).
6. Valider coherence avec Architecture Canon.
7. Clore.

## 7_CANONICAL_STATE

- Parent : GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 (OPEN)
- MVP v1 (3 workers, READ_INVENTORY + DOC_DRAFT) : PASS
- MVP v2 (+ANALYZE_INVENTORY + ORCHESTRATOR_CHAIN) : PASS
- Runner : 4 task types, 4 workers actifs
- Gatekeeper : validation humaine
- Type : doc-only + registry JSON

## 11_KEY_DECISIONS

- Les registres sont en JSON pour etre lisibles par le runner et par les humains.
- Les 5 roles de l'Architecture Canon sont tous references, y compris Gatekeeper (HITL).
- Les smokes PASS sont traces avec date et criteres.
- Aucun output draft n'est promu en canon sans revue.
- Les registres sont versionnes dans le repo.

## 12_INVARIANTS

- Doc-only + registry JSON.
- Ne pas ouvrir ClickUp.
- Ne pas toucher au runtime trading.
- Aucun write hors chantier/registry.
- Aucun secret, .env, token, credential.

## 16_TODO

1. Creer `modules/ai_team_mvp/registry/workers.registry.json`.
2. Creer `modules/ai_team_mvp/registry/tasks.registry.json`.
3. Creer `modules/ai_team_mvp/registry/outputs.registry.json`.
4. Rediger `01_registry_map.md`.
5. Rediger `02_smoke_matrix.md`.
6. Rediger `90_CLOSEOUT.md`.

## 17_RESUME_POINT

Reprendre depuis `modules/ai_team_mvp/registry/`, verifier la coherence des registres avec l'Architecture Canon.
