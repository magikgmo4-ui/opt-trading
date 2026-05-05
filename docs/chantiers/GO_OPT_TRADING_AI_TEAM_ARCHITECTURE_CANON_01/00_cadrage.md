---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01
status: open
lifecycle_stage: cadrage
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/01_initial_project_doc.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_DOC_AUDIT_01/02_journal_technique.md
  - docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
  - docs/agents/strict_workers/MODELS_MATRIX_01.md
  - scripts/ai/workers/tasks.index.json
---

# GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01 — 00_cadrage

## 1_MASTER_TARGET

Produire une synthese d'architecture cible interne pour l'AI Team, en transformant l'audit documentaire 6 sources en une architecture canonique exploitable, sans choisir de stack finale.

## 3_INITIAL_NEED

L'audit documentaire `GO_OPT_TRADING_AI_TEAM_DOC_AUDIT_01` a couvert 6 sources (Marblism, CrewAI, LangGraph, AutoGen, OpenAI Agents SDK, Strict Workers interne). L'etape suivante consiste a synthetiser ces elements en une architecture cible par axes, utilisable comme socle pour le setup MVP.

## 4_MASTER_PROJECT_PLAN

1. Reprendre la matrice comparative (journal technique L124-158).
2. Extraire les primitives indispensables vs options confort vs dependances ecosysteme.
3. Articuler Strict Workers comme couche de securite/execution.
4. Produire l'architecture cible par axes (roles, orchestration, memoire, HITL, surfaces, observabilite, securite).
5. Borne les decisions sans figer une stack finale.
6. Identifier les gaps avant MVP.
7. Definir le prochain GO : `GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01`.

## 7_CANONICAL_STATE

- Parent : `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`
- Base audit : `GO_OPT_TRADING_AI_TEAM_DOC_AUDIT_01` (PASS)
- Strict Workers : seed artefact interne, branche `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01`
- Branche de travail : `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`
- Type : doc-only, aucun runtime modifie

## 11_KEY_DECISIONS

- Aucune stack finale n'est retenue dans ce GO.
- Strict Workers est traite comme couche de securite/execution, pas comme framework d'orchestration.
- L'architecture cible doit etre lisible independamment du choix de framework.
- Les axes de conception sont derives du besoin produit (pattern Marblism + trading), pas de preferences techniques.

## 12_INVARIANTS

- Doc-only.
- Ne pas fermer le parent AI Team.
- Ne pas ouvrir ClickUp.
- Ne pas toucher au runtime.
- Ne pas patcher MATRICE_DOC_OPS sauf gap bloquant.
- Ne pas restaurer le stash reseau_ssh.

## 16_TODO

1. Rediger `01_architecture_cible.md`.
2. Rediger `02_decisions.md`.
3. Valider coherence avec Strict Workers.
4. Fermer ce GO si l'architecture est exploitable pour le MVP.

## 17_RESUME_POINT

Reprendre depuis `01_architecture_cible.md`, recroiser avec la matrice comparative du journal technique, puis ouvrir `GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01`.
