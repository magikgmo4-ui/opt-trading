---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_OBSERVATION_EVENT_SCHEMA_01
doc_type: canonical_schema
repo: opt-trading
status: open
created_at: 2026-05-17
schema_version: V1
---

# 20_CANONICAL_OBSERVATION_EVENT_SCHEMA

Schéma canonique V1 des événements d'observation OpenClaw dry-run.

Dérivé de l'inventaire `10_SIGNAL_INVENTORY.md` et des journaux réels `data/journal/daily/*.json`.

---

## Principe

```text
Un ObservationEvent représente un run OpenClaw dry-run tel qu'il peut être
structuré, persisté et exposé à un consommateur (LocalCMS, dashboard, BDD future).

Il n'est pas une copie du journal brut. C'est une vue normalisée, minimaliste,
opérable par un consommateur sans dépendance aux détails de pipeline.
```

---

## Entité principale : `ObservationEvent`

| Champ | Type | Contrainte | Source | Description |
| --- | --- | --- | --- | --- |
| `run_id` | string | NOT NULL, UNIQUE | `journal.run_id` | Clé primaire — format `YYYYMMDD_NNN` |
| `session_id` | UUID string | NOT NULL | `journal.session_id` | Identifiant session OpenClaw |
| `run_date` | ISO date | NOT NULL | extrait de `run_id` | Date du run — `YYYYMMDD` |
| `started_at` | ISO timestamp UTC | NOT NULL | `journal.started_at` | Début du run |
| `completed_at` | ISO timestamp UTC | NULLABLE | `journal.completed_at` | Fin du run |
| `duration_s` | float | NULLABLE | `journal.duration_s` | Durée totale du run |
| `status` | enum | NOT NULL | dérivé de `all_ok` | `PASS` / `FAIL` |
| `dry_run` | bool | NOT NULL | `journal.dry_run` | Mode dry-run actif |
| `paper_mode` | bool | NOT NULL | `journal.paper_mode` | Mode paper actif |
| `validation_verdict` | string | NULLABLE | `journal.validation_verdict` | `APPROVED` / `REJECTED` / null |
| `trade_executor_status` | string | NULLABLE | `journal.trade_executor_status` | `dry_run` / `paper` / `live` |
| `outcome` | string | NULLABLE | `journal.result_tracker_outcome` | `win` / `loss` / `breakeven` |
| `pnl_net` | float | NULLABLE | `journal.pnl_paper.net_pnl` | P&L net du run (paper) |
| `localcms_ok` | bool | NULLABLE | `journal.localcms_ok` | LocalCMS mis à jour avec succès |
| `closeout_required` | bool | NOT NULL | `journal.closeout_required` | Anomalie bloquante requérant closeout |
| `closeout_acknowledged` | bool | NOT NULL | `journal.closeout_acknowledged` | Closeout acquitté |
| `ingested_at` | ISO timestamp UTC | NOT NULL | ajouté à l'ingestion | Timestamp d'ingestion (non présent dans journal brut) |
| `source_file` | string | NOT NULL | nom du fichier journal | `data/journal/daily/20260517_001.json` |

---

## Règles de mapping

```text
run_id           = journal.run_id                         (PK, UNIQUE)
session_id       = journal.session_id
run_date         = run_id[:8]                             (YYYYMMDD)
started_at       = journal.started_at
completed_at     = journal.completed_at
duration_s       = journal.duration_s
status           = "PASS" if journal.all_ok else "FAIL"
dry_run          = journal.dry_run
paper_mode       = journal.paper_mode
validation_verdict = journal.validation_verdict
trade_executor_status = journal.trade_executor_status
outcome          = journal.result_tracker_outcome
pnl_net          = journal.pnl_paper.net_pnl              (si présent)
localcms_ok      = journal.localcms_ok
closeout_required = journal.closeout_required
closeout_acknowledged = journal.closeout_acknowledged
ingested_at      = now() UTC                              (ajouté à l'ingestion)
source_file      = chemin relatif du fichier journal
```

---

## Invariants

### Idempotence
```text
Un run_id déjà ingéré ne crée pas de doublon.
Si run_id existe : skip ou update selon stratégie retenue.
```

### Mode guard obligatoire
```text
En Phase 1 : dry_run = true ET paper_mode = true sont des invariants.
Si dry_run = false OU paper_mode = false : anomalie à signaler.
```

### Closeout
```text
Si closeout_required = true ET closeout_acknowledged = false :
→ le run doit déclencher une alerte opérateur.
```

---

## Entité agrégée : `ObservationSummary`

Vue agrégée de l'observation pour le dashboard / LocalCMS.

| Champ | Type | Dérivé de | Description |
| --- | --- | --- | --- |
| `total_runs` | int | count(ObservationEvent) | Nombre total de runs observés |
| `pass_count` | int | count(status=PASS) | Runs PASS |
| `fail_count` | int | count(status=FAIL) | Runs FAIL |
| `win_count` | int | count(outcome=win) | Runs win |
| `loss_count` | int | count(outcome=loss) | Runs loss |
| `breakeven_count` | int | count(outcome=breakeven) | Runs breakeven |
| `pnl_cumulative` | float | sum(pnl_net) | P&L cumulé |
| `win_rate` | float | win_count / total_runs | Taux de win |
| `last_run_id` | string | max(run_id) | Dernier run_id connu |
| `last_run_date` | ISO date | max(run_date) | Date du dernier run |
| `observation_start` | ISO date | min(run_date) | Début de l'observation |
| `days_elapsed` | int | (today - observation_start).days | Jours écoulés |
| `runs_to_threshold` | int | max(0, 30 - total_runs) | Gap au seuil 30 runs |
| `days_to_threshold` | int | max(0, 14 - days_elapsed) | Gap au seuil 14 jours |
| `eligible` | bool | total_runs >= 30 AND fail_count == 0 AND days_elapsed >= 14 | Éligibilité multi-signal |

---

## Ce que ce schéma n'inclut pas

```text
- Le détail des steps (trop granulaire — consulter le journal brut)
- L'état tmux (monitoring local)
- Les engines_context internes (niveau step)
- Le schéma physique BDD (moteur non figé — cf. DB_LAYER_INGESTION_PHYSICAL_SCHEMA_DECISION_01.md)
- Les artefacts Desk Pro (chemin distinct — cf. DB_LAYER_INGESTION_SCHEMA_MAPPING_01.md)
```

---

## Compatibilité future

```text
Ce schéma V1 doit tolérer :
- l'ajout de nouveaux champs (ex : signal_ticker, strategy_id)
- l'ajout de nouvelles entités (ex : StepEvent si le besoin step-level émerge)
- l'ajout d'un champ sheets_status si le sync Sheets devient traçable par run
- une migration vers une BDD sans changer le contrat logique
```
