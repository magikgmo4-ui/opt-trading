---
go_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_REGISTRY_REALIGNMENT_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Realign the central registries with the DeepSeek family consolidation verdict.

## 2_INITIAL_PROJECT_DOC
This document.

## 3_INITIAL_NEED
`deepseek_hub`, `deepseek_response`, and `deepseek_thinking` are visible in the repo and in the operator menu, but they are still absent from the central registries. The family verdict from `GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01` must now be reflected in registry truth without touching runtime behavior.

## 4_MASTER_PROJECT_PLAN
1. Record the existing registry gap and the chosen alignment scope.
2. Add the active DeepSeek family entries to central registries.
3. Keep `deepseek_student` out of central registries for this lot and document why.
4. Verify the resulting diff stays registry-only plus chantier docs.

## 6_FINAL_TARGET
Central registries describe `deepseek_hub` as the family hub and `deepseek_response` / `deepseek_thinking` as active compatibility components, with no runtime or global index mutation.

## 7_CANONICAL_STATE
- `registry/modules_registry.yaml` contains the active DeepSeek family entries for this lot.
- `registry/wrappers_registry.yaml` contains the related wrappers.
- `registry/ui_surfaces_registry.yaml` exposes the operator hub surface.
- `deepseek_student` remains documented outside central registries until a dedicated physical/runtime closure lot handles it.

## 12_INVARIANTS
- No runtime behavior change.
- No modification of `scripts/student/`, `student/scripts/`, or DeepSeek module code.
- No modification of global indexes.
- No change to `secrets/`.

## 16_TODO
- [x] Inspect current DeepSeek registry gap
- [x] Decide the central registry scope for this lot
- [x] Apply registry updates
- [x] Verify resulting scope and consistency

## 17_RESUME_POINT
Registry realignment applied and verified locally. Next natural step is PR creation / review for this lot, then a dedicated decision lot for the `deepseek_student` central registry status if still needed.
