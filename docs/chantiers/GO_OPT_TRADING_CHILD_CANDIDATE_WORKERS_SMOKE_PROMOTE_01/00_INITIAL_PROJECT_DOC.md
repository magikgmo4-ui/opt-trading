---
doc_id: GO_OPT_TRADING_CHILD_CANDIDATE_WORKERS_SMOKE_PROMOTE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
module: ai_workers
go_id: GO_OPT_TRADING_CHILD_CANDIDATE_WORKERS_SMOKE_PROMOTE_01
status: closed
lifecycle_stage: done
created_at: 2026-05-28
closed_at: 2026-05-28
pr: pending
links:
  - tests/test_candidate_workers.py
  - scripts/ai/workers/localcms_automation_status_sync.py
  - scripts/ai/workers/openclaw_mobile_control.py
  - scripts/deploy_wrappers_ot_wrap_01.sh
  - docs/registry/JOBS_REGISTRY.md
---

# GO_OPT_TRADING_CHILD_CANDIDATE_WORKERS_SMOKE_PROMOTE_01

## Objectif

Valider les 3 workers `candidate` restants dans JOBS_REGISTRY.md par smoke + tests, puis promouvoir en `active`.

Cibles :
- `aw_localcms_sync` (`localcms_automation_status_sync.py`) — candidate, medium risk
- `aw_openclaw_mobile` (`openclaw_mobile_control.py`) — candidate, medium risk
- `op_deploy_wrappers` (`deploy_wrappers_ot_wrap_01.sh`) — candidate, medium risk

## Livrable

`tests/test_candidate_workers.py` — 43 tests, 10 classes :

**localcms_automation_status_sync :**
- `TestLocalcmsReadJson` (3) — read_json() : existing file, missing file, invalid JSON
- `TestLocalcmsLedgerSummary` (2) — ledger_summary() : missing file, existing JSONL
- `TestLocalcmsBuildSnapshot` (4) — build_snapshot() : required keys, phase/job_id, status PASS, allowed_writes list
- `TestLocalcmsTmuxSessions` (1) — tmux_sessions() : available + sessions keys
- `TestLocalcmsSmoke` (2) — subprocess main : exit 0, snapshot PASS

**openclaw_mobile_control :**
- `TestValidatePhase` (5) — validate_phase() : PHASE_01, lowercase norm, PHASE_02 None, None default, arbitrary None
- `TestValidateJobForMobile` (4) — validate_job_for_mobile() : valid job, None job, forbidden marker, external write scope
- `TestSafeName` (5) — safe_name() : alphanumeric, slash replaced, None→all, empty→all, max 96
- `TestGetJob` (3) — get_job() : known, unknown, None
- `TestSafetyTemplate` (1) — safety_template() : non_trading_only + no external_write/signal/secret
- `TestAllJobs` (2) — PHASE_01_JOBS : required attrs, no external write scope
- `TestOpenclawtMobileSmoke` (5) — subprocess : status exit 0, status JSON PASS, list-jobs exit 0, list-jobs count, preflight valid job

**deploy_wrappers_ot_wrap_01.sh :**
- `TestDeployWrappers` (6) — script exists, bash -n syntax, set -euo pipefail, validated_prompt_factory ref, trae_module_validator ref, ln -sf pattern

## Points techniques notables

- Smoke localcms et openclaw via subprocess (scripts utilisent `path.relative_to(REPO_ROOT)` — tmpdir patch hors REPO_ROOT échoue)
- `_omc_run(*args)` helper pour les 5 tests smoke openclaw_mobile
- PyYAML parse `on:` → `True` en YAML 1.1 (pattern `wf.get("on") or wf.get(True) or {}`)
- TemporaryDirectory : lecture fichiers impérativement dans le bloc `with`

## Verdict

```
43/43 PASS
JOBS_REGISTRY.md v1.5 mis à jour :
  aw_localcms_sync    : candidate → active (add_test → keep)
  aw_openclaw_mobile  : candidate → active (add_test → keep)
  op_deploy_wrappers  : candidate → active (add_test → keep)
  B04 / B05           : CLOSED
```
