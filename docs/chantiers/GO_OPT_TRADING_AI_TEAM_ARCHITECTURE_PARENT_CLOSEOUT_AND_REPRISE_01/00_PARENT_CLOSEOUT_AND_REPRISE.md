# 00_PARENT_CLOSEOUT_AND_REPRISE

## 1_MASTER_TARGET

Consolider la séquence OpenClaw builder/gateway après fermeture complète des chaînes Builder Docs et Gateway Token.

## 7_CANONICAL_STATE

```text
SURFACE = OPENCLAW_BUILDER_GATEWAY
STATE = COMPLETE_AT_REST

BUILDER_DOCS_CHAIN = COMPLETE_AT_REST
GATEWAY_TOKEN_CHAIN = COMPLETE_AT_REST

REPO = sot/mainline
WORKING_TREE = clean
```

## 13_ESTABLISHED

```text
Builder documentation chain:
- FIRST_CONTROLLED_JOB   → MERGED_PASS
- DOC_TASK_DRY_RUN       → MERGED_PASS
- DOC_PLAN_REVIEW        → MERGED_PASS
- DOC_WRITING            → MERGED_PASS
- DOC_ADOPTION           → MERGED_PASS
- DOC_INDEXATION_REVIEW  → MERGED_PASS

Gateway token chain:
- REVIEW                 → MERGED_PASS
- PATCH                  → MERGED_PASS
```

## Gateway finding consolidé

```text
GATEWAY_USER = ghost
CORRECT_INVOCATION = openclaw agent as ghost
INCORRECT_INVOCATION = sudo -u openclaw openclaw agent
TOKEN_RECONCILIATION = completed
NEXT_GO_REQUIRED = false
```

## 12_INVARIANTS

```text
NO_RUNTIME_PATCH = true unless separately gated
NO_GLOBAL_INDEX_UPDATE = true unless explicitly required
NO_SSH = true unless separately gated
NO_OPEN_TECHNICAL_CHILD = true without validated need
```

## Optional follow-ups

```text
OPTIONAL_ONLY:
GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_DOC_INBOX_POINTER_01

CONDITION:
Only if discoverability becomes a real need.
```

## 17_RESUME_POINT

```text
REPRISE:
- Start from sot/mainline clean.
- Builder Docs and Gateway Token chains are complete at rest.
- Correct builder invocation is as ghost.
- No mandatory NEXT_GO.
- Before opening new work, choose a new product surface from MACHINE_WORK_SPLIT / ACTIVE_STREAMS.
```

## RISKS

- À qualifier.
