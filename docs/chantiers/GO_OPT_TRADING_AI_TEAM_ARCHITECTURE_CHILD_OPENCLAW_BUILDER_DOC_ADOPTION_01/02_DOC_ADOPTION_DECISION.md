# 02_DOC_ADOPTION_DECISION

## Decision summary

```text
DOC_ADOPTION_STATUS = PASS
FINAL_DECISION = DOC_PACK_ADOPTED_LOCAL
ADOPTION_SCOPE = LOCAL_CHILD_REFERENCE
GLOBAL_INDEX_UPDATE = false
RUNTIME_PATCH = false
GATEWAY_TOKEN_FIX = false
```

## Adopted documents

| Document                         | Decision                       | Adopted role                                                 | Scope limit                            |
| -------------------------------- | ------------------------------ | ------------------------------------------------------------ | -------------------------------------- |
| `BUILDER_OPERATIONAL_GUIDE.md`   | ADOPTED_LOCAL                  | Operator reference for controlled builder documentation jobs | Local child reference only             |
| `BUILDER_ARCHITECTURE_VIEW.md`   | ADOPTED_LOCAL                  | Builder/gateway/fallback architecture reference              | Does not validate or fix gateway token |
| `BUILDER_CONTROLLED_WORKFLOW.md` | ADOPTED_LOCAL                  | Gate → execution log → closeout workflow reference           | Does not create runtime authority      |
| `BUILDER_SECURITY_GUARDRAILS.md` | ADOPTED_LOCAL_WITH_SCOPE_LIMIT | Builder-specific no-SSH/no-runtime/no-index guardrails       | Not a global security policy           |

## Adoption rules

```text
USE_AS_REFERENCE_FOR_FUTURE_BUILDER_CHILDREN = true
MOVE_DOCS = false
RENAME_DOCS = false
GLOBAL_INDEX_UPDATE = false
ACTIVE_STREAMS_UPDATE = false
RUNTIME_AUTHORITY_CREATED = false
```

## Risk handling

```text
RISK_1 = documents may be mistaken for global governance
MITIGATION_1 = adoption is local only

RISK_2 = gateway token mismatch may be perceived as resolved
MITIGATION_2 = explicitly keep token issue unresolved

RISK_3 = workflow doc may be used to justify runtime mutation
MITIGATION_3 = preserve gate and no-runtime-patch boundary
```

## NEXT_GO

```text
GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_DOC_INDEXATION_REVIEW_01
```

## 17_RESUME_POINT

Proceed to closeout of this adoption child. Any global indexation or broader integration must be handled in a separate review GO.

## RISKS

- À qualifier.
