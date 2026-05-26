---
go_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_REGISTRY_REALIGNMENT_01
doc_type: DECISION
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 20_REALIGNMENT_DECISION

## Registry changes in this lot

1. `modules_registry.yaml`
Add three active entries:
- `deepseek_hub`
- `deepseek_response`
- `deepseek_thinking`

2. `wrappers_registry.yaml`
Add the wrapper triplets required to operate the same three modules from the central wrapper registry.

3. `ui_surfaces_registry.yaml`
Expose only `deepseek_hub` as the canonical operator surface for the family.

## Explicit non-change

`deepseek_student` is intentionally not added to central registries in this lot.

Reason:
The consolidation verdict classifies it as legacy/transitional, but the central registries currently model active/beta/ready states only. A dedicated follow-up lot can decide whether to extend the registry vocabulary or close the physical/runtime boundary first.
