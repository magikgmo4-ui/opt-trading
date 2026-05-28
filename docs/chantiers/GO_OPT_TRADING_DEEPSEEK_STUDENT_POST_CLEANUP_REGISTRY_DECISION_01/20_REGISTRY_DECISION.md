---
go_id: GO_OPT_TRADING_DEEPSEEK_STUDENT_POST_CLEANUP_REGISTRY_DECISION_01
doc_type: REGISTRY_DECISION
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-27
---

# 20_REGISTRY_DECISION

## Final decision

`deepseek_student` should remain excluded from central registries.

## Why this is stronger after cleanup

Before cleanup, exclusion was temporary because the runtime boundary was unresolved.

After cleanup, exclusion remains correct for a different reason:

- the canonical object is `student/scripts/`, not `modules/deepseek_student/`
- the remaining `deepseek_student` naming in `scripts/student/` is now shim compatibility, not a primary owner surface
- `deepseek_hub` already holds the central family-level operator/documentary role

So adding a central `deepseek_student` entry now would mostly register a compatibility alias or naming residue rather than a true central module owner.

## Answers to the key questions

1. Should the registry object represent `student/scripts/` rather than `modules/deepseek_student/`?
Yes, if any future object were ever represented centrally.

2. Is central `legacy` justified now?
No, not in the current central module registry.

Reason:
`legacy` would be semantically closer than `transitional`, but it would still centralize a compatibility alias instead of a clean module/object boundary.

3. Is central `transitional` more correct?
No.

Cleanup has already stabilized the runtime truth. The remaining role is compatibility, not an unresolved migration leader.

4. Is permanent exclusion preferable?
Yes.

Given the current registry model, exclusion is the cleanest and most faithful representation.

## Canonical rule set from this GO

1. no `deepseek_student` entry is added to `registry/modules_registry.yaml`
2. no wrapper registry triplet is added for `deepseek_student`
3. no UI surface registry entry is added for `deepseek_student`
4. DeepSeek central representation continues through `deepseek_hub`, `deepseek_response`, and `deepseek_thinking`
5. `deepseek_student` remains a compatibility/documentary concept outside central registries unless the registry model itself changes later
