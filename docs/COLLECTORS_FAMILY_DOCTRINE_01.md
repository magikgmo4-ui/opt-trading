# Collectors family doctrine 01

## Established
- `derivatives_collector` remains the canonical derivatives collector module.
- `collectors_core` is the shared runtime foundation for the newer provider modules.
- `collector_coingecko` and `collector_binance_spot` are validated spot collectors built on `collectors_core`.

## Family doctrine
- collector family stays file-first
- collector family keeps explicit module boundaries
- lifecycle vocabulary should converge around status, latest, manifest, events, and errors artifacts
- config doctrine should converge around committed defaults, local overrides, and env overrides
- operator surface should converge around predictable cmd, sanity, menu, and runbook expectations

## Must remain separate
- derivatives metrics semantics
- spot market snapshot semantics
- provider-specific endpoint logic
- normalized contracts for spot vs derivatives

## Migration rule
- converge docs, lifecycle vocabulary, artifact family, and operator surface first
- do not force immediate runtime migration of `derivatives_collector` into `collectors_core`
- do not add provider #3 before doctrine and migration map are clear

## Next trigger
GO_COLLECTORS_MIGRATION_MAP_01
