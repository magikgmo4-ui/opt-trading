# 02_GATEWAY_TOKEN_DECISION

## Decision summary

```text
GATEWAY_TOKEN_REVIEW_STATUS = PASS
ROOT_CAUSE_CONFIRMED = true
FINAL_DECISION = TOKEN_RECONCILIATION_NEEDED_WITH_SEPARATE_PATCH_GATE
PATCH_IN_THIS_COMMIT = false
RUNTIME_PATCH_ALLOWED_NOW = false
SECRET_EXPOSURE_ALLOWED = false
```

## Root cause

```text
gateway.auth.token = PRESENT under openclaw user config
gateway.remote.token = ABSENT under openclaw user config
ghost gateway.remote.token = ABSENT

ERROR:
unauthorized: gateway token mismatch
(set gateway.remote.token to match gateway.auth.token)
```

## Operational meaning

The gateway direct path fails because the client-side `gateway.remote.token` is not configured to match the gateway-side `gateway.auth.token`.

The embedded fallback can continue to work, but it does not validate direct gateway connectivity and does not provide the same gateway session tracking guarantees.

## Decision

```text
TOKEN_RECONCILIATION_NEEDED = true
PATCH_REQUIRED = true
PATCH_SCOPE = local OpenClaw gateway client config only
PATCH_ALLOWED_IN_THIS_CHILD = false
PATCH_REQUIRES_NEXT_GATE = true
```

## Required next gate before any patch

A separate gated patch step must explicitly validate:

```text
1. No token value printed to terminal.
2. No token committed.
3. No token copied into repository files.
4. Patch applies only to local OpenClaw runtime config.
5. gateway.remote.token becomes present.
6. gateway.remote.token matches gateway.auth.token.
7. gateway direct health/probe works after patch.
8. fallback remains available.
```

## Forbidden actions

```text
FORBIDDEN:
- commit token values
- echo token values
- write token into docs
- modify global indexes
- patch runtime modules
- perform SSH
- change gateway auth token unless explicitly gated later
```

## Recommended NEXT_GO

```text
GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_GATEWAY_TOKEN_RECONCILIATION_PATCH_01
```

## 17_RESUME_POINT

Close this review child after decision. Then open the patch child only if token reconciliation is approved.
