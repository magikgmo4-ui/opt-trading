---
go_id: GO_OPT_TRADING_DEEPSEEK_STUDENT_REGISTRY_STATUS_DECISION_01
doc_type: REPRISE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 40_REPRISE

## Summary

- `deepseek_student` is confirmed as legacy/transitional in family terms, but not eligible for immediate central registry entry.
- the blocking issue is the unresolved physical/runtime boundary, not only missing status vocabulary.
- the decision of this GO is to keep `deepseek_student` outside central registries until runtime-boundary closure is handled.

## Files created

- `docs/chantiers/GO_OPT_TRADING_DEEPSEEK_STUDENT_REGISTRY_STATUS_DECISION_01/00_INITIAL_PROJECT_DOC.md`
- `10_EVIDENCE_BASE.md`
- `20_DECISION.md`
- `30_NEXT_GO.md`
- `40_REPRISE.md`

## Diff summary

- formalise why `deepseek_student` must not yet be registered centrally
- separate the status-vocabulary question from the deeper runtime-boundary question
- designate a runtime-boundary closure GO as the next necessary execution step

## Verification

```bash
rg -n "deepseek_student|legacy|transitional|runtime boundary|outside central registries" docs/chantiers/GO_OPT_TRADING_DEEPSEEK_STUDENT_REGISTRY_STATUS_DECISION_01
git status --short --branch
git diff -- docs/chantiers/GO_OPT_TRADING_DEEPSEEK_STUDENT_REGISTRY_STATUS_DECISION_01
```

## Verdict

`PASS`
