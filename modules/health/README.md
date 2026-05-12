# health

Unified observability module for automation surface health checks.

## Commands

```bash
bash modules/health/scripts/health-check          # text output
bash modules/health/scripts/health-check --json   # JSON machine-readable
bash modules/health/scripts/health-check perf bot_vision  # filter surfaces
bash modules/health/scripts/health-alert                # alerting (Phase 2)
bash modules/health/scripts/health-dashboard            # dashboard (Phase 3)
bash modules/health/scripts/health-dashboard --json     # JSON export
bash modules/health/scripts/health-dashboard --html     # HTML static
```

## Status

```text
healthy  = surface is responding correctly
degraded = surface responds but with issues
down     = surface is not reachable
unknown  = could not determine status
```

## Phase 1 scope

- health check contract JSON
- registry of 10 automation surfaces
- cmd-health CLI with text and JSON output
- no alerting, no dashboard runtime, no circuit breakers
