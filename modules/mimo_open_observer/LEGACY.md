# mimo_open_observer legacy state

## Canonical status

`mimo_open_observer` is preserved as archival residue.

It is no longer treated as a default active runtime line.

## What remains on purpose

- code and docs for historical traceability
- fixtures and produced local data for evidence
- wrapper and scheduler files as bounded archive surfaces

## What changed

- active runtime commands are blocked by default
- shortcut installation is blocked by default
- scheduler wrapper is blocked by default
- explicit opt-in is required to run residual runtime commands:

```bash
MIMO_OPEN_OBSERVER_ALLOW_ARCHIVED_RUNTIME=1 bash modules/mimo_open_observer/cmd.sh ...
```

## Why this exists

Historical consolidation docs classify the module as `CLOSED (student)` and archive-oriented, while the repo still contains runnable assets. This file marks the module as preserved evidence rather than active product surface.
