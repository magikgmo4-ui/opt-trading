---
go_id: GO_OPT_TRADING_MACHINE_TARGET_MODEL_REFINEMENT_01
doc_type: REPRISE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 50_REPRISE

## Summary

- `machine_target` is kept as the primary anchor field
- the missing concept is not a replacement field, but a complementary semantic axis
- `placement_mode` is recommended as the first compatible refinement
- `any` remains allowed only for truly portable tools, not as a generic escape hatch for cross-machine ambiguity

## Files created

- `docs/chantiers/GO_OPT_TRADING_MACHINE_TARGET_MODEL_REFINEMENT_01/00_INITIAL_PROJECT_DOC.md`
- `10_CURRENT_STATE_AUDIT.md`
- `20_REFINED_MODEL.md`
- `30_MIGRATION_RULES.md`
- `40_NEXT_IMPL_GO.md`
- `50_REPRISE.md`

## Diff summary

- clarifies what `machine_target` should continue to mean
- separates dominant machine anchor from cross-host placement semantics
- proposes a minimal follow-up field and migration policy without breaking current readers

## Verification

```bash
rg -n "machine_target|placement_mode|portable_tool|cross_host_facade|operator_entry" docs/chantiers/GO_OPT_TRADING_MACHINE_TARGET_MODEL_REFINEMENT_01
git status --short --branch
git diff -- docs/chantiers/GO_OPT_TRADING_MACHINE_TARGET_MODEL_REFINEMENT_01
```

## Verdict

`PASS`
