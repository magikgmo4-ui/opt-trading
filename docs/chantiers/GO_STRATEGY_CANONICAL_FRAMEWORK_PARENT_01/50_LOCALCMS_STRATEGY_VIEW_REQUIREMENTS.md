---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
child_go: GO_STRATEGY_LOCALCMS_VIEW_REQUIREMENTS_01
doc_type: localcms_strategy_view_requirements
repo: opt-trading
status: open
created_at: 2026-05-17
surface: doc-only
---

# 50_LOCALCMS_STRATEGY_VIEW_REQUIREMENTS

---

## 1_OBJECTIF

Definir les requirements d'une vue strategie LocalCMS, en lecture seule, basee
sur les journaux daily et `ObservationEvent`.

LocalCMS existe deja :

```text
GET /journal/daily
GET /journal/daily/{run_id}
GET /metrics
GET /metrics/daily
```

La vue strategie doit s'ajouter comme consumer, pas comme producteur.

---

## 2_VIEW_MODEL

Vues cibles :

| Vue | Role |
| --- | --- |
| Strategy overview | Liste des strategies observees, status, sample, perf_status. |
| Strategy detail | Timeline des events, specs, gates, evidence, replay links. |
| Strategy gate panel | Promotion/retrait, blockers, next required evidence. |
| Strategy event list | Derniers `ObservationEvent` filtres par `strategy_id`. |
| Strategy compare | Comparaison read-only entre strategies. |

---

## 3_REQUIRED_FIELDS

| Field | Source |
| --- | --- |
| `strategy_id` | `ObservationEvent.strategy.strategy_id` |
| `strategy_version` | `ObservationEvent.strategy.strategy_version` |
| `setup_type` | `ObservationEvent.strategy.setup_type` |
| `lifecycle_status` | `ObservationEvent.strategy.lifecycle_status` ou gate state |
| `symbol` | `ObservationEvent.signal.symbol` |
| `timeframe` | `ObservationEvent.signal.timeframe` |
| `confidence` | `ObservationEvent.signal.confidence` |
| `event_count` | count events by `strategy_id` |
| `pass_count` | count `ObservationEvent.status = PASS` |
| `pnl_cumulative` | sum `pnl_net` |
| `win_rate` | Perf/Event aggregate |
| `perf_status` | Perf Engine output |
| `promotion_blockers` | Gate output |
| `last_run_id` | newest event by run_id |

---

## 4_ENDPOINTS_CANDIDATS

Ces endpoints sont des requirements futurs, non implementes dans ce parent :

```text
GET /strategies
GET /strategies/daily
GET /strategies/{strategy_id}
GET /strategies/{strategy_id}/events
GET /strategies/{strategy_id}/gates
```

Contraintes :

```text
GET only
read-only
no order action
no Google Sheets write
no secret display
no mutation of journal
```

---

## 5_UI_REQUIREMENTS

La vue LocalCMS doit afficher :

- status lifecycle courant;
- sample size et jours observes;
- `perf_status`;
- derniers events;
- evidence sources;
- invalidation;
- blockers de promotion;
- retirement warnings;
- lien vers `/journal/daily/{run_id}`;
- lien vers replay Trading Lab si disponible.

Elle ne doit pas afficher :

- bouton BUY;
- bouton SELL;
- bouton Bitget;
- action live;
- write Sheets automatique.

---

## 6_COMPATIBILITY_WITH_CURRENT_LOCALCMS

Current LocalCMS lit deja :

```text
data/journal/daily/*.json
data/journal/sync_log.jsonl
```

`_build_metrics()` calcule deja :

```text
total_runs
pass_count
fail_count
win_count
loss_count
breakeven_count
pnl_cumulative
win_rate
observation.runs_to_threshold
observation.days_to_threshold
observation.eligible
sheets_sync
```

La vue strategie doit reutiliser cette logique d'agregation, avec group-by
`strategy_id`.

---

## 7_ACCEPTANCE_CRITERIA_FOR_CHILD

Le futur child LocalCMS pourra etre considere pret si :

```text
reads only data/journal/daily
groups by strategy_id
handles missing strategy_id for legacy runs
exposes JSON and HTML read-only
does not mutate journal files
does not send Telegram
does not write Sheets
does not expose secrets
```

## RISKS

- À qualifier.
