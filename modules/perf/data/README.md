# PERF data

Canonical candidate location for PERF runtime data.

## Current decision

- historical default DB path remains `perf/perf.db`
- canonical target candidate is `modules/perf/data/perf.db`
- any effective switch must be controlled via `PERF_DB_PATH`

## Scope of current implementation

- no automatic runtime switch
- no destructive move
- relocation tooling only
