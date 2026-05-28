---
go_id: GO_OPT_TRADING_REGISTRY_MODEL_P3_CLOSEOUT_01
doc_type: REMAINING_GAPS
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 30_REMAINING_GAPS

## Residual gap G1 - `mimo_open_observer`

`mimo_open_observer` is the only remaining explicit `machine_target:any` residual case without `placement_mode`.

Why it remains open:

- the registry still marks it active
- the module still exposes runnable CLI and scheduler wiring
- historical docs also classify it as closed/student in some places

So the remaining issue is state clarification, not generic machine-target design anymore.

## Residual gap G2 - optional future status grammar

The registry source-of-truth contract identified future central `legacy` and `transitional` vocabulary as useful, but this is no longer blocking P3 registry model closeout.

## Residual gap G3 - broader registry-model ambitions are optional

P3 does not require:

- a `machine_targets` matrix
- a global registry rewrite
- central representation of compatibility aliases like `deepseek_student`

Those remain optional future design work, not required next steps.
