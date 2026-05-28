# 10_API_SPEC

## Nouveaux endpoints

| Endpoint | Méthode | Description |
|---|---|---|
| `GET /metrics` | GET | Métriques agrégées (PnL, Sharpe, drawdown, win rate) |
| `GET /events` | GET | Events trackés (entry, exit, PnL) |
| `GET /events/{id}` | GET | Détail d'un event |
| `GET /positions` | GET | Positions (candidate, active, closed) |
| `GET /positions/{id}` | GET | Détail d'une position |

## Format réponse

```json
{
  "metrics": {
    "total_pnl": 1234.56,
    "win_rate": 0.65,
    "sharpe_ratio": 1.42,
    "max_drawdown": -0.12,
    "profit_factor": 2.1,
    "total_trades": 100,
    "winning_trades": 65
  }
}
```

## Structure

```text
perf/
  perf_app.py              <- existant, ajouter endpoints
  routes/
    metrics.py
    events.py
    positions.py
```
