# deploy_module_multi_machine continuity

Last reconciled: 2026-03-18
Orchestrator: `admin-trading`
Primary targets: `student`, `db-layer`

## Standard state

- `deploy_module_multi_machine` is the validated multi-machine deployment standard on `admin-trading`.
- Global wrappers present on `admin-trading`:
  - `menu-deploy_module_multi_machine`
  - `cmd-deploy_module_multi_machine`
  - `sanity-deploy_module_multi_machine`
- Capabilities confirmed in production:
  - `status`
  - `plan`
  - `preflight`
  - `deploy`
  - `--post-install`
  - menu aligned with CLI
  - run-scoped tempfiles / `run_id`
  - remote lock by target + `install_path`
  - stale lock inspection + explicit cleanup

## Lot A reconciliation

### Already validated before current run

- `module_contextuals_shell`
  - `student`: runtime present, sanity OK
  - `db-layer`: runtime present, sanity OK
- `env`
  - `student`: runtime present, sanity OK
  - `db-layer`: runtime present, sanity OK
- `repo_hygiene`
  - `student`: runtime present, sanity OK
  - `db-layer`: runtime present, sanity OK

### Validated during current run

- `audit`
  - source: `/opt/trading/modules/audit`
  - preflight: OK on `student` and `db-layer`
  - deploy run id: `20260318T205850202362Z_a29e99be`
  - result:
    - `student`: deployed to `/opt/trading/audit`, sanity OK
    - `db-layer`: deployed to `/opt/trading/audit`, sanity OK
  - `post-install`: not requested; no `scripts/install_module.sh` in source runtime
- `repo_local_artifacts`
  - source: `/opt/trading/modules/repo_local_artifacts`
  - preflight: OK on `student` and `db-layer`
  - deploy run id: `20260318T212740202162Z_a00ec825`
  - result:
    - `student`: deployed to `/opt/trading/repo_local_artifacts`, sanity OK
    - `db-layer`: deployed to `/opt/trading/repo_local_artifacts`, sanity OK
  - `post-install`: not requested during deploy; no `scripts/install_module.sh` in source runtime
- `repo_ownership_guard`
  - source: `/opt/trading/modules/repo_ownership_guard`
  - inspection: source README mentions optional sudo-based ownership fixes, but deployed wrapper runtime itself remains inspect-oriented (`cmd/menu/sanity`) and no fix action is executed by deploy or sanity
  - preflight: OK on `student` and `db-layer`
  - deploy run id: `20260318T225707250840Z_881e5e15`
  - result:
    - `student`: deployed to `/opt/trading/repo_ownership_guard`, sanity OK
    - `db-layer`: deployed to `/opt/trading/repo_ownership_guard`, sanity OK
  - `post-install`: not requested during deploy; no `scripts/install_module.sh` in source runtime

### Not yet validated in Lot A

- `ops_wrappers`
  - source inspection: wrapper-generation module with `ops_wrappers.sh`, wrapper templates, and shortcut installation logic
  - source sanity on `admin-trading`: OK, but only checks `/opt/trading/modules` presence and script existence
  - observed source-layout copy already present on `student` and `db-layer` at `/opt/trading/modules/ops_wrappers`
  - observed global wrapper already present on both targets: `cmd-ops_wrappers -> /opt/trading/modules/ops_wrappers/scripts/cmd.sh`
  - observed source-layout hashes on `admin-trading`, `student`, and `db-layer`: identical for `ops_wrappers.sh`, `README.md`, `scripts/cmd.sh`, `scripts/menu.sh`, `scripts/sanity_check.sh`
  - observed non-destructive validation on targets: `cmd-ops_wrappers scan` works on both targets
  - standard runtime path `/opt/trading/ops_wrappers` remains absent on targets and is **not** the right deployment shape for this module
  - adaptation options considered:
    - keep it source-only and never deploy/update it remotely
    - refactor it into a runtime-safe `/opt/trading/ops_wrappers` module without sudo side effects
    - keep its current source-layout behavior and, if a future refresh is needed, deploy it explicitly to `/opt/trading/modules/ops_wrappers`
  - adapted deployment strategy retained: treat `ops_wrappers` as a source-layout tool, not a standard runtime module; if future refresh is needed, use explicit `--install-path /opt/trading/modules/ops_wrappers` instead of `/opt/trading/ops_wrappers`
  - no code change applied during this strategy pass; no global shortcut install executed on targets
