---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DRY_RUN_IMPL_01_SOURCE_AUDIT
doc_type: source_audit
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DRY_RUN_IMPL_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 10_SOURCE_AUDIT - Source Audit

## Point d'entree minimal retenu

Le point d'entree minimal retenu est un **nouveau module isole**: `modules/desk_pro/dry_run.py`.

## Classement des composants inspectes

| Element | Classement | Motif |
| --- | --- | --- |
| `modules/desk_pro/signal_event_adapter.py` | UTILISABLE | adapter V0->V1 deja stable et teste |
| `tests/test_signal_event_adapter.py` | UTILISABLE | base de validation existante |
| `tests/test_admin_trading_contract_compatibility_smoke.py` | UTILISABLE | fixtures et expectations contractuelles deja en place |
| `modules/desk_pro_runner/app/desk_pro_runner.py` | A ADAPTER | runner existant mais dependant du pipeline orchestration live |
| `modules/desk_pro/service/aggregator.py` | HORS SCOPE | snapshot mock utile comme reference, pas comme entree dry-run cible |
| `modules/desk_pro/models.py` | HYPOTHESE | modeles existants partiels, non necessaires au patch minimal |
| `desk/snapshots/latest.json` contract | UTILISABLE | format stable deja confirme |
| `visual_context` V1 documentaire | UTILISABLE | compatible via dict local ou fixture |

## Decision de patch

- ne pas modifier `desk_pro_runner`
- ne pas brancher le dry-run au runtime existant
- ne pas lire de fichiers live dans le module dry-run
- reutiliser uniquement l'adapter `signal_event` et des dicts/fixtures

## Conclusion

Le plus petit changement correct est un helper autonome dans `modules/desk_pro/`, accompagne d'une suite de tests dediee.

## RISKS

- À qualifier.
