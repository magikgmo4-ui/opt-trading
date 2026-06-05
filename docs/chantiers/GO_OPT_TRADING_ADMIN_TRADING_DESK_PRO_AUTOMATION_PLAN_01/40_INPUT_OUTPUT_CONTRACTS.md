---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01_IO_CONTRACTS
doc_type: input_output_contracts
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 40_INPUT_OUTPUT_CONTRACTS - Input Output Contracts

## Matrice IO

| Artifact | Producer | Consumer | Path/ref | Freshness | Required | Failure mode |
| --- | --- | --- | --- | --- | --- | --- |
| `signal_event` V1 | webhook V0 + adapter | Desk Pro dry-run | `state/events.jsonl` via `read_events_v1()` | event-driven | non au boot, oui pour event enrichi | degrade en synthese sans signal |
| `visual_context` V1 | headless/ShareX/doc contract | Desk Pro | ref logique ou sidecar | doit etre coherent avec snapshot | non si snapshot suffit | degrade vers snapshot-only |
| `desk_snapshot` | desk_bridge + ingest | Desk Pro | `desk/snapshots/latest.json` | frais requis | **oui** | run refuse ou marque stale |
| `tv_inputs_latest` | capture inputs | Desk Pro | `desk/inputs/tv_inputs_latest.json` | stale aujourd'hui | non tant que bypass possible | log warning |
| `desk_state` | aggregator | Desk Pro / dashboard | `desk/state/latest.json` | stale aujourd'hui | non dans phase 1 | bypass + warning |
| synthesis output | Desk Pro dry-run | operator / shared latest | path a definir | current-run | oui | run marked error |

## Inputs minimum pour phase 1

- `desk_snapshot` frais
- `signal_event` V1 optionnel
- `visual_context` reference optionnelle

## Outputs cibles pour phase 1

1. `latest` JSON de synthesis
2. report texte/markdown
3. status d'execution clair: `ok`, `stale`, `partial`, `error`

## Semantiques

### Freshness

- `desk_snapshot` stale => ne pas produire une synthese nominale
- `signal_event` absent => synthese partielle autorisee
- `visual_context` absent mais snapshot present => synthese visuelle indirecte autorisee

### Missing

- missing `desk_snapshot` = blocking
- missing `signal_event` = non-blocking
- missing `visual_context_ref` = non-blocking
- missing `desk_state` / `tv_inputs` = warning dans phase 1

### Error

- parse error input => `status=error`
- stale input critique => `status=stale`
- partial artifact set => `status=partial`
- successful dry-run => `status=ok`

## RISKS

- À qualifier.
