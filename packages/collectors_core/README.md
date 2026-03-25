# collectors_core

Shared platform package for minimal cross-module runtime concerns.

Responsibility boundary:
- config boundary
- env and secrets resolution boundary
- HTTP policy
- retry and backoff
- rate limiting
- validation hooks
- structured logging
- manifest and status helpers
- common errors and lifecycle helpers

Implemented in the pilot scope:
- TOML config loading with deterministic layer order
- environment override expansion using the module_id prefix rule
- JSON and JSONL artifact writing helpers
- UTC timestamp helpers
- minimal JSON HTTP client wrapper

Still not in scope here:
- provider-specific auth or endpoints
- deployable module behavior
