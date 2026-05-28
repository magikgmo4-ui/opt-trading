---
go_id: GO_OPT_TRADING_DEEPSEEK_STUDENT_POST_CLEANUP_REGISTRY_DECISION_01
doc_type: REPRISE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-27
---

# 40_REPRISE

## Summary

- post-cleanup, `deepseek_student` still should not enter central registries
- the reason has changed: the runtime boundary is now closed, but the surviving object is a student-side surface plus compatibility shims, not a clean central module object
- `legacy` would be closer than `transitional`, but still not justified under the current central module registry model
- no immediate registry mutation GO is needed for `deepseek_student`

## Files created

- `docs/chantiers/GO_OPT_TRADING_DEEPSEEK_STUDENT_POST_CLEANUP_REGISTRY_DECISION_01/00_INITIAL_PROJECT_DOC.md`
- `10_POST_CLEANUP_EVIDENCE.md`
- `20_REGISTRY_DECISION.md`
- `30_NEXT_REGISTRY_ACTION.md`
- `40_REPRISE.md`

## Diff summary

- re-evaluates the central-registry question after runtime cleanup is complete
- concludes that exclusion remains the most faithful central representation
- redirects follow-up energy toward broader registry-model or machine-target governance rather than a forced `deepseek_student` mutation

## Verification

```bash
rg -n "excluded from central registries|legacy|transitional|student/scripts|deepseek_student" docs/chantiers/GO_OPT_TRADING_DEEPSEEK_STUDENT_POST_CLEANUP_REGISTRY_DECISION_01
git status --short --branch
git diff -- docs/chantiers/GO_OPT_TRADING_DEEPSEEK_STUDENT_POST_CLEANUP_REGISTRY_DECISION_01
```

## Resume point

```text
CURRENT_GO = GO_OPT_TRADING_DEEPSEEK_STUDENT_POST_CLEANUP_REGISTRY_DECISION_01
MODE = doc-only
NEXT_IF_PASS = GO_OPT_TRADING_MACHINE_TARGET_MODEL_REFINEMENT_01
ALTERNATIVE_NEXT = future registry-model GO if compatibility aliases must become central objects
```

## Verdict

`PASS`
