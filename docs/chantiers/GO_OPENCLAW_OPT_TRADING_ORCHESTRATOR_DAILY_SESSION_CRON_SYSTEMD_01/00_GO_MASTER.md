---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_CRON_SYSTEMD_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #483  (Daily session automation scheduler — merged)
  - PR #484  (Steady-state observation run 01 — merged)
  - PR #486  (Steady-state observation run 02 TMUX active — merged)
  - PR #487  (Steady-state closeout — merged)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_CRON_SYSTEMD_01

## Objectif

Intégrer l'exécution quotidienne automatique du scheduler daily session
via cron/systemd, en conservant tous les garde-fous dry-run établis.

## Contexte établi

- Scheduler daily session : `scripts/schedule/daily_session.sh`
- Dry-run par défaut (DRY_RUN=1)
- Precheck TMUX (WARN non-bloquant) + LocalCMS (/health)
- Journal JSON/CSV + LocalCMS history view + Google Sheets sync dry-run
- Baseline TMUX 9 sessions, 3 critiques
- Aucune écriture Sheets automatique
- Aucun trade live / Bitget order

## Périmètre

1. Créer le service systemd `daily-session.service`
2. Créer le timer systemd `daily-session.timer` (horaire configurable)
3. Script d'installation `scripts/schedule/install_scheduler_service.sh`
4. Script de désinstallation `scripts/schedule/uninstall_scheduler_service.sh`
5. Script de vérification de statut `scripts/schedule/check_scheduler_status.sh`
6. Logging : redirection des stdout/stderr vers `data/logs/scheduler/`
7. Tests de validation (install, enable, status, disable, uninstall)

## Choix d'architecture

```
systemd timer (daily-session.timer)
  └─ systemd service (daily-session.service)
       └─ scripts/schedule/daily_session.sh (DRY_RUN=1 PAPER_MODE=1)
            ├─ precheck TMUX
            ├─ precheck LocalCMS
            ├─ daily_session_journal.py --no-closeout
            └─ sync_daily_session.py (dry-run)
```

## Détails d'implémentation

### daily-session.service

```ini
[Unit]
Description=OpenClaw Daily Session Scheduler (dry-run)
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=ghost
WorkingDirectory=/opt/trading
Environment=DRY_RUN=1
Environment=PAPER_MODE=1
ExecStart=/opt/trading/scripts/schedule/daily_session.sh
StandardOutput=append:/opt/trading/data/logs/scheduler/systemd-stdout.log
StandardError=append:/opt/trading/data/logs/scheduler/systemd-stderr.log

[Install]
WantedBy=multi-user.target
```

### daily-session.timer

```ini
[Unit]
Description=Daily session scheduler timer (every 24h)

[Timer]
OnCalendar=daily
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
```

### install_scheduler_service.sh

Installe les fichiers `.service` et `.timer` dans `/etc/systemd/system/`,
recharge systemd, enable + start le timer.

### uninstall_scheduler_service.sh

Stop + disable le timer et le service, supprime les fichiers `.service`
et `.timer` de `/etc/systemd/system/`, reload systemd.

### check_scheduler_status.sh

Affiche le statut du timer, du service, le dernier run, les logs.

## Tests

```bash
tests/e2e/test_daily_session_scheduler_service.sh
```

- install → service/timer files exist
- enable → timer is loaded
- status → timer/service active
- dry-run execution via systemd-run
- disable → timer stopped
- uninstall → files removed
- rollback → clean state

## Livrables

- `scripts/schedule/daily-session.service`
- `scripts/schedule/daily-session.timer`
- `scripts/schedule/install_scheduler_service.sh`
- `scripts/schedule/uninstall_scheduler_service.sh`
- `scripts/schedule/check_scheduler_status.sh`
- `tests/e2e/test_daily_session_scheduler_service.sh`

## Rollback / disable path

```bash
# Disable
sudo systemctl disable --now daily-session.timer

# Uninstall
sudo bash scripts/schedule/uninstall_scheduler_service.sh

# Verify clean
sudo systemctl list-timers | grep daily-session  # should be empty
ls /etc/systemd/system/daily-session.*            # should not exist
```

## Contraintes

- `DRY_RUN=1` et `PAPER_MODE=1` codés en dur dans le service
- Controlled-write Sheets : manuel uniquement
- No live trade / No Bitget order
- LocalCMS read-only
- Prechecks TMUX + LocalCMS exécutés avant chaque run
- Chemins absolus dans les fichiers systemd (WorkingDirectory, ExecStart)
- Le timer peut être désactivé immédiatement sans perte de données
