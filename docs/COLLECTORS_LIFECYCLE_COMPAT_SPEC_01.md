# Collectors lifecycle compat spec 01

## 1. Purpose

This spec freezes the minimal lifecycle compatibility target for `modules/derivatives_collector` under the collector-family doctrine.

This is still a documentation/specification pass.
It does not implement the compatibility layer.
It defines the exact target semantics that a future additive patch would need to follow.

## 2. Compatibility rules

- additive only
- existing JSON / CSV derivatives exports remain valid
- no derivatives business semantics are changed
- no spot schema reuse is forced
- no current downstream consumer may be broken by the first compatibility pass

## 3. Required lifecycle field set

### 3.1 Core identity fields
Every lifecycle artifact in the compatibility family should carry:
- `contract_version`
- `module_id`
- `provider_id` when applicable
- `run_id`
- `generated_at`

### 3.2 Minimal meanings
- `contract_version`
  - lifecycle compatibility contract version
  - fixed to `v1` in the first pass
- `module_id`
  - fixed to `derivatives_collector` for this module
- `provider_id`
  - optional in the family module context
  - may remain absent or null when one run spans multiple sources
  - must not be faked when the run is genuinely multi-source
- `run_id`
  - unique identifier for one collector run
- `generated_at`
  - UTC timestamp with trailing `Z`

## 4. Lifecycle vocabulary

### 4.1 State vocabulary
`status.json` should converge toward the family vocabulary:
- `never_run`
- `running`
- `healthy`
- `degraded`
- `stale`
- `failed`

### 4.2 Freshness vocabulary
- `fresh`
- `stale`
- `unknown`

### 4.3 Error class vocabulary
- `recoverable`
- `non_recoverable`

### 4.4 Retryability vocabulary
- `retryable` as boolean
- `retry_after` as absolute UTC timestamp when known

## 5. Artifact family meanings in the derivatives context

### 5.1 `manifest.json`
Meaning:
- discovery and compatibility summary for the latest valid derivatives output set

Must contain at minimum:
- core identity fields
- artifact inventory
- derivatives output inventory summary
- compatibility notes indicating that legacy JSON / CSV exports remain authoritative downstream outputs

### 5.2 `status.json`
Meaning:
- deterministic current-state file for the derivatives collector lifecycle

Must contain at minimum:
- core identity fields
- `state`
- `freshness_state`
- `last_event_at`
- `last_success_run_id`
- `last_success_at`
- `last_failure_run_id`
- `last_failure_at`
- `active_run_id`
- `last_error_code`
- `retryable`
- `retry_after`
- `message`

### 5.3 `latest.json`
Meaning:
- pointer to the latest valid derivatives output set

Must contain at minimum:
- core identity fields
- references to the latest derivatives outputs
- compatibility summary of what the latest derivatives package contains
- no fake normalized spot-style schema

### 5.4 `events.jsonl`
Meaning:
- append-only lifecycle history for derivatives collector runs

Each line must contain at minimum:
- core identity fields
- `event_id`
- `event_at`
- `event_type`
- `level`
- `message`
- `state_after`

### 5.5 `errors.jsonl`
Meaning:
- append-only structured failure history for derivatives collector runs

Each line must contain at minimum:
- core identity fields
- `error_id`
- `error_at`
- `error_code`
- `error_class`
- `retryable`
- `message`
- `stage`
- optional transport / provider detail when relevant

## 6. Mapping from current derivatives outputs to family artifacts

### 6.1 Current derivatives outputs
Current documented downstream outputs remain:
- JSON exports
- CSV exports

### 6.2 Compatibility mapping target
- `latest.json`
  - should point to the latest valid derivatives output set
  - should summarize which derivatives export files belong to that set
- `manifest.json`
  - should inventory the same output set in a more complete discovery format
  - should declare compatibility notes and file inventory

### 6.3 Preservation rule
- neither `latest.json` nor `manifest.json` replaces current derivatives exports in the first pass
- they act as family-level lifecycle and discovery companions

## 7. Minimal event vocabulary

Recommended minimal `event_type` set:
- `run_started`
- `source_fetch_started`
- `source_fetch_succeeded`
- `source_fetch_failed`
- `outputs_published`
- `run_succeeded`
- `run_failed`

This is a family-level vocabulary.
It does not prescribe how derivatives business payloads are shaped.

## 8. Minimal error vocabulary

Recommended minimal `error_code` categories:
- `configuration_error`
- `source_request_error`
- `source_auth_error` when applicable
- `normalization_error`
- `output_write_error`
- `unknown_error`

Recommended minimal `stage` categories:
- `configuration`
- `source_fetch`
- `normalization`
- `publish`
- `lifecycle`

## 9. What this spec deliberately avoids

- forcing one provider id for genuinely multi-source runs
- forcing spot-family normalized contracts onto derivatives outputs
- removing or renaming current derivatives exports
- forcing runtime extraction into `collectors_core`

## 10. Recommended next trigger

GO_COLLECTORS_LIFECYCLE_COMPAT_PATCH_01

## RISKS

- À qualifier.
