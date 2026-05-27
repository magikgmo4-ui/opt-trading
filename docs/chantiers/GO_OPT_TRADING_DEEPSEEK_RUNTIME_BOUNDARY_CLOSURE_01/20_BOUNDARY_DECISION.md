---
go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_BOUNDARY_CLOSURE_01
doc_type: BOUNDARY_DECISION
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-27
---

# 20_BOUNDARY_DECISION

## Final boundary decision

### Surviving runtime surface

`student/scripts/` is the surviving canonical runtime and operator surface for the DeepSeek student cluster.

### Temporary compatibility surface

`scripts/student/` remains a legacy compatibility layer only.

It is not the canonical workspace anymore, but it cannot be removed until the remaining callers and shortcuts are fully verified or migrated.

### Non-runtime surface

`modules/deepseek_student/` is not a runtime owner.

It must be treated as a module scaffold/documentary compatibility surface pending later cleanup, absorption, or archival.

## Implications

1. future runtime truth references should point first to `student/scripts/`
2. `scripts/student/` should be described as compat-only, not as active owner
3. `modules/deepseek_student/` should not drive registry or runtime decisions by itself
4. any future central registry entry, if one still becomes necessary, must describe the surviving object after compat cleanup rather than the current module scaffold
