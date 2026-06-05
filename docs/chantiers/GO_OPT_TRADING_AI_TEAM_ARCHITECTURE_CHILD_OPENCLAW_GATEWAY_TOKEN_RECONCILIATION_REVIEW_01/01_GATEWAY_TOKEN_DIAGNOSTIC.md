# 01_GATEWAY_TOKEN_DIAGNOSTIC

## Error observed

```text
ERROR: gateway connect failed: GatewayClientRequestError:
  unauthorized: gateway token mismatch
  (set gateway.remote.token to match gateway.auth.token)
Gateway target: ws://127.0.0.1:18789
Source: local loopback
Fallback: embedded execution
```

## Source artifacts

```text
- GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_DOC_TASK_DRY_RUN_01
  02_DOC_TASK_DRY_RUN_EXECUTION_LOG.md

- GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01
  02_REMOTE_EXEC_LOG.md
  03_REMOTE_EXEC_STATE.md
```

## Config inspection (live — 2026-05-14)

### User: openclaw

```text
gateway.auth.token   = PRESENT (48 chars)
gateway.remote.token = ABSENT
gateway.remote.url   = not set
gateway.bind         = loopback
gateway.port         = 18789
```

### User: ghost

```text
gateway.remote.token = ABSENT
gateway.remote.url   = not set
```

## Root cause

```text
CAUSE:
The openclaw gateway runs under the `openclaw` user with a valid `gateway.auth.token`.
When `openclaw agent` is called (as ghost or openclaw), the client attempts to connect
to ws://127.0.0.1:18789 and must present `gateway.remote.token` matching `gateway.auth.token`.

Neither the `ghost` user config nor the `openclaw` user config has `gateway.remote.token` set.
The gateway rejects the connection with token mismatch, then the CLI falls back to embedded execution.

SUMMARY:
gateway.remote.token is missing from the connecting client config.
It must be set to the same value as gateway.auth.token for direct gateway calls to succeed.
```

## Impact

```text
CURRENT_IMPACT = LOW
- embedded fallback works for documentation dry-run tasks
- structured responses are produced correctly
- no data loss, no security exposure

FUTURE_IMPACT = MEDIUM
- direct gateway provides better session management and auditability
- without gateway.remote.token, all builder calls fall back to embedded
- embedded mode bypasses gateway session tracking
```

## Diagnostic verdict

```text
DIAGNOSTIC_STATUS = COMPLETE
ROOT_CAUSE_IDENTIFIED = true
ACTION_REQUIRED = TOKEN_RECONCILIATION_NEEDED
PATCH_ALLOWED_IN_THIS_CHILD = pending gate
```

## RISKS

- À qualifier.
