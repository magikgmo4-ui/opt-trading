---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_01
doc_type: current_state
repo: opt-trading
status: open
created_at: 2026-05-17
source_prouvee: modules/localcms/app/main.py — _build_metrics() lignes 174-250
---

# 10_LOCALCMS_CURRENT_EXPOSURE

État réel de ce que LocalCMS expose aujourd'hui, dérivé de la source
`modules/localcms/app/main.py` — fonction `_build_metrics()`.

---

## Endpoint actuel

```
GET /metrics/daily  → JSON
GET /metrics        → HTML dashboard
```

---

## Réponse JSON actuelle — `GET /metrics/daily`

```json
{
  "generated_at": "<ISO timestamp UTC>",
  "total_runs": 14,
  "pass_count": 14,
  "fail_count": 0,
  "win_count": 14,
  "loss_count": 0,
  "breakeven_count": 0,
  "pnl_cumulative": 6132.42,
  "win_rate": 1.0,
  "last_run": {
    "run_id": "20260517_001",
    "started_at": "2026-05-17T04:03:47",
    "all_ok": true,
    "outcome": "win",
    "net_pnl": 438.03,
    "validation_verdict": "APPROVED",
    "signal": "BUY BTCUSDT"
  },
  "sheets_sync": {
    "dry_run": 6,
    "written": 1,
    "blocked": 2,
    "failed": 0
  }
}
```

---

## Source des données — `_build_metrics()`

| Champ JSON | Source dans le code | Transformation |
| --- | --- | --- |
| `generated_at` | `datetime.now(timezone.utc).isoformat()` | timestamp au moment de la requête |
| `total_runs` | `len(all_entries)` | count des fichiers JSON dans `JOURNAL_DIR` |
| `pass_count` | `sum(1 for e if e.get("all_ok"))` | filtre `all_ok = True` |
| `fail_count` | `total - pass_count` | dérivé |
| `win_count` | `sum(1 for e if outcome == "win")` | filtre `pnl_paper.outcome` |
| `loss_count` | filtre `outcome == "loss"` | filtre `pnl_paper.outcome` |
| `breakeven_count` | filtre `outcome == "breakeven"` | filtre `pnl_paper.outcome` |
| `pnl_cumulative` | `round(sum(pnl_values), 4)` | somme `pnl_paper.net_pnl` |
| `win_rate` | `win_count / total` | ratio |
| `last_run` | `all_entries[0]` | premier fichier (tri décroissant) |
| `sheets_sync` | lecture `SYNC_LOG` ligne par ligne | comptage statuts |

---

## Ce que le dashboard HTML (`/metrics`) affiche

Basé sur `_metrics_html(m, tmux)` — rendu HTML de `_build_metrics()`.

| Élément UI | Champ source |
| --- | --- |
| Nombre de runs | `total_runs` |
| Pass count | `pass_count` |
| P&L cumulé (coloré) | `pnl_cumulative` |
| Dernier run (run_id, statut, P&L, signal) | `last_run.*` |
| Sheets sync (dry/written/blocked) | `sheets_sync.*` |

---

## Champs absents de l'exposition actuelle

Ces champs sont dans `ObservationSummary` V1 (PR #524) mais **absents** de `_build_metrics()`.

| Champ manquant | Calculable depuis | Complexité |
| --- | --- | --- |
| `observation_start` | `min(run_id[:8])` des fichiers journal | simple |
| `days_elapsed` | `(today - observation_start).days` | simple |
| `runs_to_threshold` | `max(0, 30 - total_runs)` | trivial |
| `days_to_threshold` | `max(0, 14 - days_elapsed)` | simple |
| `eligible` | `total_runs >= 30 AND fail_count == 0 AND days_elapsed >= 14` | trivial |
| `closeout_required_count` | `sum(1 for e if e.get("closeout_required"))` | simple |
| `last_run.session_id` | `e.get("session_id")` | trivial |
| `last_run.closeout_required` | `e.get("closeout_required")` | trivial |
| `last_run.localcms_ok` | `e.get("localcms_ok")` | trivial |

Tous ces champs sont calculables sans données externes ni appel réseau.

## RISKS

- À qualifier.
