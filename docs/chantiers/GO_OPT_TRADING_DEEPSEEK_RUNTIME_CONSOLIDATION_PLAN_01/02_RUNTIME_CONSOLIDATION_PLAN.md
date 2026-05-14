---
doc_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01_CONSOLIDATION_PLAN
doc_type: consolidation_plan
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01
status: draft_for_review
lifecycle_stage: child_plan
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01
topic_keys:
  - opt-trading
  - deepseek
  - consolidation-plan
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01/02_RUNTIME_CONSOLIDATION_PLAN.md
point_de_reprise: "Plan de consolidation runtime DeepSeek."
updated_at: 2026-05-13
links:
  - docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01/01_EXISTING_STATE.md
---

# 02_RUNTIME_CONSOLIDATION_PLAN

## 1_CIBLE RUNTIME

```text
student/
├── scripts/student_*              ← raccourcis globaux canoniques (MENU, CMD, SANITY)
├── scripts/deepseek_hub/          ← scripts hub unifies
├── scripts/deepseek_student/      ← scripts etudiant
├── scripts/wrappers/              ← wrappers de compatibilite
├── docs/                          ← runbook, architecture
└── validation/                    ← validation live

modules/deepseek_hub/              ← facade module survivante
modules/deepseek_response/         ← retire apres verification callers
modules/deepseek_thinking/         ← retire apres verification callers
modules/deepseek_student/          ← retire ou fusionne dans student/
scripts/student/                   ← RETIRE (legacy)
```

## 2_PHASES

```text
Phase 1 — AUDIT DES CALLERS
  - lister tous les appels reels a deepseek_response, deepseek_thinking
  - verifier post_change.sh, workflow_post_change_v2
  - verifier les wrappers student/scripts/wrappers/

Phase 2 — MIGRATION DES SCRIPTS
  - copier scripts/student/ manquants vers student/scripts/
  - mettre a jour les raccourcis globaux
  - verifier que les patches deepseek_hub sont appliques

Phase 3 — RETRAIT DES DOUBLONS
  - supprimer scripts/student/ apres verification
  - supprimer modules/deepseek_student/ une fois fusionne
  - supprimer modules/deepseek_response/ et thinking/ si plus de callers

Phase 4 — VALIDATION
  - test post_change workflow
  - test daily-ai-report
  - test menu-deepseek / cmd-deepseek_*
  - rollback documente
```

## 3_DEPENDANCES

```text
- post_change workflow (ne pas casser)
- Ollama local (doit etre actif)
- shortcuts operateurs (/usr/local/bin/menu-deepseek, etc.)
- modules/deepseek_hub/patches/apply_patches.sh
```

## 4_RISQUES

| Risque | Impact | Mitigation |
|---|---|---|
| casser post_change | perte workflow | test avant retrait |
| shortcuts orphelins | perte acces operateur | backup + rollback |
| scripts/student/ encore utilise | regression | audit callers avant retrait |
| deepseek_response/thinking encore appeles | erreur runtime | verification exhaustive |
