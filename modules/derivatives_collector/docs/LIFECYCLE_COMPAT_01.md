# Lifecycle compatibility runner 01

## Purpose

This runner adds a minimal collector-family lifecycle layer on top of the existing `derivatives_collector` without removing current JSON / CSV exports.

## What it adds

Alongside existing derivatives exports in `OUTPUT_DIR`, the runner writes:
- `manifest.json`
- `status.json`
- `latest.json`
- `events.jsonl`
- `errors.jsonl`

## Preservation rules

- current JSON / CSV exports remain valid
- derivatives metrics semantics remain unchanged
- no spot schema is reused
- this runner is additive and separate from the historical command surface

## Usage

From repo root:

```bash
bash modules/derivatives_collector/scripts/lifecycle_compat.sh collect
bash modules/derivatives_collector/scripts/lifecycle_compat.sh sample
bash modules/derivatives_collector/scripts/lifecycle_compat.sh status
```

## Notes

- `collect` uses the configured data source
- `sample` forces `mock`
- lifecycle artifacts are written in the same output directory as the existing derivatives exports
