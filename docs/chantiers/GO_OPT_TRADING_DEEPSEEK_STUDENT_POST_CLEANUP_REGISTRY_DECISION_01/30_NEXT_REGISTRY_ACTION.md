---
go_id: GO_OPT_TRADING_DEEPSEEK_STUDENT_POST_CLEANUP_REGISTRY_DECISION_01
doc_type: NEXT_REGISTRY_ACTION
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-27
---

# 30_NEXT_REGISTRY_ACTION

## Immediate next action

No `deepseek_student` registry mutation GO is required now.

## Why no immediate mutation GO

This GO concludes that the correct registry action is deliberate non-addition.

So the next logical work is not `deepseek_student` realignment, but one of these broader follow-ups:

1. `GO_OPT_TRADING_MACHINE_TARGET_MODEL_REFINEMENT_01`
2. a future registry-model GO if the project later wants to represent compatibility aliases or non-module runtime surfaces centrally
3. a future physical cleanup/archival GO if `modules/deepseek_student/` or the remaining shim layer should be retired further

## If a future central entry is ever reconsidered

Then it should come in a separate GO and satisfy all these conditions:

1. the represented object is explicitly `student/scripts/` or another clearly surviving surface
2. the registry grammar explicitly supports the intended compatibility concept
3. wrapper and UI consequences are stated explicitly

## Wrapper/UI consequence today

If a central entry were added today, the likely related wrappers would be:

- `cmd-deepseek_student`
- `menu-deepseek_student`
- `sanity-deepseek_student`

But this GO explicitly decides not to centralize those compatibility-facing names.
