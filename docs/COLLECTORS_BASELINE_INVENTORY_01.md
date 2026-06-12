# Collectors baseline inventory 01

## 1. Collector surfaces in scope
- `modules/derivatives_collector`
- `packages/collectors_core`
- `modules/collector_coingecko`
- `modules/collector_binance_spot`

## 2. Wrappers to inventory
For each surface, inventory:
- `cmd`
- `sanity`
- `menu`
- install / shortcut expectations
- runbook references

## 3. Config files to inventory
For each surface, inventory:
- committed defaults
- local override files
- env overrides
- secret carriers
- compatibility notes

## 4. Artifacts to inventory
For each surface, inventory:
- runtime status artifacts
- latest pointer artifacts
- manifest artifacts
- events / errors history artifacts
- normalized outputs
- raw exports
- CSV / JSON downstream exports

## 5. Downstream consumers to inventory
Identify known or implied consumers of:
- derivatives outputs
- spot normalized outputs
- canonical status / lifecycle artifacts

## 6. Probable runtime duplication areas
Inventory possible duplication around:
- config loading
- env resolution
- HTTP handling
- retry / error classification
- timestamp helpers
- file writing helpers
- lifecycle / run identity handling

## 7. Easy convergence candidates
Likely low-risk candidates:
- vocabulary
- artifact family naming
- runbook language
- operator surface expectations
- config doctrine wording

## 8. Areas to keep separate
Keep separate unless proven otherwise:
- derivatives metrics semantics
- spot snapshot semantics
- provider-specific endpoint logic
- normalized contracts for spot vs derivatives

## 9. Next trigger
GO_COLLECTORS_BASELINE_GAP_MATRIX_01

## RISKS

- À qualifier.
