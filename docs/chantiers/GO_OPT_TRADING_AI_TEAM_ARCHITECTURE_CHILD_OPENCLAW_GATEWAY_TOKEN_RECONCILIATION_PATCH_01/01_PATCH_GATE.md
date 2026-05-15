# 01_PATCH_GATE

## Gate

```text
GATE_STATUS = PENDING
PATCH_SCOPE = local openclaw runtime config only
MUTATION_ALLOWED = true (config file only)
SSH_ALLOWED = false
RUNTIME_MODULE_PATCH_ALLOWED = false
GLOBAL_INDEX_ALLOWED = false
TOKEN_COMMIT_ALLOWED = false
TOKEN_PRINT_ALLOWED = false
TOKEN_IN_DOCS_ALLOWED = false
```

## Patch action

```text
TARGET_FILE = /home/openclaw/.openclaw/openclaw.json
TARGET_KEY  = gateway.remote.token
TARGET_VALUE = <value of gateway.auth.token — never printed, never committed>
METHOD = python3 in-place JSON patch via sudo -u openclaw
```

## PASS criteria

```text
- gateway.remote.token becomes present in openclaw.json
- gateway.remote.token == gateway.auth.token
- no token value printed to terminal
- no token value committed
- no token value written into docs
- openclaw gateway health returns ok after patch
- openclaw gateway probe passes
```

## FAIL criteria

```text
- token value leaked to terminal
- token value committed
- patch fails or corrupts openclaw.json
- gateway health still fails after patch
- any SSH executed
- any runtime module patched
- any global index modified
```
