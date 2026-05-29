---
doc_id: OPT_TRADING_RUNS_VALIDATION_BACKLOG_01
doc_type: canonical_runs_validation_backlog
repo: opt-trading
project: opt-trading
status: active
source_kind: canonical
created_at: 2026-05-28
updated_at: 2026-05-28
go_id: GO_OPT_TRADING_RUNS_VALIDATION_BACKLOG_CANONICALIZE_01
owner_surface: doc_ops
reference_canonique_principale: docs/index/RUNS_VALIDATION_BACKLOG_01.md
point_de_reprise: "Table RUNS_VALIDATION_BACKLOG"
topic_keys:
  - runs
  - validation
  - backlog
  - phase
  - pending
  - machine
  - github_actions
  - openclaw
  - automation
---

# RUNS_VALIDATION_BACKLOG_01

## Role

Registre canonique des runs, phases, validations en attente et verifications ulterieures detectees dans les chantiers `opt-trading`.

Ce registre est un index de suivi. Il ne remplace pas les preuves detaillees dans les chantiers, emails, logs ou outputs runtime.

## Regles

- `PASS_FULL` interdit sans preuve runtime ou CI complete.
- `PRECHECK_PASS` reste a verifier si le modele, runner ou E2E n'a pas ete execute completement.
- `PASS_WITH_WARNINGS` ne ferme pas le parent sans acceptation explicite ou correction.
- `PARTIAL_PASS` implique un prochain run cible.
- `FIXTURE_ONLY` ne vaut pas preuve runtime reelle.
- Aucun rerun CI ou runtime n'est declenche par ce fichier.

## Statuts canoniques utilises

```text
DUE_NOW
SCHEDULED
BLOCKED_BY_CI_SCOPE
BLOCKED_BY_PRECHECK
PARTIAL_PASS
PASS_WITH_WARNINGS
PRECHECK_PASS
FIXTURE_ONLY_OR_NOT_PROVEN
WAITING_POLICY_ACCEPTANCE
DONE_OR_NOT_ACTIONABLE
```

## RUNS_VALIDATION_BACKLOG

