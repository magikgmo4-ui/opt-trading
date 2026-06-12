# Daily Session Observability — Closeout Final Baseline

## Résultat global

```
DAILY_SESSION_OBSERVABILITY_BASELINE = PASS
```

## Séquence complète des PRs

| PR    | GO (suffixe)                                   | Résultat                                |
| ----- | ---------------------------------------------- | --------------------------------------- |
| #483  | DAILY_SESSION_AUTOMATION_SCHEDULER_01          | Scheduler bash créé, dry-run par défaut |
| #484  | STEADY_STATE_OBSERVATION_RUN_01                | Run 01 OK — TMUX 0 session (WARN)       |
| #486  | STEADY_STATE_RUN_02_TMUX_ACTIVE_01             | Run 02 OK — TMUX 9 sessions actives     |
| #487  | STEADY_STATE_CLOSEOUT_01                       | Baseline dry-run figée PASS             |
| #488  | DAILY_SESSION_CRON_SYSTEMD_01                  | Systemd service + timer installés       |
| #489  | DAILY_SESSION_SYSTEMD_FIRST_RUN_OBSERVATION_01 | Premier run systemd OK                  |
| #490  | DAILY_SESSION_SYSTEMD_STEADY_STATE_3_RUN_01    | 3 runs systemd — cohérents, anomalie rate-limit résolue |
| #493  | DAILY_SESSION_7D_DRY_RUN_OBSERVATION_01        | 7/7 runs OK, données 100% cohérentes    |
| #501  | GOOGLE_SHEETS_ADC_AUTH_FALLBACK_01             | ADC = PASS (JSON key bloqué par policy) |
| #504  | GOOGLE_SHEETS_GSPREAD_DEPENDENCY_FIX_01        | gspread==6.2.1 + google-auth==2.53.0    |
| #505  | DAILY_SESSION_GOOGLE_SHEETS_CLOSEOUT_01        | Controlled-write PASS — run_id=20260516_013 |

## État opérationnel courant

| Composant                         | État                        |
| --------------------------------- | --------------------------- |
| Scheduler bash                    | opérationnel                |
| Systemd service (oneshot)         | actif                       |
| Systemd timer (OnCalendar=daily)  | actif, trigger minuit       |
| TMUX precheck                     | 9 sessions, 3 critiques     |
| LocalCMS health                   | 4/4 endpoints OK            |
| Journal JSON/CSV                  | opérationnel                |
| LocalCMS /journal history view    | opérationnel                |
| Google Sheets controlled sync     | opérationnel (ADC + gspread)|

## Preuve d'exécution

### 7-day dry-run (PR #493)

| Jour | run_id        | all_ok | outcome | P&L      | localcms | tmux | sheets |
| ---- | ------------- | ------ | ------- | -------- | -------- | ---- | ------ |
| J1   | 20260516_001  | True   | win     | +438.03  | 4/4      | 9    | dry    |
| J2   | 20260516_002  | True   | win     | +438.03  | 4/4      | 9    | dry    |
| J3   | 20260516_003  | True   | win     | +438.03  | 4/4      | 9    | dry    |
| J4   | 20260516_004  | True   | win     | +438.03  | 4/4      | 9    | dry    |
| J5   | 20260516_005  | True   | win     | +438.03  | 4/4      | 9    | dry    |
| J6   | 20260516_006  | True   | win     | +438.03  | 4/4      | 9    | dry    |
| J7   | 20260516_007  | True   | win     | +438.03  | 4/4      | 9    | dry    |

### Controlled-write réel (PR #505)

```
run_id     = 20260516_013
signal     = BUY BTCUSDT
verdict    = APPROVED
outcome    = win
net_pnl    = +438.03
mode       = controlled_write
status     = synced
row        = appended Google Sheets sheet1
```

## Dépendances figées

```
gspread      = 6.2.1   (requirements.txt)
google-auth  = 2.53.0  (requirements.txt)
```

## Invariants sécurité

| Invariant                         | État |
| --------------------------------- | ---- |
| Aucun secret dans le repo         | PASS |
| Aucun secret dans les logs        | PASS |
| `GOOGLE_SHEETS_SYNC_SHEET_ID` hors repo (env) | PASS |
| Dry-run par défaut                | PASS |
| Controlled-write manuel seulement | PASS |
| No live trade                     | PASS |
| No Bitget order                   | PASS |
| LocalCMS read-only                | PASS |

## Rollback / disable path

```bash
# Désactiver le timer systemd
sudo systemctl disable --now daily-session.timer

# Désactiver le service
sudo systemctl disable daily-session.service

# Vérifier
systemctl status daily-session.timer daily-session.service
```

Le script scheduler et les journaux restent intacts — seule l'exécution
automatique est suspendue.

## Prochaines options

### A — Observation continue (recommandé)
Laisser le timer actif. Accumuler des runs quotidiens en dry-run.
Révision hebdomadaire des journaux via LocalCMS `/journal`.

### B — Multi-signal paper-mode
Étendre le pipeline à plusieurs tickers (ex. ETHUSDT, SOLUSDT) en
parallèle, toujours en paper-mode. Nécessite un GO dédié.

### C — Dashboard métriques LocalCMS
Construire une vue agrégée LocalCMS qui lit `data/journal/daily/*.json`
et affiche métriques clés (P&L cumulé, win-rate, durée moyenne).
Doc-only dans un premier temps.

### D — Préparation live trading (doc-only)
Rédiger le protocole de passage paper → live : critères de déclenchement,
garde-fous, approbations requises. Aucune exécution réelle dans ce GO.

## Recommandation

Option A (observation continue) + Option C (dashboard métriques) en parallèle,
puis Option D pour documenter la voie vers le live. Option B quand la baseline
multi-signal est définie.

## RISKS

- À qualifier.
