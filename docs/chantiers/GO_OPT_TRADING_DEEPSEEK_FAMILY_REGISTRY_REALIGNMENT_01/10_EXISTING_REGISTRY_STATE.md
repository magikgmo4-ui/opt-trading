---
go_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_REGISTRY_REALIGNMENT_01
doc_type: EXISTING_STATE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 10_EXISTING_REGISTRY_STATE

## Observed state

- `scripts/ai/menu/opt_trading_menu.json` already exposes `deepseek_hub`, `deepseek_response`, `deepseek_thinking`, and an archived `deepseek_student` entry.
- `registry/modules_registry.yaml` has no `deepseek_*` entries.
- `registry/wrappers_registry.yaml` has no `deepseek_*` wrapper entries.
- `registry/ui_surfaces_registry.yaml` has no DeepSeek operator surface.

## Consequence

The central registries under-describe a family that is already materially present in the repo and in operator navigation.

## Scope decision for this lot

- Add `deepseek_hub` as the operator hub / documentary owner.
- Add `deepseek_response` and `deepseek_thinking` as active compatibility components.
- Keep `deepseek_student` outside central registries for now because this lot does not introduce a new central `legacy` status model and does not settle the physical/runtime boundary with `scripts/student/` and `student/scripts/`.
