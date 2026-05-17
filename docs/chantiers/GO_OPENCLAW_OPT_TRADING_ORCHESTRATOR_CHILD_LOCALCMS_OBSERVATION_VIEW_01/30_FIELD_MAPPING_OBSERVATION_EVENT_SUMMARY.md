---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_01
doc_type: field_mapping
repo: opt-trading
status: open
created_at: 2026-05-17
---

# 30_FIELD_MAPPING_OBSERVATION_EVENT_SUMMARY

Mapping précis champ par champ — de la source journal vers la sortie JSON étendue.

Référence : `_build_metrics()` dans `modules/localcms/app/main.py`.

---

## Champs existants — pas de changement

| Champ JSON | Calcul actuel | Statut |
| --- | --- | --- |
| `generated_at` | `datetime.now(timezone.utc).isoformat()` | inchangé |
| `total_runs` | `len(all_entries)` | inchangé |
| `pass_count` | `sum(1 for e if all_ok)` | inchangé |
| `fail_count` | `total - pass_count` | inchangé |
| `win_count` | `sum(1 for e if outcome == "win")` | inchangé |
| `loss_count` | `sum(1 for e if outcome == "loss")` | inchangé |
| `breakeven_count` | `sum(1 for e if outcome == "breakeven")` | inchangé |
| `pnl_cumulative` | `round(sum(pnl_values), 4)` | inchangé |
| `win_rate` | `win_count / total` | inchangé |
| `last_run.run_id` | `e.get("run_id", "")` | inchangé |
| `last_run.started_at` | `e.get("started_at", "")[:19]` | inchangé |
| `last_run.all_ok` | `e.get("all_ok", False)` | inchangé |
| `last_run.outcome` | `e.get("pnl_paper", {}).get("outcome", "")` | inchangé |
| `last_run.net_pnl` | `e.get("pnl_paper", {}).get("net_pnl", 0)` | inchangé |
| `last_run.validation_verdict` | `e.get("validation_verdict", "")` | inchangé |
| `last_run.signal` | signal_source concaténé | inchangé |
| `sheets_sync.*` | lecture `SYNC_LOG` | inchangé |

---

## Bloc `observation` — nouveaux calculs

### `observation_start`

```python
# Trouver la date du plus ancien run_id connu
run_ids = [e.get("run_id", "") for e in all_entries if e.get("run_id")]
if run_ids:
    oldest = min(run_ids)            # ex: "20260516_012"
    observation_start = date(
        int(oldest[:4]),
        int(oldest[4:6]),
        int(oldest[6:8])
    )
else:
    observation_start = None
```

### `days_elapsed`

```python
if observation_start:
    days_elapsed = (date.today() - observation_start).days
else:
    days_elapsed = 0
```

### `runs_to_threshold`

```python
THRESHOLD_RUNS = 30
runs_to_threshold = max(0, THRESHOLD_RUNS - total)
```

### `days_to_threshold`

```python
THRESHOLD_DAYS = 14
days_to_threshold = max(0, THRESHOLD_DAYS - days_elapsed)
```

### `eligible`

```python
eligible = (
    total >= THRESHOLD_RUNS
    and fail_count == 0
    and days_elapsed >= THRESHOLD_DAYS
)
```

### `closeout_required_count`

```python
closeout_required_count = sum(
    1 for e in all_entries if e.get("closeout_required", False)
)
```

---

## Extensions `last_run`

```python
if all_entries:
    e = all_entries[0]
    last_run = {
        # champs existants
        "run_id": e.get("run_id", ""),
        "started_at": (e.get("started_at", "") or "")[:19],
        "all_ok": e.get("all_ok", False),
        "outcome": e.get("pnl_paper", {}).get("outcome", ""),
        "net_pnl": e.get("pnl_paper", {}).get("net_pnl", 0),
        "validation_verdict": e.get("validation_verdict", ""),
        "signal": ...,
        # champs ajoutés
        "session_id": e.get("session_id", ""),
        "localcms_ok": e.get("localcms_ok"),
        "closeout_required": e.get("closeout_required", False),
    }
```

---

## Retour `observation` dans `_build_metrics()`

```python
"observation": {
    "observation_start": observation_start.isoformat() if observation_start else None,
    "days_elapsed": days_elapsed,
    "runs_to_threshold": runs_to_threshold,
    "days_to_threshold": days_to_threshold,
    "eligible": eligible,
    "closeout_required_count": closeout_required_count,
    "threshold_runs": THRESHOLD_RUNS,
    "threshold_days": THRESHOLD_DAYS,
},
```

---

## Résumé des constantes Phase 1

| Constante | Valeur | Source |
| --- | --- | --- |
| `THRESHOLD_RUNS` | `30` | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PHASE1_30_RUN_14_DAY_OBSERVATION_01/00_GO_MASTER.md` |
| `THRESHOLD_DAYS` | `14` | idem |
| `OBSERVATION_START` | calculé dynamiquement depuis `min(run_id[:8])` | journaux réels |
