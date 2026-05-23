# validation_report

## Scope

```text
GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01
GO_OPT_TRADING_DOC_OPS_METHOD_SESSION_PATCH_TRANSPORT_01
```

## Validation attendue après application locale

| Check | Expected |
|---|---|
| README_PRESENT | PASS |
| MANIFEST_PRESENT | PASS |
| PROMPTS_PRESENT | PASS |
| CHECKLISTS_PRESENT | PASS |
| TEMPLATES_PRESENT | PASS |
| PATCHES_DIR_PRESENT | PASS |
| SESSION_TRANSPORT_TOOLS_PRESENT | PASS |
| NO_SECRETS | PASS |
| GLOBAL_INDEXES_UNTOUCHED | PASS |
| RUNTIME_UNTOUCHED | PASS |
| DOC_ONLY | PASS |
| ROOT_PATCH_NOT_STAGED | PASS |

## Commandes

```bash
git diff --check
find bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01 -maxdepth 5 -type f | sort
find . -maxdepth 1 -type f -name '*.patch' -print
grep -RniE 'token|secret|api_key|apikey|password|passwd|bearer|PRIVATE KEY' \
  bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01 \
  docs/governance/SESSION_PATCH_TRANSPORT_METHOD_01.md \
  docs/governance/GLOBAL_INDEX_UPDATE_TRIGGER_RULE_01.md \
  tools/session_transport || true
```

## Note

Les mots sensibles peuvent apparaître dans les checklists. Les valeurs réelles sont interdites.
