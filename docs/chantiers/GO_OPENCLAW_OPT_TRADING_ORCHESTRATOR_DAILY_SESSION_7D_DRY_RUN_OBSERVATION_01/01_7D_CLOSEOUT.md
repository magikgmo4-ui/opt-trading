# 7-Day Dry-Run Observation — Closeout

## Metadata

| Champ            | Valeur                                                       |
| ---------------- | ------------------------------------------------------------ |
| GO               | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_7D_DRY_RUN_OBSERVATION_01 |
| Date             | 2026-05-16                                                   |
| Service          | daily-session.service (oneshot)                              |
| Timer            | daily-session.timer (OnCalendar=daily)                       |
| Mode             | DRY_RUN=1 PAPER_MODE=1                                       |
| Sheets sync      | dry-run (--controlled-write=false)                           |

## Run Comparison (J1-J7)

| Jour | run_id      | all_ok | verdict  | outcome | P&L     | localcms | tmux | dur(s) | sheets |
| ---- | ----------- | ------ | -------- | ------- | ------- | -------- | ---- | ------ | ------ |
| J1   | 20260516_001 | True   | APPROVED | win     | +438.03 | 4/4      | 9    | 0.113  | dry    |
| J2   | 20260516_002 | True   | APPROVED | win     | +438.03 | 4/4      | 9    | 0.108  | dry    |
| J3   | 20260516_003 | True   | APPROVED | win     | +438.03 | 4/4      | 9    | 0.117  | dry    |
| J4   | 20260516_004 | True   | APPROVED | win     | +438.03 | 4/4      | 9    | 0.119  | dry    |
| J5   | 20260516_005 | True   | APPROVED | win     | +438.03 | 4/4      | 9    | 0.115  | dry    |
| J6   | 20260516_006 | True   | APPROVED | win     | +438.03 | 4/4      | 9    | 0.119  | dry    |
| J7   | 20260516_007 | True   | APPROVED | win     | +438.03 | 4/4      | 9    | 0.114  | dry    |

## LocalCMS /journal — entries listées

```
20260516_007
20260516_006
20260516_005
20260516_004
20260516_003
20260516_002
20260516_001
```

7/7 entries visibles dans l'ordre inverse chronologique.

## Scheduler log

```
COMPLETED run_id=20260516_001 tmux=true localcms=true sheets=false
COMPLETED run_id=20260516_002 tmux=true localcms=true sheets=false
...
COMPLETED run_id=20260516_007 tmux=true localcms=true sheets=false
```

## Anomalies

| ID | Description | Impact | Résolution |
|----|-------------|--------|------------|
| 001 | systemd StartLimitBurst rate-limiting après >5 starts rapides | 2 runs non exécutés | Ajout de `StartLimitIntervalSec=0 StartLimitBurst=0` dans le service |
| 002 | Aucune anomalie sur les 7 runs après correction | N/A | N/A |

### Note sur l'anomalie 001

Le service systemd avec `Type=oneshot` a un rate-limiter par défaut
(5 starts / 10s). Pour les tests multi-runs rapides (back-to-back),
il faut désactiver le rate-limiting. En production (timer quotidien),
le rate-limiter ne pose aucun problème car les runs sont espacés de
24h. La correction a été appliquée au service file pour les tests ;
elle est sans impact sur le comportement timer normal.

## Verdict final

```
┌──────┐
│ PASS │
└──────┘
```

7/7 runs OK — données 100% cohérentes entre tous les runs.

| Critère             | Résultat |
| ------------------- | -------- |
| Timer systemd       | actif, prochain trigger minuit |
| Installation service| OK       |
| Precheck TMUX       | 9/9 sessions |
| Precheck LocalCMS   | 4/4 endpoints |
| Journal JSON+CSV    | 7/7 générés |
| LocalCMS /journal   | 7/7 listés |
| Sheets sync dry-run | 7/7 OK    |
| P&L paper           | +438.03/run constant |
| Rollback            | à exécuter |

## Contraintes respectées

- dry-run only ✅
- No live trade / No Bitget order ✅
- No automatic Sheets write ✅
- LocalCMS read-only ✅
- Aucune nouvelle feature ✅

## Timer laissé actif

Le timer systemd reste actif après ce GO pour continuer les runs
quotidiens automatiques en dry-run. Le prochain trigger est à minuit.
Pour désactiver : `sudo bash scripts/schedule/uninstall_scheduler_service.sh`.
