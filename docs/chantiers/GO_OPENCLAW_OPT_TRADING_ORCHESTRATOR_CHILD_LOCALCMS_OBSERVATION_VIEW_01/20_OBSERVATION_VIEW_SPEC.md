---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_01
doc_type: view_spec
repo: opt-trading
status: open
created_at: 2026-05-17
schema_ref: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_OBSERVATION_EVENT_SCHEMA_01/20_CANONICAL_OBSERVATION_EVENT_SCHEMA.md
---

# 20_OBSERVATION_VIEW_SPEC

Spécification de la vue cible LocalCMS pour exposer `ObservationSummary` V1.

---

## Principe

```text
Étendre _build_metrics() pour inclure les champs Phase 1 manquants.
Ne pas créer un endpoint séparé — enrichir l'existant.
Rester compatible avec les consommateurs actuels (le champ last_run reste, les champs existants restent).
```

---

## Réponse JSON cible — `GET /metrics/daily` étendu

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

  "observation": {
    "observation_start": "2026-05-16",
    "days_elapsed": 2,
    "runs_to_threshold": 16,
    "days_to_threshold": 12,
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

## Bloc `observation` — détail des champs

| Champ | Type | Règle | Exemple |
| --- | --- | --- | --- |
| `observation_start` | ISO date string | `min(run_id[:8])` des journaux connus — format `YYYY-MM-DD` | `"2026-05-16"` |
| `days_elapsed` | int | `(date.today() - observation_start).days` | `2` |
| `runs_to_threshold` | int | `max(0, 30 - total_runs)` | `16` |
| `days_to_threshold` | int | `max(0, 14 - days_elapsed)` | `12` |
| `eligible` | bool | `total_runs >= 30 AND fail_count == 0 AND days_elapsed >= 14` | `false` |
| `closeout_required_count` | int | `sum(1 for e if e.get("closeout_required"))` | `0` |
| `threshold_runs` | int | constante `30` | `30` |
| `threshold_days` | int | constante `14` | `14` |

---

## Extensions du bloc `last_run`

| Champ ajouté | Source | Note |
| --- | --- | --- |
| `session_id` | `e.get("session_id", "")` | UUID session OpenClaw |
| `localcms_ok` | `e.get("localcms_ok", None)` | `false` si LocalCMS indisponible au run |
| `closeout_required` | `e.get("closeout_required", False)` | alerte bloquante |

---

## Dashboard HTML `/metrics` — extensions recommandées

Nouveaux éléments UI à ajouter au template `_metrics_html()` :

### Bloc Phase 1 — état seuils

```
┌─────────────────────────────────────────┐
│  Phase 1 Observation                     │
│  Runs    : 14 / 30   [████░░░░░░] 47%   │
│  Jours   :  2 / 14   [██░░░░░░░░] 14%   │
│  Éligible : NON                          │
│  Début   : 2026-05-16                    │
└─────────────────────────────────────────┘
```

### Alerte closeout_required

```
Si closeout_required_count > 0 :
┌─────────────────────────────────────────┐
│  ⚠ CLOSEOUT REQUIS — N run(s) bloquants │
└─────────────────────────────────────────┘
```

---

## Comportement si journal vide

```text
Si JOURNAL_DIR vide ou inexistant :
  observation_start = null
  days_elapsed = 0
  runs_to_threshold = 30
  days_to_threshold = 14
  eligible = false
  closeout_required_count = 0
```

---

## Compatibilité ascendante

```text
Tous les champs existants restent inchangés.
Le bloc "observation" est un objet nouveau — les consommateurs qui ignorent
les champs inconnus ne sont pas impactés.
Les extensions "last_run" sont additives — aucun champ existant retiré.
```
