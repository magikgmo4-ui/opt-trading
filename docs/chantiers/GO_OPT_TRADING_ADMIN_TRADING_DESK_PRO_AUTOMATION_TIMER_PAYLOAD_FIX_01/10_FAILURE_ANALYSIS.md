---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_PAYLOAD_FIX_01_FAILURE_ANALYSIS
doc_type: failure_analysis
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_PAYLOAD_FIX_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 10_FAILURE_ANALYSIS - Failure Analysis

## Timer pause before patch

- `sudo systemctl stop desk_pro_dry_run.timer`: executed
- timer post-stop: `inactive`
- service post-stop: `inactive`
- manual service start: `NO`

## Error analysis

| Erreur | Cause probable | Fix applique | Bloquant |
| --- | --- | --- | --- |
| `missing engine` | script emet un payload incomplet | ajout de `engine` V0 | Oui |
| `invalid direction: 'LONG'` | direction hors enum adapte | `signal=BUY` V0 | Oui |
| `missing timestamp` | aucun `_ts` fourni | `_ts` UTC genere | Oui |
| `unexpected source: 'timer_trigger'` | source manuelle non canonique | laisser l'adapter definir `tradingview.webhook` | Oui |
| `unexpected event_type: 'signal'` | event_type hors contrat V1 | laisser l'adapter definir `signal_event` | Oui |
| `desk_snapshot missing` | snapshot absent en timer-only | degrade en warning non bloquant | Non |

## Root cause summary

Le probleme etait double:

- `modules/desk_pro/desk_pro_dry_run.sh` construisait un faux payload V1 partiel au lieu d'un payload V0 compatible adaptateur
- `modules/desk_pro/dry_run.py` traitait `desk_snapshot` absent comme une erreur bloquante alors que le mode timer-only dry-run doit tolérer son absence
