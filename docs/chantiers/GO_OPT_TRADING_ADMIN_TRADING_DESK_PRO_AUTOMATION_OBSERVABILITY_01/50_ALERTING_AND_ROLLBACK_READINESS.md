---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01_ALERTING
doc_type: alerting_and_rollback_readiness
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 50_ALERTING_AND_ROLLBACK_READINESS - Alerting and Rollback Readiness

## Rollback readiness

- rollback deja documente: YES
- rollback execute dans ce GO: NO
- condition de rollback immediate: erreur de unit file, run non desire, comportement inattendu, ou demande explicite

## Rollback commande

```bash
sudo systemctl disable --now desk_pro_dry_run.timer || true
sudo rm -f /etc/systemd/system/desk_pro_dry_run.service
sudo rm -f /etc/systemd/system/desk_pro_dry_run.timer
sudo systemctl daemon-reload
sudo systemctl reset-failed desk_pro_dry_run.service desk_pro_dry_run.timer || true
```

## Minimum observability before future manual start

- status timer/service re-verifie juste avant start
- `journalctl` vide ou compris avant start
- destination des artefacts ciblee et reconnue
- rollback operable confirme
- aucun indice de dependance live non desiree

## Alerting position

- aucune alerte supplementaire n'est configuree dans ce GO
- l'alerte minimale disponible est la lecture systemd et journal
- un GO futur peut ajouter une surface d'observabilite plus explicite avant tout smoke runtime
