# DB Layer Failover Runbook

## 1. Objectif
Ce runbook decrit le mode degrade quand `db-layer` est indisponible.

Le plan retenu est :
- `admin-trading` = source of truth runtime
- `fantome` = hub ops temporaire et secours artefacts
- `student` = lab Ollama hors chemin critique
- `db-layer` = retire du chemin operationnel jusqu'au retour reseau/SSH

## 2. Ce qui reste nominal
- `tv-webhook.service` sur `admin-trading`
- `tv-perf.service` sur `admin-trading`
- `bot_vision_step2.service` sur `admin-trading`
- `localcms.service` sur `fantome`
- `openclaw-gateway.service` sur `fantome`
- `shared-sshfs.service` sur `fantome`

## 3. Ce qui n'est plus nominal
- aucun acces SSH valide a `db-layer`
- aucune preuve runtime sur `shared-sshfs.service` cote `db-layer`
- aucune preuve runtime sur `algo-hf-api.service` cote `db-layer`
- aucune orchestration devant dependre de `db-layer`

## 4. Preflight depuis `cursor-ai`

```powershell
ssh admin-trading "hostname"
ssh fantome "hostname"
ssh student "hostname"
ssh admin-trading "systemctl is-active tv-webhook.service tv-perf.service bot_vision_step2.service"
ssh fantome "systemctl is-active shared-sshfs.service localcms.service openclaw-gateway.service"
ssh student "systemctl is-active ollama.service"
```

Attendu :
- `admin-trading`, `fantome`, `student` repondent
- services `active` sur `admin-trading` et `fantome`
- `ollama.service` peut rester uniquement un lab, sans impact prod

## 5. Bascule operationnelle

### Etape 1 - Declarer le mode degrade
Usage humain immediat :
- ne plus utiliser `db-layer` comme point d'entree SSH
- lancer les operations trading/Desk sur `admin-trading`
- lancer les operations cockpit/OpenClaw sur `fantome`

### Etape 2 - Revalider les surfaces critiques sur `admin-trading`

```bash
ssh admin-trading "bash -lc 'hostname; systemctl is-active tv-webhook.service tv-perf.service bot_vision_step2.service; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:8000/docs; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:8010/perf/ui; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:8010/desk/ui; ls -lh /opt/trading/state/events.jsonl /opt/trading/perf/perf.db'"
```

Attendu :
- les 3 services sont `active`
- les 3 URLs repondent `200`
- `events.jsonl` et `perf.db` existent et ont une date recente

### Etape 3 - Rafraichir l'export Desk Pro sur `admin-trading`

```bash
ssh admin-trading 'cd /opt/trading && scripts/admin_trading/desk_pro_cmd.sh last-run-info'
ssh admin-trading 'cd /opt/trading && scripts/admin_trading/desk_pro_cmd.sh export-html-latest'
ssh admin-trading 'cd /opt/trading && scripts/admin_trading/desk_pro_cmd.sh copy-latest-to-shared'
ssh admin-trading 'bash -lc "ls -lh /srv/sftp/shared_files/shared/desk_pro/latest"'
```

But :
- remettre a jour `/srv/sftp/shared_files/shared/desk_pro/latest`
- ne pas dependre de l'ancien export vu au `4 avr`

### Etape 4 - Revalider `fantome` comme hub ops

```bash
ssh fantome "bash -lc 'hostname; systemctl is-active shared-sshfs.service localcms.service openclaw-gateway.service; systemctl is-active opt-trading-runtime-health.timer opt-trading-fleet-orchestrator.timer; curl -s http://127.0.0.1:8700/health; sudo -n -u openclaw openclaw gateway probe --timeout 30000; mount | grep \" on /shared \"; ls -lh /shared/desk_pro/latest /shared/vision_outbox | tail -n +1'"
```

Attendu :
- services et timers `active`
- LocalCMS renvoie `{"ok":true,...}`
- gateway probe `Reachable: yes`
- `/shared` est monte depuis `admin-trading`

### Etape 5 - Creer une copie de secours locale sur `fantome`
Commande a lancer sur `fantome` :

```bash
ssh fantome "bash -lc 'mkdir -p /opt/trading/data/failover/admin-trading/state; mkdir -p /opt/trading/data/failover/admin-trading/perf; mkdir -p /opt/trading/data/failover/admin-trading/shared_snapshots/desk_pro_latest; mkdir -p /opt/trading/data/failover/admin-trading/shared_snapshots/vision_outbox; rsync -av admin-trading:/opt/trading/state/events.jsonl /opt/trading/data/failover/admin-trading/state/; rsync -av admin-trading:/opt/trading/perf/perf.db /opt/trading/data/failover/admin-trading/perf/; rsync -av --delete admin-trading:/srv/sftp/shared_files/shared/desk_pro/latest/ /opt/trading/data/failover/admin-trading/shared_snapshots/desk_pro_latest/; rsync -av admin-trading:/srv/sftp/shared_files/shared/vision_outbox/ /opt/trading/data/failover/admin-trading/shared_snapshots/vision_outbox/; find /opt/trading/data/failover/admin-trading -maxdepth 3 -type f | sort | tail -n 20'"
```

