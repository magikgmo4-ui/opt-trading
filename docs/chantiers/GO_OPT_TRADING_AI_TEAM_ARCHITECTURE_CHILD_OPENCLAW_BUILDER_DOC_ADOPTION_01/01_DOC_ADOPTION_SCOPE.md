# 01_DOC_ADOPTION_SCOPE

## Source

```text
SOURCE_GO = GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_DOC_WRITING_01
SOURCE_STATUS = MERGED_PASS
SOURCE_BASE = sot/mainline
```

## Documents under adoption review

| Document                       | Source path       | Adoption status | Intended role                                      |
| ------------------------------ | ----------------- | --------------- | -------------------------------------------------- |
| BUILDER_OPERATIONAL_GUIDE.md   | previous child GO | PENDING         | Operator reference for controlled builder jobs     |
| BUILDER_ARCHITECTURE_VIEW.md   | previous child GO | PENDING         | Builder/gateway/fallback architecture reference    |
| BUILDER_CONTROLLED_WORKFLOW.md | previous child GO | PENDING         | Gate → execution log → closeout workflow reference |
| BUILDER_SECURITY_GUARDRAILS.md | previous child GO | PENDING         | Builder-specific guardrails reference              |

## Adoption boundaries

```text
LOCAL_ADOPTION_ONLY = true
GLOBAL_INDEX_UPDATE = false
RUNTIME_PATCH = false
GATEWAY_TOKEN_FIX = false
DOC_MOVE_OR_RENAME = false
```

## Adoption criteria

```text
USABLE = document can guide future builder documentation children
BOUNDED = document does not create implicit runtime authority
NON_DUPLICATIVE = document does not replace broader project governance
TRACEABLE = document points back to a merged child GO
SAFE = document preserves no SSH / no runtime patch / no global index update
```

## Initial verdict

```text
DOC_ADOPTION_STATUS = IN_PROGRESS
FINAL_DECISION = PENDING
```
