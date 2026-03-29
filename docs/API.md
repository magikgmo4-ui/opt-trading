# API — Endpoints (résumé)

## Webhook
- `POST /tv` : reçoit alertes TradingView (JSON object + key)
  - sizing runtime dépend de `/opt/trading/state/risk_config.json`
  - convention canonique `risk_pct` pour les comptes runtime: fraction décimale (`0.01 = 1%`, `0.02 = 2%`)
  - compat legacy: les valeurs `> 1` sont encore interprétées comme des pourcentages entiers (`2` => `2%`), mais sont à éviter dans les configs courantes
- `GET /dash` : UI dashboard (webhook)
- `GET /api/state` / `/api/events` / `/api/metrics` : données UI

## Performance
- `POST /perf/event` : OPEN/UPDATE/CLOSE
- `GET /perf/summary`
- `GET /perf/equity`
- `GET /perf/open`
- `GET /perf/trades?limit=50&engine=...&status=OPEN|CLOSED&symbol=...`
- `GET /perf/ui`

## Exemples curl
```bash
curl -s http://127.0.0.1:8010/perf/open
curl -s "http://127.0.0.1:8010/perf/trades?limit=5"
```
