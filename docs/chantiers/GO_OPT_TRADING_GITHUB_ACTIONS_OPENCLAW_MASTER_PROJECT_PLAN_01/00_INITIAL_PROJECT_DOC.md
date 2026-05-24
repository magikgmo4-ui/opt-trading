---
doc_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
GO_STRUCTURAL_ROLE: GO_MASTER_PROJECT_PLAN
PF_ID: PF_OPT_TRADING
MASTER_TARGET_ID: MT_GITHUB_ACTIONS_OPENCLAW_01
MASTER_PROJECT_PLAN_ID: MPP_GITHUB_ACTIONS_OPENCLAW_01
PARENT_GO_ID: null
NEXT_ATTACH_TARGET: null
status: draft_opening_bundle
lifecycle_stage: planning
surface: github_actions_openclaw
source_kind: canonical_opening_bundle
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 00_INITIAL_PROJECT_DOC — GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01

## 1_MASTER_TARGET

`github_actions_openclaw`

## 2_INITIAL_PROJECT_DOC

Ce document transporte le plan initial validé du chantier `github_actions_openclaw`.

Il reste la fiche de référence du chantier tant qu'aucun changement explicite ou implicite de projet ne remplace le master target.

## 3_INITIAL_NEED

Préparer tous les jobs/actions nécessaires dans GitHub Actions, les tester, exporter un registre dans le repo, relire le registre des jobs non-trading pour éviter les doublons, puis seulement préparer et tester l'orchestration par OpenClaw.

## 4_MASTER_PROJECT_PLAN

Chaîne de travail validée :

1. Lire l'état réel du repo, la matrice et les surfaces CI existantes.
2. Inventorier les workflows GitHub Actions existants.
3. Relire le registre des jobs non-trading.
4. Produire un registre canonique GitHub Actions.
5. Classer les jobs : `REUSE`, `WRAP_IN_ACTION`, `DUPLICATE`, `MISSING`, `OPENCLAW_ONLY`, `ACTION_ONLY`.
6. Ne pas recréer un job déjà couvert.
7. Tester GitHub Actions seules avant OpenClaw.
8. Préparer l'orchestration OpenClaw seulement après registry + tests + dedup.
9. Garder HITL pour merge/apply/write sensibles.

## 5_GO_PLAN

- Phase 01 : ouverture master plan + registry + inventory.
- Phase 02 : validation des workflows Actions existants.
- Phase 03 : création ciblée des jobs manquants.
- Phase 04 : test `workflow_dispatch`.
- Phase 05 : child GO OpenClaw orchestration.
- Phase 06 : close gate master target.

## 6_FINAL_TARGET

GitHub Actions devient une couche de jobs CI standardisée, registrée et testée, que OpenClaw peut lire, déclencher et surveiller sans dupliquer les jobs non-trading.

## TRANSPORT

`TRANSPORT_MODE = bundle_patch_zip`

Artefacts attendus :

- `TARGETS.md`
- `target_card.json`
- `.patch` canonique
- `.zip` transportable
