---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_IMPL_01_INSTALL_RUNBOOK
doc_type: installation_runbook_draft
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_IMPL_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 40_INSTALLATION_RUNBOOK_DRAFT - Installation Runbook (Draft)

## Avertissement

Ce runbook decrit l'installation future. **NE PAS EXECUTER** dans ce GO.

## Installation steps futures

### 1. Prepare environment

```bash
sudo useradd -r -s /bin/false ghost || true
sudo mkdir -p /opt/trading
```

### 2. Copy systemd files

```bash
sudo cp modules/desk_pro/systemd/desk_pro_dry_run.timer /etc/systemd/system/
sudo cp modules/desk_pro/systemd/desk_pro_dry_run.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/desk_pro_dry_run.timer
sudo chmod 644 /etc/systemd/system/desk_pro_dry_run.service
```

### 3. Reload systemd

```bash
sudo systemctl daemon-reload
```

### 4. Verify

```bash
sudo systemd-analyze verify /etc/systemd/system/desk_pro_dry_run.timer
sudo systemd-analyze verify /etc/systemd/system/desk_pro_dry_run.service
```

### 5. Enable timer

```bash
sudo systemctl enable desk_pro_dry_run.timer
```

### 6. Start timer

```bash
sudo systemctl start desk_pro_dry_run.timer
```

### 7. Check status

```bash
sudo systemctl status desk_pro_dry_run.timer
sudo systemctl status desk_pro_dry_run.service
```

## Rollback steps

```bash
sudo systemctl stop desk_pro_dry_run.timer
sudo systemctl disable desk_pro_dry_run.timer
sudo rm /etc/systemd/system/desk_pro_dry_run.timer
sudo rm /etc/systemd/system/desk_pro_dry_run.service
sudo systemctl daemon-reload
```

## Preconditions

- User `ghost` existe
- Fichiers de config verifies
- Tests passent

## Next GO

`GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_INSTALL_GATED_01`