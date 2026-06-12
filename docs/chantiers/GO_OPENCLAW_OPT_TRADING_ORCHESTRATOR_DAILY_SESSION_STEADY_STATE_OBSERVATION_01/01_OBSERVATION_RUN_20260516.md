# Observation Run — 2026-05-16

## Metadata

| Champ            | Valeur                                                       |
| ---------------- | ------------------------------------------------------------ |
| GO               | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_STEADY_STATE_OBSERVATION_01 |
| Date             | 2026-05-16                                                   |
| Run ID           | 20260516_001                                                 |
| Mode             | DRY_RUN=1 PAPER_MODE=1                                       |
| Sheets sync      | dry-run (--controlled-write=false)                           |
| LocalCMS         | http://127.0.0.1:8700                                        |

## Exécution

### 1. Precheck TMUX

```
[2026-05-16 13:04:21 UTC] [WARN] TMUX is installed but no sessions running
```

TMUX installed (`tmux` found in PATH) but no active sessions. Expected in this
environment — no production TMUX sessions are running.

Statut: `false` (non-blocking WARN)

### 2. Precheck LocalCMS

```
[2026-05-16 13:04:21 UTC] [OK] LocalCMS /health returned 200
```

LocalCMS was started on port 8700 before the run. Health endpoint returns `{"ok":true,"module":"localcms","version":"1.0.0"}`.

Statut: `true`

### 3. Génération journal quotidien

| Champ              | Valeur                          |
| ------------------ | ------------------------------- |
| run_id             | 20260516_001                    |
| journal_type       | daily_session                   |
| all_ok             | True                            |
| dry_run            | True                            |
| paper_mode         | True                            |
| pipeline_duration_s| 0.088                           |
| duration_s         | 0.112                           |
| signal             | BUY BTCUSDT                     |
| verdict            | APPROVED                        |
| outcome            | win                             |
| net_pnl            | 438.03                          |
| closeout           | False                           |

Fichiers générés:
- `data/journal/daily/20260516_001.json`
- `data/journal/daily/20260516_001.csv`

### 4. Pipeline E2E dry-run (7 steps)

| Step                   | Status   |
| ---------------------- | -------- |
| 1_signal_router        | dry_run  |
| 2_proposition_engine   | BUY @ 0.82 |
| 3_validation_gate      | APPROVED |
| 4_trade_executor       | dry_run @ 65000.0 |
| 5_result_tracker       | win / +438.03 |
| 6_datasheet_writer     | dry_run (skipped) |
| 7_learning_feeder      | dry_run (brick not stored) |

### 5. LocalCMS journal endpoints

- `GET /journal` → HTML avec liste entries (200 OK)
- `GET /journal/20260516_001` → HTML détail (200 OK)
- `GET /journal/json` → JSON liste (200 OK)

LocalCMS endpoint verification during journal run (4/4):

| Endpoint          | Status | Détail                              |
| ----------------- | ------ | ----------------------------------- |
| /health           | 200    | `{"ok":true,"module":"localcms"}`   |
| /menu             | 200    | 14 domains                          |
| /menu/state       | 200    | 0 state entries                     |
| /runtime/tmux     | 200    | 9 expected, 0 up (expected)         |

### 6. Google Sheets sync (dry-run)

```
⚠ DRY-RUN — no write to Google Sheets.
  Use --controlled-write to actually sync.
```

Row preview confirms all 22 columns mapped correctly. No write performed.

### 7. Scheduler log

Fichier: `data/logs/scheduler/scheduler.log`

```
[2026-05-16 13:04:22 UTC] [scheduler] [COMPLETED] run_id=20260516_001 tmux=false localcms=true sheets=false
```

## Statut final

```
┌──────────┐
│ DEGRADED │
└──────────┘
```

| Critère         | Résultat |
| --------------- | -------- |
| Scheduler run   | ✅       |
| Journal produit | ✅       |
| LocalCMS up     | ✅       |
| Sheets sync dry | ✅       |
| TMUX            | ❌       |

**DEGRADED** car TMUX n'est pas disponible dans cet environnement (pas de
sessions TMUX actives). Il s'agit d'une limitation de l'environnement
d'observation, pas d'un défaut du scheduler ou de la stack d'observabilité.

## Notes

1. **Env vs prod gap**: TMUX sessions ne sont pas disponibles dans ce contexte
   CI-like. En production, le precheck TMUX est un WARN non-bloquant, ce qui
   est le comportement attendu.

2. **LocalCMS port**: Le scheduler et le journal pointent vers `127.0.0.1:8700`.
   LocalCMS doit être démarré sur ce port pour que le precheck et les endpoints
   journal fonctionnent.

3. **Exit code 1**: `daily_session_journal.py --no-closeout` retourne exit=1
   (closeout en attente). Le scheduler accepte ce code comme OK.

4. **Controlled-write**: Sheets sync est en dry-run. Aucune écriture Sheets
   automatique — conforme aux contraintes.

5. **Aucune régression**: Aucune modification de code n'a été nécessaire.
   La stack tourne comme livrée par les PR #472, #475, #478, #480, #483.

## Artefacts

- `data/journal/daily/20260516_001.json` — journal JSON complet
- `data/journal/daily/20260516_001.csv` — résumé CSV
- `data/logs/scheduler/scheduler.log` — log scheduler
- `data/journal/sync_log.jsonl` — log sync Sheets (dry-run entry)

## RISKS

- À qualifier.
