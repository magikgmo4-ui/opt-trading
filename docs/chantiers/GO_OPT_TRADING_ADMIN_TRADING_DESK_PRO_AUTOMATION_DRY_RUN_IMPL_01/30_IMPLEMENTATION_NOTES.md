---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DRY_RUN_IMPL_01_IMPL_NOTES
doc_type: implementation_notes
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DRY_RUN_IMPL_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 30_IMPLEMENTATION_NOTES - Implementation Notes

## Fichiers crees

1. `modules/desk_pro/dry_run.py`
2. `tests/test_desk_pro_dry_run.py`

## API exposee

```python
build_desk_pro_dry_run_synthesis(signal_event, visual_context=None, desk_snapshot=None) -> dict
validate_desk_pro_dry_run_inputs(signal_event, visual_context=None, desk_snapshot=None) -> tuple[bool, list[str]]
run_desk_pro_dry_run(signal_event_payload, visual_context=None, desk_snapshot=None) -> dict
```

## Choix d'implementation

- reutilisation de `normalize_signal_event_v1` et `validate_signal_event_v1`
- validation locale de `visual_context` et `desk_snapshot`
- synthese sous forme de dict simple, sans dependance runtime
- join checks minimaux: timeframe, symbole, besoin de normalisation, reference visuelle

## Ce qui n'a pas ete modifie

- aucun module systemd
- aucun timer
- aucun runner live existant
- aucune fixture historique
- aucun fichier runtime sous `desk/` ou `state/`

## Resultat

Le patch ajoute un point d'execution testable et reutilisable pour les futurs GO timer spec et observability, sans coupler Desk Pro dry-run au runtime reel.
