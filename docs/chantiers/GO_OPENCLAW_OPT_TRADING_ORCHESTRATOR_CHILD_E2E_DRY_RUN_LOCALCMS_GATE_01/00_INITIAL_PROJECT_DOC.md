---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_DRY_RUN_LOCALCMS_GATE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_DRY_RUN_LOCALCMS_GATE_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01
upstream_parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
pf_id: PF_OPENCLAW_ORCHESTRATOR_FULL
status: open
lifecycle_stage: opening
surface: scripts/e2e/dry_run_pipeline.py
source_kind: canonical
updated_at: 2026-05-26
topic_keys:
  - e2e
  - localcms
  - gate
  - dry-run
---

# 00_INITIAL_PROJECT_DOC — E2E Dry-Run LocalCMS Gate

## 1_MASTER_TARGET

Fermer le gap E2E documenté dans `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01` (#830) : `scripts/e2e/dry_run_pipeline.py` sort rc=1 si LocalCMS n'est pas lancé.

## 2_INITIAL_PROJECT_DOC

Ce GO ouvre `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_DRY_RUN_LOCALCMS_GATE_01`.

## 3_INITIAL_NEED

Deux problèmes distincts identifiés à la lecture :
1. **Crash réel** : step 1c importe `NotificationDispatcher` directement — échoue avec `ModuleNotFoundError: No module named 'requests'` dans le venv → rc=1 sans atteindre le check LocalCMS
2. **Gate LocalCMS non structurée** : step 8 appelle `check_lcms_endpoints()` sans mode, LocalCMS absent = report incomplet et exit code incohérent

## 4_SCOPE

```
scripts/e2e/dry_run_pipeline.py
tests/e2e/test_dry_run_pipeline_localcms_gate.py
docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_DRY_RUN_LOCALCMS_GATE_01/
```

## 5_FINAL_TARGET

- `dry_run_pipeline.py` ne crashe plus en mode default (venv sans requests)
- Gate LocalCMS : PASS / WARN_SKIPPED / BLOCKED explicite
- rc=0 si LocalCMS absent en mode default
- rc=1 uniquement si REQUIRE_LOCALCMS_E2E=1 et LocalCMS absent
- 28 tests gate + 23 tests E2E existants = 51 tests ALL PASS
