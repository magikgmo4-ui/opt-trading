---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_MASTER_PLAN_ROADMAP_REFRESH_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_MASTER_PLAN_ROADMAP_REFRESH_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
master_project_plan_id: MPP_OPENCLAW_ORCHESTRATOR_FULL
pf_id: PF_OPENCLAW_ORCHESTRATOR_FULL
status: open
lifecycle_stage: opening
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-23
topic_keys:
  - openclaw
  - orchestration
  - master-plan
  - roadmap-refresh
  - documentation
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/00_SYSTEM_MASTER_PLAN.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/01_AUDIT_SURFACES_AND_STATE.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_FRESHNESS_AUDIT_01/00_FRESHNESS_AUDIT.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/11_NEXT_GO_SEQUENCE_AND_IDE_BUNDLE_PLAN.md
---

# 00_INITIAL_PROJECT_DOC — OpenClaw master plan roadmap refresh

## 1_MASTER_TARGET

Maintenir `PF_OPENCLAW_ORCHESTRATOR_FULL` lisible et opérable en corrigeant le master plan OpenClaw après les closeouts PASS récents, sans fermer le parent ni modifier les index globaux.

## 2_INITIAL_PROJECT_DOC

Cette fiche ouvre le child documentaire chargé de transformer l'audit de fraîcheur en mise à jour contrôlée du master plan existant.

## 3_INITIAL_NEED

La PR #764 a ajouté un audit read-only qui prouve que le master plan du 2026-05-14 est partiellement périmé : bridge, signal router, notification dispatcher et proposition engine sont maintenant PASS. Les tableaux et la roadmap du master plan doivent refléter cet état réel.

## 4_MASTER_PROJECT_PLAN

Parent et plan de rattachement :

```text
PF_ID: PF_OPENCLAW_ORCHESTRATOR_FULL
MASTER_PROJECT_PLAN_ID: MPP_OPENCLAW_ORCHESTRATOR_FULL
PARENT_GO_ID: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
SYSTEM_MASTER_PLAN: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
```

## 5_GO_PLAN

```text
GO_ID: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_MASTER_PLAN_ROADMAP_REFRESH_01
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PARENT_GO_ID: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
FINAL_TARGET: master plan OpenClaw mis à jour avec état post-closeouts et NEXT_GO réel
```

## 6_FINAL_TARGET

Mettre à jour uniquement les documents du master plan OpenClaw nécessaires pour :

- remplacer les statuts obsolètes `PRÉVU / IMPL MANQUANTE / NON OUVERT` par `PASS` quand prouvé ;
- inscrire `GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01` comme prochain GO réel recommandé ;
- conserver la distinction entre audit historique 2026-05-14 et état réel 2026-05-23 ;
- ne pas fermer le parent ;
- ne pas modifier les index globaux sauf décision explicite ultérieure.

## 7_CANONICAL_STATE

État établi par PR #764 fusionnée :

```text
PR_764 = MERGED
FRESHNESS_AUDIT = PRESENT
OPENCLAW_OPERATOR_BRIDGE = PASS
SIGNAL_ROUTER = PASS
NOTIFICATION_DISPATCHER = PASS
PROPOSITION_ENGINE = PASS
NEXT_REAL_GO = GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01
```

## 8_VALIDATED_PLAN

1. Lire `00_SYSTEM_MASTER_PLAN.md`.
2. Lire `01_AUDIT_SURFACES_AND_STATE.md`.
3. Lire `00_FRESHNESS_AUDIT.md`.
4. Modifier seulement les passages d'état et de roadmap devenus périmés.
5. Ajouter un bloc de datation indiquant que l'audit 2026-05-14 reste historique.
6. Documenter le NEXT_GO réel : `VALIDATION_GATE_V1_01`.
7. Produire closeout seulement si les modifications sont limitées, cohérentes et vérifiables.

## 9_SELECTED_SOLUTION

Patch documentaire ciblé, sans refonte complète du master plan.

## 10_SELECTED_SETUP

```text
BRANCH: go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_MASTER_PLAN_ROADMAP_REFRESH_01
BASE_SHA: 70e685cb2f3b53129e28fb58730f721b596e26ec
SCOPE: docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/
NO_GLOBAL_INDEX_PATCH: true
```

## 11_KEY_DECISIONS

- Le parent reste `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`.
- Le child ne ferme pas le parent.
- La PR #764 sert de preuve documentaire de fraîcheur.
- Le prochain GO réel est `VALIDATION_GATE_V1_01`.

## 12_INVARIANTS

```text
NO_PARENT_CLOSEOUT = true
NO_GLOBAL_INDEX_PATCH_WITHOUT_EXPLICIT_TRIGGER = true
NO_LIVE_TRADE_WITHOUT_GATE = true
OPENCLAW_DOES_NOT_ORCHESTRATE = true
OPT_TRADING_ORCHESTRATES = true
```

## 13_ESTABLISHED

- PR #764 fusionnée.
- Audit de fraîcheur présent.
- Quatre surfaces reclassifiées PASS.
- Le master plan principal reste partiellement périmé tant que ce child n'est pas appliqué.

## 14_HYPOTHESIS

- Une modification ciblée de `00_SYSTEM_MASTER_PLAN.md` et/ou `01_AUDIT_SURFACES_AND_STATE.md` suffit probablement.
- Les index globaux n'ont pas besoin de changer, sauf si l'horizon global ou le NEXT_GO global doit être publié.

## 15_REMAINING_GAP

- Master plan encore à patcher.
- Roadmap à réaligner avec `VALIDATION_GATE_V1_01`.
- Closeout du présent child à produire après patch.

## 16_TODO

1. Fetch local/remote state.
2. Relire les documents de gouvernance requis.
3. Appliquer patch documentaire ciblé.
4. Vérifier diff.
5. Commit/PR.
6. Closeout si scope respecté.

## 17_RESUME_POINT

```text
Reprendre sur la branche:
go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_MASTER_PLAN_ROADMAP_REFRESH_01

Lire:
docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_MASTER_PLAN_ROADMAP_REFRESH_01/00_INITIAL_PROJECT_DOC.md

action suivante:
mettre à jour le master plan OpenClaw avec l'état post-PR #764.
```

## 18_TO_DOCUMENT

TAGS:
- OPENCLAW
- MASTER_PLAN
- ROADMAP_REFRESH
- PR_764
- VALIDATION_GATE

Blocs à extraire :
- `7_CANONICAL_STATE`
- `12_INVARIANTS`
- `17_RESUME_POINT`

## 19_TO_REMEMBER

### MEM_CANDIDATE

Quand PR #764 est fusionnée, le prochain child OpenClaw logique est `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_MASTER_PLAN_ROADMAP_REFRESH_01`, puis le prochain GO produit est `GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01`.

### SAVE_MEMORY

Non requis automatiquement. À mémoriser seulement sur demande explicite.
