# 90_CHILD_CLOSEOUT

## Verdict

```text
CHILD_STATUS = PASS
PATCH_STATUS = PASS
GATEWAY_DIRECT_WORKING = true (ghost user)
TOKEN_COMMITTED = false
TOKEN_PRINTED = false
RUNTIME_MODULE_PATCHED = false
GLOBAL_INDEX_UPDATED = false
```

## 1_MASTER_TARGET

Appliquer la réconciliation du token gateway et valider que le gateway direct fonctionne.

## 3_INITIAL_NEED

Le warning `gateway token mismatch` bloquait le gateway direct lors des invocations builder. Ce child a identifié que le problème venait de l'invocation `sudo -u openclaw openclaw agent`, pas d'une mauvaise config token.

## Root cause (final)

```text
Gateway process = ghost user (PID 9541)
Previous invocation = sudo -u openclaw openclaw agent (wrong user context)
Fix = invoke builder as ghost user directly
```

## 13_ESTABLISHED

```text
BRANCH = go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_GATEWAY_TOKEN_RECONCILIATION_PATCH_01
OPEN_COMMIT   = 96c1c8f4
GATE_COMMIT   = c2ee304e
```

## Patch summary

```text
Phase 1: set openclaw.remote.token = openclaw.auth.token → still failed
Phase 2: root cause deepened — gateway runs as ghost, not openclaw
Phase 3: set openclaw.remote.token = ghost.auth.token → still failed
Phase 4: run as ghost directly → gateway direct works, no mismatch
```

## Correct invocation going forward

```text
# CORRECT — gateway direct, no mismatch
openclaw agent --agent builder --message "..." --json

# INCORRECT — causes token mismatch, falls back to embedded
sudo -u openclaw openclaw agent --agent builder --message "..." --json
```

## Artifacts

| File                          | Status   |
| ----------------------------- | -------- |
| `00_INITIAL_PROJECT_DOC.md`   | created  |
| `01_PATCH_GATE.md`            | PASSED   |
| `02_PATCH_EXECUTION_LOG.md`   | PASS     |
| `90_CHILD_CLOSEOUT.md`        | closeout |

## Scope limits preserved

```text
NO_TOKEN_COMMITTED = true
NO_TOKEN_PRINTED = true
NO_SSH = true
NO_RUNTIME_MODULE_PATCH = true
NO_GLOBAL_INDEX_UPDATE = true
```

## NEXT_GO

```text
None required. Gateway direct validated for ghost user.
```

## 17_RESUME_POINT

After merge, resume from `sot/mainline`.
Builder invocations must use `openclaw agent` as `ghost` user directly.
