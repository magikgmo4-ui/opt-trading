---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_STEP_04_NOTE
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - step-04
  - alignement
  - documentation
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/94_plan_execution_step_by_step.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - docs/governance/REPO_ROOT_POLICY.md
---

# Step 04 — alignement documentaire top-level

## Statut
Complete.

## Objectif
Corriger les ecarts simples entre la documentation canonique top-level et l'etat reel observe a la racine du repo.

## Scope
- `docs/architecture/REPO_SURFACES_MAP.md`
- `docs/governance/REPO_ROOT_POLICY.md`

## Verifications utilisees
- lecture de `REPO_SURFACES_MAP.md`
- lecture de `REPO_ROOT_POLICY.md`
- listing des repertoires top-level via `Get-ChildItem -Force -Directory`
- listing des fichiers racine via `Get-ChildItem -Force -File`

## Preuves observees

### 1. Top-level reel observe au 2026-04-24
Repertoires :
- `adapters`
- `audit`
- `contracts`
- `data`
- `deploy_module_multi_machine`
- `docs`
- `modules`
- `packages`
- `perf`
- `registry`
- `schemas`
- `scripts`
- `shared`
- `state`
- `student`
- `tests`
- `tmp`
- `tools`
- `tradingview`
- `workflow_ai`
- plus surfaces locales : `_archive`, `__pycache__`, `.ruff_cache`, `.secrets`, `.uv-cache`, `.uv-python`

Fichiers racine :
- `.env.example`
- `README.md`
- `requirements.txt`
- `webhook_server.py`
- `bitget_bridge.py`

### 2. Ecarts constates avant correction
- `REPO_SURFACES_MAP.md` mentionnait `infra_context_sanitized/`, absent du top-level reel.
- `REPO_SURFACES_MAP.md` ne listait pas explicitement plusieurs surfaces top-level reelles : `state/`, `data/`, `contracts/`, `audit/`, `tests/`.
- `REPO_ROOT_POLICY.md` ne fixait pas clairement la racine minimale de fichiers observee au top-level.
- `REPO_ROOT_POLICY.md` ne gelait pas assez explicitement la regle "pas de nouveau support a la racine".

## Decisions appliquees

### Decision 1
`REPO_SURFACES_MAP.md` est realigne sur les surfaces top-level reelles observees.

Effets :
- suppression de `infra_context_sanitized/`
- ajout explicite de `state/`, `data/`, `contracts/`, `audit/`, `tests/`
- ajout d'une section locale/archive plus explicite

### Decision 2
`REPO_ROOT_POLICY.md` est recentre sur la discipline racine.

Effets :
- articulation explicite avec `REPO_SURFACES_MAP.md`
- definition claire des fichiers racine legitimes
- ajout de la regle "aucun nouveau support a la racine"
- ajout d'un garde-fou sur les surfaces local-only

## Fichiers modifies
- `docs/architecture/REPO_SURFACES_MAP.md`
- `docs/governance/REPO_ROOT_POLICY.md`
- `docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/94_plan_execution_step_by_step.md`

## Rollback
- revert doc-only de `REPO_SURFACES_MAP.md`
- revert doc-only de `REPO_ROOT_POLICY.md`
- revert doc-only de `94_plan_execution_step_by_step.md`
- suppression de cette note si le step est annule

## Resultat
Le parent dispose maintenant d'un premier lot execute et trace. Le canon top-level est aligne avec l'etat reel sans move physique.

## Point de reprise
Passer au `Step 05` pour auditer les exceptions racine, d'abord `webhook_server.py` puis `bitget_bridge.py`.
