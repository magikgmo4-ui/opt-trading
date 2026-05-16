# Systemd First-Run Observation — 2026-05-16

## Metadata

| Champ            | Valeur                                                       |
| ---------------- | ------------------------------------------------------------ |
| GO               | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_SYSTEMD_FIRST_RUN_OBSERVATION_01 |
| Date             | 2026-05-16                                                   |
| Run ID           | 20260516_001                                                 |
| Service          | daily-session.service (oneshot)                              |
| Timer            | daily-session.timer (OnCalendar=daily)                       |
| Mode             | DRY_RUN=1 PAPER_MODE=1 (hardcodé)                            |
| Sheets sync      | dry-run (--controlled-write=false)                           |

## Installation

```
sudo bash scripts/schedule/install_scheduler_service.sh
```

Résultat :
- Service : `/etc/systemd/system/daily-session.service`
- Timer : `/etc/systemd/system/daily-session.timer`
- Timer enabled + started
- Prochain trigger : Sun 2026-05-17 00:01:26 EDT

## Exécution manuelle (start)

```
sudo systemctl start daily-session.service
```

### Precheck TMUX
```
[OK] TMUX is running
```
9 sessions actives.

### Precheck LocalCMS
```
[OK] LocalCMS /health returned 200
```

### Journal quotidien
```
run_id: 20260516_001
all_ok: True
dry_run: True
verdict: APPROVED
outcome: win
pnl: 438.03
localcms_ok: True
tmux_before: 9
```

### LocalCMS
- `/journal` → HTML list OK
- `/journal/20260516_001` → HTML detail OK

### Google Sheets sync
```
[STEP] sync Google Sheets
[INFO] controlled-write Sheets: DISABLED (dry-run only)
```

### Service logs
```
May 16 15:03:49 db-layer systemd[1]: Starting daily-session.service ...
May 16 15:03:50 db-layer systemd[1]: Finished daily-session.service ...
```

### Check status script
```
bash scripts/schedule/check_scheduler_status.sh
```
Affiche timer status, service status, journalctl logs, scheduler log, latest journal.

## Statut final

```
┌──────┐
│ PASS │
└──────┘
```

| Critère           | Résultat |
| ----------------- | -------- |
| Install           | ✅       |
| Enable            | ✅       |
| Start manuel      | ✅       |
| Precheck TMUX     | ✅       |
| Precheck LocalCMS | ✅       |
| Journal           | ✅       |
| LocalCMS view     | ✅       |
| Sheets sync dry   | ✅       |
| Service logs      | ✅       |
| Check status      | ✅       |

## Rollback path confirmé

```
sudo bash scripts/schedule/uninstall_scheduler_service.sh
```

Vérification post-rollback :
- `/etc/systemd/system/daily-session.*` → CLEAN (no files)
- `systemctl list-timers | grep daily-session` → CLEAN (no timer)

## Scripts livrés

| Fichier                                          | Rôle                            |
| ------------------------------------------------ | ------------------------------- |
| `scripts/schedule/daily-session.service`         | Systemd oneshot unit            |
| `scripts/schedule/daily-session.timer`           | Systemd daily timer             |
| `scripts/schedule/install_scheduler_service.sh`  | Install, enable, start          |
| `scripts/schedule/uninstall_scheduler_service.sh`| Stop, disable, remove files     |
| `scripts/schedule/check_scheduler_status.sh`     | Status, logs, last journal      |

## Contraintes respectées

- DRY_RUN=1 hardcodé dans le service ✅
- No live trade / No Bitget order ✅
- No automatic Sheets write ✅
- LocalCMS read-only ✅
- Rollback obligatoire effectué ✅
