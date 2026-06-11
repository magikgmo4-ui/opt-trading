# GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_LIVE_RUNTIME_VALIDATION_01

## Objectif

Monitoring runtime 24h du Data Center — valider que les 28 contrats restent PROVEN, que le pipeline horaire tourne, et que LocalCMS répond.

## Contexte

- Phase construction terminée (13 PRs mergées)
- 28 contrats canonisés (20 PROVEN, 8 PARTIAL)
- Pipeline hourly automatisé (16 producers)
- LocalCMS live sur :8700

## Scope

- ❌ Pas de nouveaux contrats
- ❌ Pas de modification de producers (sauf bug bloquant)
- ✅ Observer freshness / failures / partials
- ✅ Capturer preuves runtime toutes les 4-6h
- ✅ Produire rapport final après 24h

## Script de monitoring

```bash
bash scripts/data_center/live_runtime_validation_24h.sh
```

Capture un snapshot JSON + log dans `runtime_snapshots/`.

## Critères de succès

- Validator PASS
- Hourly pipeline confirmé
- LocalCMS répond (4 endpoints)
- 28 contrats audités (fraîcheur)
- 20 PROVEN maintenus
- 8 PARTIAL avec next_action documenté
- Aucun crash bloquant