But :
- disposer d'une copie locale sur `fantome`
- remplacer temporairement le role de cache/stockage de `db-layer`

### Etape 6 - Validation apres copie

```bash
ssh fantome "bash -lc 'ls -lh /opt/trading/data/failover/admin-trading/state/events.jsonl; ls -lh /opt/trading/data/failover/admin-trading/perf/perf.db; ls -lh /opt/trading/data/failover/admin-trading/shared_snapshots/desk_pro_latest; ls -lt /opt/trading/data/failover/admin-trading/shared_snapshots/vision_outbox | head -n 10'"
```

Attendu :
- `events.jsonl` et `perf.db` existent sur `fantome`
- les artefacts `desk_pro/latest` sont presents
- `vision_outbox` contient des fichiers recents

## 6. Routine operateur en mode degrade

### Trading / Perf / Desk
- UI Perf : `http://192.168.0.111:8010/perf/ui`
- UI Desk : `http://192.168.0.111:8010/desk/ui`
- source runtime : `admin-trading`

### Cockpit / Fleet / Gateway
- LocalCMS : `http://192.168.0.191:8700/`
- OpenClaw gateway : tunnel SSH vers `fantome`

```powershell
ssh -L 18789:127.0.0.1:18789 fantome
```

### Recuperation d'artefacts depuis `cursor-ai`

```powershell
scp admin-trading:/opt/trading/state/events.jsonl .
scp admin-trading:/opt/trading/perf/perf.db .
scp -r fantome:/opt/trading/data/failover/admin-trading/shared_snapshots/desk_pro_latest .
scp -r fantome:/opt/trading/data/failover/admin-trading/shared_snapshots/vision_outbox .
```

## 7. Checks periodiques recommandes

### Toutes les 5 minutes

```bash
ssh admin-trading 'bash -lc "systemctl is-active tv-webhook.service tv-perf.service bot_vision_step2.service"'
ssh fantome 'bash -lc "systemctl is-active shared-sshfs.service localcms.service openclaw-gateway.service opt-trading-runtime-health.timer opt-trading-fleet-orchestrator.timer"'
```

### Toutes les 15 minutes

```bash
ssh fantome "bash -lc 'rsync -av admin-trading:/opt/trading/state/events.jsonl /opt/trading/data/failover/admin-trading/state/; rsync -av admin-trading:/opt/trading/perf/perf.db /opt/trading/data/failover/admin-trading/perf/'"
```

Automatisation recommandee sur `fantome` :

```bash
cp deploy/systemd/opt-trading-admin-failover-sync.service /etc/systemd/system/
cp deploy/systemd/opt-trading-admin-failover-sync.timer /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now opt-trading-admin-failover-sync.timer
systemctl status opt-trading-admin-failover-sync.timer
```

Le timer appelle : `bash /opt/trading/scripts/fantome_admin_failover_sync.sh`

### En fin de session operateur

```bash
ssh admin-trading 'cd /opt/trading && scripts/admin_trading/desk_pro_cmd.sh export-html-latest'
ssh admin-trading 'cd /opt/trading && scripts/admin_trading/desk_pro_cmd.sh copy-latest-to-shared'
ssh fantome 'bash -lc "rsync -av --delete admin-trading:/srv/sftp/shared_files/shared/desk_pro/latest/ /opt/trading/data/failover/admin-trading/shared_snapshots/desk_pro_latest/"'
```

## 8. Signes d'echec immediat
- `ssh db-layer` recommence a etre la seule source de verite dans les habitudes operateur
- `tv-webhook.service` ou `tv-perf.service` passe `inactive`
- `/shared` n'est plus monte sur `fantome`
- `LocalCMS` ne repond plus sur `8700`
- `openclaw gateway probe` ne repond plus `Reachable: yes`
- `desk_pro/latest` reste stale apres `copy-latest-to-shared`

## 9. Rollback quand `db-layer` revient

### Etape 1 - Requalifier `db-layer`

```powershell
ssh db-layer "hostname"
ssh db-layer "systemctl is-active shared-sshfs.service"
ssh db-layer "ls -ld /opt/trading /opt/trading/data /shared"
```

### Etape 2 - Rejouer la verification runtime

```bash
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/healthcheck.py --dry-run --no-telegram'
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --map config/machine_runtime_map.yml --dry-run --no-telegram'
```

### Etape 3 - Sortir du mode degrade
- arreter d'utiliser `fantome` comme copie locale de secours
- revenir a `db-layer` pour les usages de consultation/stockage central qui lui appartiennent
- conserver `admin-trading` comme source runtime trading

### Etape 4 - Nettoyage optionnel sur `fantome`

```bash
ssh fantome 'bash -lc "ls -lh /opt/trading/data/failover/admin-trading"'
```

Supprimer seulement apres validation humaine explicite.

## 10. Limites de ce runbook
- ne redeploie aucun nouveau service systemd
- ne deplace pas les services trading hors `admin-trading`
- ne promeut pas `student` en machine de prod
- ne reconfigure pas automatiquement `LocalCMS`
- ne repare pas `db-layer`; il contourne son absence
