---
doc_id: GO_DESKPRO_INPUT_EXPANSION_01_CURRENT_INPUT_SURFACES
doc_type: inventory
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_01
status: reference
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01/20_INPUT_CONSUMER_MAP.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DRY_RUN_IMPL_01/30_IMPLEMENTATION_NOTES.md
---

# 10_CURRENT_INPUT_SURFACES - Inputs réels (repo)

## Inputs prouvés

| Input | Statut | Preuve | Format |
| --- | --- | --- | --- |
| `desk_snapshot` | CONFIRMED | `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01/20_INPUT_CONSUMER_MAP.md` | dict `{symbol, tf, snapshot_ts, path, ...}` |
| `signal_event` | AVAILABLE | `modules/desk_pro/signal_event_adapter.py` | dict V0 (events.jsonl) → dict V1 `signal_event` |
| `visual_context` | AVAILABLE | `modules/desk_pro/dry_run.py` | dict V1 minimal `{source,capture_id,symbol,timeframe,captured_at,image_ref,status}` |

## Consumer surfaces Desk Pro

| Surface | Preuve | Rôle |
| --- | --- | --- |
| Dry-run synthesis 3 inputs | `modules/desk_pro/dry_run.py` | jointures + warnings/errors + safety flags |
| Tests smoke 3 inputs | `tests/test_desk_pro_combined_input_smoke.py` | prouve synthèse “signal_event + visual_context + desk_snapshot” |
| UI/API | `modules/desk_pro/api/routes.py` ; `modules/desk_pro/ui/page.py` | consumer UI |

## Conclusion

Desk Pro consomme déjà `desk_snapshot` et peut consommer `signal_event` + `visual_context` via un contrat V1. L’expansion doit formaliser les classes d’inputs et la politique de jointure avant d’ajouter des producers supplémentaires (vision/headless, telegram claims, metrics).
