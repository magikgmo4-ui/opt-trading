# LocalCMS Metrics Dashboard — Closeout

## Résultat

```
LOCALCMS_METRICS_DASHBOARD = PASS
```

## Implémentation

### Nouveau helper `_build_metrics()`

Lit tous les `data/journal/daily/*.json` et `data/journal/sync_log.jsonl`.
Retourne un dict avec : `total_runs`, `pass_count`, `fail_count`,
`win_count`, `loss_count`, `breakeven_count`, `pnl_cumulative`, `win_rate`,
`last_run`, `sheets_sync`, `generated_at`.

### Nouveaux endpoints

| Endpoint         | Réponse | Description                        |
| ---------------- | ------- | ---------------------------------- |
| `GET /metrics`   | HTML    | Dashboard visuel (runs, P&L, TMUX, Sheets) |
| `GET /metrics/daily` | JSON | API métriques daily session    |

### Sidebar mise à jour

Section "Metrics / Dashboard" ajoutée dans :
- Vue journal (`/journal`)
- Vue détail journal (`/journal/{run_id}`)
- Dashboard principal (`/` / `/ui`)

## Données réelles au moment du closeout

```json
{
  "total_runs": 13,
  "pass_count": 13,
  "fail_count": 0,
  "win_count": 13,
  "pnl_cumulative": 5694.39,
  "win_rate": 1.0,
  "last_run": {
    "run_id": "20260516_013",
    "outcome": "win",
    "net_pnl": 438.03,
    "validation_verdict": "APPROVED"
  },
  "sheets_sync": {
    "dry_run": 5,
    "written": 1,
    "blocked": 2,
    "failed": 0
  }
}
```

## Tests

```
10 nouveaux tests — TestLocalCMSMetricsDashboard
42/42 total PASS
```

Tests couverts :
- Routes `/metrics` et `/metrics/daily` présentes
- `_build_metrics()` retourne dict avec toutes les clés requises
- `pass_count + fail_count == total_runs`
- `win + loss + breakeven <= total_runs`
- `0 <= win_rate <= 1.0`
- `sheets_sync` a les 4 clés
- GET uniquement (no POST/PUT/DELETE)
- `SYNC_LOG` constant défini

## Invariants

- Read-only : aucun endpoint d'écriture ajouté ✓
- No secrets in repo/logs ✓
- No automatic Sheets write ✓
- No live trade ✓
- No Bitget order ✓
