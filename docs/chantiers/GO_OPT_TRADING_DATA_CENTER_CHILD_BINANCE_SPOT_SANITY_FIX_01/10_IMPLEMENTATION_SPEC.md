# Implementation Spec

## Change
Extract the repeated runtime directory setup into a local helper `_ensure_runtime_directories(config)`.

## Behavior
- `run_sanity()` calls the helper before requirement validation.
- `run_collection()` reuses the same helper.
- No new status artifact is written by `run_sanity()`.
