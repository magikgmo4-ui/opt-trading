---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01_DECISIONS
doc_type: decisions
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01
status: open
lifecycle_stage: decisions
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01/01_architecture_cible.md
---

# 02_DECISIONS — GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01

## 1. Etat de depart

L'audit documentaire 6 sources est complet (PASS). La synthese architecturale est redigee en 10 axes dans `01_architecture_cible.md`.

## 2. Decisions

- Decision : l'architecture AI Team repose sur **trois couches** (orchestration + securite + metier).
- Decision : **Strict Workers est la couche de securite/execution obligatoire**, quel que soit le framework d'orchestration retenu.
- Decision : **aucun framework d'orchestration n'est fige** dans ce GO. Le choix est deferre au setup MVP.
- Decision : le **contrat d'integration Strict Workers** (tasks.index.json, denied inputs/commands, required_sections, smoke obligatoire) s'applique a tout worker.
- Decision : les **5 roles canoniques** (Observer, Analyzer, Documenter, Orchestrator, Gatekeeper) sont retenus comme base de l'equipe.
- Decision : le **MVP initial** peut demarrer avec 3 workers sur 1 tache READ_INVENTORY doc-only, sans sandbox Docker.
- Decision : le prochain GO est `GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01`.
- Decision : ce GO est **clos localement** (PASS), le parent AI Team reste OPEN.

## 3. Exclusions

- Aucun framework specifique retenu (ni LangGraph, ni CrewAI, ni autre).
- Aucun runtime modifie.
- Aucun worker implemente dans ce GO.
- Aucune decision de production.

## 4. Verdict

**PASS** — architecture cible livree, decisions bornees, next GO defini.

## 5. Point de reprise

Reprendre depuis `01_architecture_cible.md`, puis ouvrir `GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01`.
