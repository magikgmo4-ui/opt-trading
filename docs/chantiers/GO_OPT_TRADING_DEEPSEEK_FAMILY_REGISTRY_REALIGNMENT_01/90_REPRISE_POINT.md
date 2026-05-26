---
go_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_REGISTRY_REALIGNMENT_01
doc_type: REPRISE_POINT
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 90_REPRISE_POINT

## Summary

- Added `deepseek_hub`, `deepseek_response`, and `deepseek_thinking` to `registry/modules_registry.yaml`.
- Added matching wrapper entries to `registry/wrappers_registry.yaml`.
- Added the canonical `deepseek_hub` operator surface to `registry/ui_surfaces_registry.yaml`.
- Left `deepseek_student` outside central registries in this lot.

## Verification

```bash
git diff --check
python3 -c "import yaml; files=['registry/modules_registry.yaml','registry/wrappers_registry.yaml','registry/ui_surfaces_registry.yaml']; [yaml.safe_load(open(f, encoding='utf-8')) for f in files]; print('yaml-ok')"
rg -n "deepseek_hub|deepseek_response|deepseek_thinking|deepseek_student" registry/
```

## Resume

Prepare the branch diff for review and decide separately whether central registries should later gain an explicit legacy status for `deepseek_student`.
