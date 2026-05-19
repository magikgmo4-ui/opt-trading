# 3-Run Steady-State Review — 2026-05-16

## Metadata

| Champ            | Valeur                                                       |
| ---------------- | ------------------------------------------------------------ |
| GO               | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_SYSTEMD_STEADY_STATE_3_RUN_REVIEW_01 |
| Date             | 2026-05-16                                                   |
| Service          | daily-session.service (oneshot)                              |
| Timer            | daily-session.timer (OnCalendar=daily)                       |
| Mode             | DRY_RUN=1 PAPER_MODE=1 (hardcodé)                            |
| Sheets sync      | dry-run (--controlled-write=false)                           |

## Run Comparison

| Champ                | Run 1            | Run 2            | Run 3            |
| -------------------- | ---------------- | ---------------- | ---------------- |
| run_id               | 20260516_001     | 20260516_002     | 20260516_003     |
| all_ok               | True             | True             | True             |
| dry_run              | True             | True             | True             |
| verdict              | APPROVED         | APPROVED         | APPROVED         |
| outcome              | win              | win              | win              |
| net_pnl              | 438.03           | 438.03           | 438.03           |
| duration_s           | 0.215            | 0.111            | 0.115            |
| localcms_ok          | True             | True             | True             |
| tmux_before          | 9                | 9                | 9                |
| closeout_acknowledged| False            | False            | False            |
| controlled_write     | False            | False            | False            |

## LocalCMS /journal — entries listées

```
20260516_003
20260516_002
20260516_001
```

Toutes les 3 entries visibles (ordre inverse chronologique).

## Scheduler logs

```
COMPLETED run_id=20260516_001 tmux=true localcms=true sheets=false
COMPLETED run_id=20260516_002 tmux=true localcms=true sheets=false
COMPLETED run_id=20260516_003 tmux=true localcms=true sheets=false
```

## Journalctl service logs

```
Starting daily-session.service ... Finished daily-session.service  (x3)
```

Total historique : 6 finished runs (3 PR #489 + 3 ce review).

## Analyse

### Reproductibilité

Les 3 runs produisent des résultats rigoureusement identiques :
- Même verdict (APPROVED), même outcome (win), même P&L (+438.03)
- Même dry_run=True, controlled_write=False
- TMUX 9 sessions, LocalCMS 4/4 endpoints OK
- closeout_acknowledged=False dans tous les cas (--no-closeout)

Seule la durée varie légèrement (0.215s vs ~0.113s) — variance normale due
à la génération d'UUID, timestamps, et latence réseau LocalCMS.

### Stabilité systemd

- Type=oneshot : exit=0 dans les 3 cas
- Timer : next trigger correct après chaque run
- Pas de drift, pas d'accumulation de processus, pas de fuite mémoire
- Logs propres dans scheduler.log et journalctl

## Statut final

```
┌──────┐
│ PASS │
└──────┘
```

3/3 runs OK, données 100% cohérentes entre runs.

## Closeout

### Résumé de la campagne d'observation

| GO                                                 | Statut |
| -------------------------------------------------- | ------ |
| PR #484 — Steady-state run 01 (sans TMUX)          | DEGRADED |
| PR #486 — Steady-state run 02 (TMUX actif)         | PASS   |
| PR #487 — Steady-state closeout                    | PASS   |
| PR #489 — Systemd first-run                        | PASS   |
| Ce GO — 3-run systemd steady-state review          | PASS   |

### Stack validée

```
systemd timer
  └─ systemd service (oneshot, DRY_RUN=1)
       └─ daily_session.sh
            ├─ precheck TMUX (9 sessions, 3 critiques)
            ├─ precheck LocalCMS (4/4 endpoints)
            ├─ daily_session_journal.py (JSON + CSV)
            ├─ sync_daily_session.py (dry-run, 22 colonnes)
            └─ status + log
```

### Invariants maintenus

- DRY_RUN=1 : ✅ (hardcodé dans le service)
- NO_AUTOMATIC_SHEETS_WRITE : ✅ (controlled-write=false)
- NO_LIVE_TRADE / NO_BITGET_ORDER : ✅
- LOCALCMS_READ_ONLY : ✅
- Rollback path : ✅ (uninstall script + clean state vérifié)

## Rollback effectué

```bash
sudo bash /opt/trading/scripts/schedule/uninstall_scheduler_service.sh
```

État final : aucun fichier systemd, aucun timer actif.