- `journal_engine`
  - source inspection: app-bearing module with `app/`, `config/`, sample inputs, and wrapper scripts
  - source sanity on `admin-trading`: OK, but it runs a real sample build and `python3 -m modules.journal_engine.app.journal_engine`
  - runtime on `student` and `db-layer`: absent
  - deployment decision: do **not** standard-deploy for now because the source wrappers and app assume the repo-style `modules.journal_engine...` import path and a root layout aligned with `/opt/trading/modules`, which does not match the runtime install path `/opt/trading/journal_engine`

### Present on targets but not yet validated as standard Lot A runtime

- `scripts`
  - source module sanity on `admin-trading`: OK
  - source module shape: wrapper-only module under `/opt/trading/modules/scripts`
  - runtime on `student` and `db-layer`: `/opt/trading/scripts` already present, large shared scripts tree, strongly divergent from the wrapper-only source module
  - standard `scripts/sanity_check.sh` path not present in runtime path checked on either target
  - reconciliation decision: do **not** redeploy the source module over `/opt/trading/scripts` because it would replace a much larger existing runtime with a small wrapper-only tree
- `perf`
  - source module sanity on `admin-trading`: OK
  - source module shape: wrapper-only module under `/opt/trading/modules/perf`
  - runtime on `student` and `db-layer`: `/opt/trading/perf` already present as application runtime with `perf_app.py` and related data, not as wrapper-only module
  - standard `scripts/sanity_check.sh` path not present in runtime path checked on either target
  - reconciliation decision: do **not** redeploy the source module over `/opt/trading/perf` because the observed runtime is structurally different from the wrapper-only source module

## Current operational observations

- `student` and `db-layer` are reachable via corrected SSH aliases from `admin-trading`.
- No standard module observed under `/opt/trading/modules` with `scripts/install_module.sh`.
- For the current low-risk set, `--post-install` is expected to be `skipped`.
- `scripts` is now treated as a runtime reconciliation case, not a safe first deploy candidate.
- `ops_wrappers` is now documented as a non-standard deploy candidate because it targets wrapper generation and privileged shortcut installation.
- `ops_wrappers` is now documented as a source-layout tool already present on targets, not as a missing standard runtime.

## ops_wrappers runbook

- Dedicated runbook written:
  - `/opt/trading/docs/ops_wrappers_source_layout_refresh_runbook.md`
- Status:
  - source-layout refresh procedure documented
  - no real refresh executed in this documentation pass
  - runbook aligned with the non-standard doctrine and the validated source-layout preflight

## Recommended next candidate

- No safe standard Lot A deploy candidate remains after reconciling `scripts`, `perf`, `journal_engine`, and `ops_wrappers`.
- Recommended next task: if `ops_wrappers` needs an update, use the dedicated source-layout refresh runbook and require an explicit GO before the first real refresh.

## Remaining real limits

- No standard source module with `scripts/install_module.sh` observed in `/opt/trading/modules`.
- `repo_ownership_guard` source README still describes optional sudo-based ownership fixes, but this run validated only the wrapper runtime deployment and wrapper sanity, not execution of fix actions.
- `ops_wrappers` changes wrapper generation / installation behavior, hardcodes `/opt/trading/modules/ops_wrappers`, and installs `/usr/local/bin` shortcuts via `sudo`; it should not be treated like a neutral wrapper-only module, even though a working source-layout copy already exists on targets.
- `journal_engine` looks functionally heavier than wrapper-only modules because its sanity runs a sample build against module data, and its wrappers import `modules.journal_engine...`, which does not match the standard deployed runtime path.
- `scripts` should not be redeployed blindly because the observed target runtime is a much larger shared scripts tree than the current source module.
- `perf` should not be redeployed blindly because the observed target runtime is an existing application runtime (`perf_app.py`, local DB/artifacts) and not the wrapper-only source module.

## RISKS

- À qualifier.
