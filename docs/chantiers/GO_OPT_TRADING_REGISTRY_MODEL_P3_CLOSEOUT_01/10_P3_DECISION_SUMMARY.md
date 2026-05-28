---
go_id: GO_OPT_TRADING_REGISTRY_MODEL_P3_CLOSEOUT_01
doc_type: P3_DECISION_SUMMARY
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 10_P3_DECISION_SUMMARY

## P3 decisions now established

1. `registry/*.yaml` remains the central source of truth.
2. Specialized readers own registry reading by domain.
3. `registry_router` is a navigation facade, not a source of truth.
4. local fallbacks are degraded read-only modes, never a parallel truth.
5. `deepseek_student` stays excluded from central registries.
6. `student/scripts/` is the canonical DeepSeek student runtime/operator surface.
7. `scripts/student/` is a compatibility shim layer.
8. `modules/deepseek_student/` is a non-runtime scaffold.
9. `machine_target` remains the primary compatible anchor.
10. `placement_mode` is now the complementary semantic axis.
11. unqualified `machine_target: any` is now forbidden except for an explicit residual allowlist.
12. the residual allowlist is reduced to `mimo_open_observer` only.

## P3 conclusion

The registry model is no longer in exploratory mode.

It now has:

- a central truth contract,
- reader behavior aligned with that contract,
- a resolved DeepSeek registry stance,
- a compatible machine/placement model,
- and governance tests enforcing the refined rules.
