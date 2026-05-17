---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_SMOKE_01
doc_type: closeout
repo: opt-trading
status: PASS
created_at: 2026-05-17
verdict: PASS
merge_ref: c62a0c0f
---

# 90_CLOSEOUT

---

## Verdict

```text
PASS — tous les champs attendus présents et corrects.
```

---

## Résultat complet `_build_metrics()` — 2026-05-17T23:21:42Z

```json
{
  "generated_at": "2026-05-17T23:21:42.542887+00:00",
  "total_runs": 14,
  "pass_count": 14,
  "fail_count": 0,
  "win_count": 14,
  "loss_count": 0,
  "breakeven_count": 0,
  "pnl_cumulative": 6132.42,
  "win_rate": 1.0,
  "observation": {
    "observation_start": "2026-05-16",
    "days_elapsed": 1,
    "runs_to_threshold": 16,
    "days_to_threshold": 13,
    "eligible": false,
    "closeout_required_count": 0,
    "threshold_runs": 30,
    "threshold_days": 14
  },
  "last_run": {
    "run_id": "20260517_001",
    "session_id": "ec10dc06-83a6-4c35-b188-a136215f3c52",
    "started_at": "2026-05-17T04:03:47",
    "all_ok": true,
    "outcome": "win",
    "net_pnl": 438.03,
    "validation_verdict": "APPROVED",
    "signal": "BUY BTCUSDT",
    "localcms_ok": false,
    "closeout_required": false
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

## Vérification champ par champ

| Champ | Attendu | Présent | Valeur |
| --- | --- | --- | --- |
| `observation.observation_start` | ISO date | ✓ | `"2026-05-16"` |
| `observation.days_elapsed` | int ≥ 0 | ✓ | `1` |
| `observation.runs_to_threshold` | `30 - 14 = 16` | ✓ | `16` |
| `observation.days_to_threshold` | `14 - 1 = 13` | ✓ | `13` |
| `observation.eligible` | `false` (seuils non atteints) | ✓ | `false` |
| `observation.closeout_required_count` | `0` | ✓ | `0` |
| `observation.threshold_runs` | `30` | ✓ | `30` |
| `observation.threshold_days` | `14` | ✓ | `14` |
| `last_run.session_id` | UUID string | ✓ | `"ec10dc06-..."` |
| `last_run.localcms_ok` | bool | ✓ | `false` |
| `last_run.closeout_required` | bool | ✓ | `false` |
| Champs existants inchangés | — | ✓ | total_runs, pnl_cumulative, win_rate, sheets_sync |

---

## Note sur `localcms_ok: false`

`localcms_ok = false` dans `last_run` signifie que LocalCMS n'était pas accessible
au moment de l'exécution du run `20260517_001`. C'est attendu : le run s'exécute
avant que le service HTTP LocalCMS soit actif. Le field est présent et correctement
lu depuis le journal — le comportement est normal.

---

## Point de reprise

```text
LocalCMS observation view = PASS / validé sur sot/mainline @ c62a0c0f
Phase 1 observation continue.
Prochaine revue : 2026-05-24 (20 runs ou 7 jours).
Point de décision final : ≥2026-05-30.
```

---

## Invariants respectés

- Aucun trade
- Aucun SSH
- Aucun Google Sheets write
- `GO_INDEX.md` non modifié
- `ACTIVE_STREAMS.md` non modifié
