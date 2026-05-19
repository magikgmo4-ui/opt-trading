# OT-LIVE-01 — MACHINE DRILL (SYSTEMD / WRAPPERS) — ADMIN-TRADING

Date (America/Montreal) : 2026-03-12

## 1. MACHINE INSPECTÉE
- **Cible** : `admin-trading`
- **Accès** : SSH (BatchMode=yes) depuis poste Windows
- **Preuve d’identité machine** (extrait) :
  - Debian GNU/Linux 12 (bookworm)
  - Kernel: Linux 6.1.0-42-amd64
  - User: `ghost`

## 2. MÉTHODE (LECTURE UNIQUEMENT)
- Aucune installation / enable / restart / daemon-reload.
- Collecte de preuves : `hostnamectl`, `systemctl list-unit-files`, `systemctl status`, `systemctl cat`, `systemctl --failed`, `command -v`, `readlink -f`.

## 3. COMMANDES EXÉCUTÉES (AVEC PREUVES)

### 3.1 Identification machine
```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "hostnamectl || hostname; whoami; uname -a"
```
Sortie (extrait) :
```text
Static hostname: admin-trading
Operating System: Debian GNU/Linux 12 (bookworm)
Kernel: Linux 6.1.0-42-amd64
ghost
Linux admin-trading 6.1.0-42-amd64 ...
```

### 3.2 Inventaire systemd (présence des unités ciblées)
```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading \
  "systemctl list-unit-files --type=service --type=timer --type=mount --type=automount --no-pager | egrep -i 'desk_retention|vision_bot|shared-sshfs|sshfs|mnt-shared|desk_snapshot_ingest|snapshot' || true"
```
Sortie :
```text
desk_retention.service                     static          -
vision_bot.service                         enabled         enabled
desk_retention.timer                       enabled         enabled
```

### 3.3 Status + contenu desk_retention (timer/service)
```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "systemctl status desk_retention.timer --no-pager -n 40"
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "systemctl status desk_retention.service --no-pager -n 60"
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "systemctl cat desk_retention.timer --no-pager"
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "systemctl cat desk_retention.service --no-pager"
```
Sorties (extraits) :
```text
desk_retention.timer - Run Desk Retention daily at 03:00
Loaded: loaded (/etc/systemd/system/desk_retention.timer; enabled; preset: enabled)
Active: active (waiting)
Trigger: ... 03:00:00 EDT
```
```text
desk_retention.service - Desk Retention (prune old desk/vision files)
Loaded: loaded (/etc/systemd/system/desk_retention.service; static)
ExecStart=/opt/trading/modules/desk_retention/desk_retention.sh 0
status=0/SUCCESS
```
```ini
# /etc/systemd/system/desk_retention.timer
[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true
```

### 3.4 Status + contenu vision_bot (service)
```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "systemctl status vision_bot.service --no-pager -n 40"
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "systemctl cat vision_bot.service --no-pager"
```
Sorties (extraits) :
```text
vision_bot.service - vision_bot (ShareX inbox -> outbox) watch loop
Loaded: loaded (/etc/systemd/system/vision_bot.service; enabled; preset: enabled)
Active: active (running)
ExecStart=/usr/bin/python3 /opt/trading/modules/vision_bot/app/vision_bot.py watch
```

### 3.5 shared_sshfs_permanent (unit files + mount)
```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "systemctl status shared-sshfs.service --no-pager -n 30 || true"
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "systemctl cat shared-sshfs.service --no-pager || true"
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "systemctl list-unit-files --type=service --type=mount --type=automount --no-pager | egrep -i 'shared|sshfs' || true"
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "findmnt /shared || true"
```
Sorties (extraits) :
```text
Unit shared-sshfs.service could not be found.
No files found for shared-sshfs.service.
```

### 3.6 Wrappers live (présence / résolution)
```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading 'command -v menu-ops_menu_hub sanity-desk_pro_runner cmd-desk_pro_runner cmd-desk_pro_dashboard'
```
Sortie :
```text
/usr/local/bin/menu-ops_menu_hub
/usr/local/bin/sanity-desk_pro_runner
/usr/local/bin/cmd-desk_pro_runner
/usr/local/bin/cmd-desk_pro_dashboard
```

Résolution (extrait) :
```text
/usr/local/bin/menu-ops_menu_hub -> /opt/trading/modules/ops_menu_hub/scripts/menu.sh
```

### 3.7 Tests wrappers non destructifs (usage réel minimal)
```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "cmd-desk_pro_runner status || true"
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "sanity-desk_pro_runner || true"
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "cmd-validated_prompt_factory list-modes || true"
```
Sorties (extraits) :
```json
{"runner_status":"OK","mode":"PAPER", ... }
```
```text
PASS: Runner status check passed.
Sanity Check Passed.
```

### 3.8 Wrappers shared_sshfs_permanent (preuve d’écart symlink)
```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "cmd-shared_sshfs_permanent info || true"
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "sanity-shared_sshfs_permanent || true"
```
Sorties :
```text
name=local
path=/usr/local
```
```text
=== sanity (wrapper) ===
name=local
path=/usr/local
FAIL: scripts missing
```

### 3.9 État systemd global (preuve de “degraded” + unité en échec)
```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 ghost@admin-trading "systemctl --failed --no-pager || true"
```
Sortie :
```text
● jdb-canon-daily.service loaded failed failed JDB daily canon compile+push (student)
```

