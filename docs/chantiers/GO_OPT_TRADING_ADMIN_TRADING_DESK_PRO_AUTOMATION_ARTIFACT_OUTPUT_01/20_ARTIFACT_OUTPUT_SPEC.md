---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01_SPEC
doc_type: artifact_output_spec
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-11
---

# 20_ARTIFACT_OUTPUT_SPEC - Artifact Output Spec

## Output directory

Default: `/opt/trading/runtime/desk_pro_dry_run/`
Override: `DESK_PRO_DRY_RUN_OUTPUT_DIR` environment variable

## Files produced

1. `latest.json` — full dry-run synthesis as JSON
2. `latest.md` — human-readable markdown report
3. `history.jsonl` — append-only log of all runs

## Included in each artifact

- `mode`: `dry_run`
- `status`: PASS, WARN, or FAIL
- `no_trade`: true
- `no_telegram`: true
- `no_webhook`: true
- `no_systemd`: true
- `signal_event`: V1 normalized
- `errors`: []
- `warnings`: []
- `summary`: entity presence booleans
- `artifact_meta`: file paths and run_id

## Safety

- `/runtime/` is git-ignored
- no network call
- no systemd dependency
- no .env access
- output dir created if missing