| RUN_ID | GO_ID | machine | branch | commit | run_date | status | evidence_path | verification_due_date | next_action |
|---|---|---|---|---|---|---|---|---|---|
| PHASE_01_STRICT_WORKER_READONLY_SMOKE | GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01 | local/temp-worktree | unknown | origin/sot/mainline | 2026-05-28 verified from docs | PRECHECK_PASS / DUE_NOW | docs/chantiers/GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01/80_PHASE_01_EXECUTION_PACKET.md ; docs/chantiers/GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01/82_PHASE_01_GATE_DECISION.md | 2026-05-28 | Rejouer `strict-worker-readonly-smoke` en vraie execution modele end-to-end ; conserver Phase 01 en `PASS_WITH_FOLLOWUP` tant que non prouve. |
| PHASE_5_DBLAYER_TO_FANTOME_OPENCLAW_REMOTE_EXEC | GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01 | db-layer -> fantome | unknown | unknown | 2026-05-06 / updated 2026-05-08 | PARTIAL_PASS / DUE_NOW | docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/02_REMOTE_EXEC_LOG.md | 2026-05-28 | Verifier si la remediation OpenClaw a ete rejouee ; SSH direct PASS mais OpenClaw applicatif FAIL sandbox/SSH. |
| RUNTIME_READONLY_1_10_DBLAYER_ADMIN_TRADING | GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01 | db-layer + admin-trading | unknown | unknown | 2026-05-23 | PASS_WITH_WARNINGS | docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01/56_STRICT_READ_ONLY_VALIDATION_RESULTS_1_10.md | 2026-05-28 | Corriger/accepter warnings : repo hygiene, Telegram allowlist, runtime healthcheck PyYAML/venv, mobile smoke non execute. |
| STEP_5_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS | GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01 | db-layer + fleet | unknown | unknown | 2026-05-23 | WAITING_POLICY_ACCEPTANCE / SCHEDULED | docs/chantiers/GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01/90_REPRISE.md | 2026-05-30 09:00 America/Montreal | Confirmer Fleet Health Phase 1 : PR #605, unreachable=[], failing=[], aucun WARN_ACTIONABLE, >=30 runs, >=14 jours, fail_count=0. |
| SIGNAL_CHAIN_TOTAL_PRODUCT_SURFACES | GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01 | multi-surface | unknown | unknown | 2026-05-23 | FIXTURE_ONLY_OR_NOT_PROVEN | docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01/03_PRODUCT_ROADMAP_KANBAN.md | 2026-05-28 | Ne pas fermer umbrella ; surfaces encore ouvertes : runtime distant, Bot Vision, Coinglass/API, Telegram inbound/outbound, Sheets implementation, Perf Engine, E2E preuves reelles. |
| GHA_26613644552_TELEGRAM_CHANNEL_REGISTRY_RUNTIME | GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01 | GitHub Actions | unknown | 7da8fe9 | 2026-05-28 22:06 America/Montreal | BLOCKED_BY_CI_SCOPE | Gmail GitHub notification ; GitHub Actions run 26613644552 | 2026-05-28 | Corriger `gate/no-lock-overlap` et `gate/file-scope` avant rerun ; tests skipped. |
| GHA_26609754836_MODELS_REGISTRY_FORMALIZE | GO_OPT_TRADING_MODELS_REGISTRY_FORMALIZE_01 | GitHub Actions | unknown | e94fc75 | 2026-05-28 20:07 America/Montreal | BLOCKED_BY_PRECHECK | Gmail GitHub notification ; GitHub Actions run 26609754836 | 2026-05-28 | Lire logs job `78412829399`; corriger packets Strict Workers au step `Validate all job packets`. |
| GHA_26604289603_SEMIAUTO_PILOT_REAL_CASE | GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_REAL_CASE_01 | GitHub Actions | unknown | 1e1faeb | 2026-05-28 17:49 America/Montreal | BLOCKED_BY_PRECHECK | Gmail GitHub notification ; GitHub Actions run 26604289603 | 2026-05-28 | Corriger `gate/preflight` avant toute validation du premier run reel pilote semi-auto. |
| GHA_26589456888_DATA_CENTER_BINANCE_SPOT_RUNTIME | data-center / binance spot collector runtime | GitHub Actions | unknown | 9d36305 | 2026-05-28 13:00 America/Montreal | BLOCKED_BY_CI_SCOPE | Gmail GitHub notification ; GitHub Actions run 26589456888 | 2026-05-28 | Corriger `gate/no-lock-overlap` et `gate/file-scope` ; tests skipped. |
| GHA_26573775281_AUTOMATION_OPS_PARENT_CLOSEOUT | GO_AUTOMATION_OPS_OPT_TRADING_CHILD_PARENT_CLOSEOUT_01 | GitHub Actions | unknown | 2a1dfc4 | 2026-05-28 08:10 America/Montreal | BLOCKED_BY_CI_SCOPE | Gmail GitHub notification ; GitHub Actions run 26573775281 | 2026-05-28 | Corriger `gate/file-scope`; ne pas considerer closeout parent comme valide tant que CI gate echoue. |
| CHATGPT_AUTOMATION_FLEET_HEALTH_GATE | automation ChatGPT | ChatGPT task | n/a | n/a | scheduled 2026-05-30 09:00 | SCHEDULED | automation title: Verifie le gate Fleet Health | 2026-05-30 09:00 America/Montreal | Attendre le rappel ou verifier manuellement le gate Fleet Health Phase 1. |
| CHATGPT_AUTOMATIONS_TRADING_WATCHLIST | automation ChatGPT | ChatGPT task | n/a | n/a | recurring | DONE_OR_NOT_ACTIONABLE | active tasks list | recurring | Hors scope repo runtime ; noter que plusieurs automations ont notifications/email disabled, donc les outputs peuvent rester non visibles hors UI. |

## Mots-cles de scan a reutiliser

```text
run
runs
phase
PHASE
execution
execution_log
validation
pending
PENDING
DRAFT_ONLY
PRECHECK_PASS
PASS_WITH_WARNINGS
PARTIAL_PASS
BLOCKED
CLOSEOUT_BLOCKED
NOT_PROVEN
FIXTURE_ONLY
follow-up
a verifier
verification
attente
a terme
```

## Machines / surfaces de scan a reutiliser

```text
student
db-layer
fantome
admin-trading
cursor-ai
windows
mobile
Termux
GitHub Actions
automations ChatGPT
```

## NEXT_GO

```text
NEXT_GO = auditer les lignes DUE_NOW dans l'ordre :
1. PHASE_01_STRICT_WORKER_READONLY_SMOKE
2. PHASE_5_DBLAYER_TO_FANTOME_OPENCLAW_REMOTE_EXEC
3. GitHub Actions BLOCKED_BY_CI_SCOPE / BLOCKED_BY_PRECHECK
4. Fleet Health Phase 1 a la date planifiee 2026-05-30
```
