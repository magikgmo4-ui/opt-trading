# RUNBOOK — Ops & Debug

## Services (exemples)
```bash
sudo systemctl status tv-webhook.service --no-pager
sudo systemctl status ngrok-tv.service --no-pager
journalctl -u tv-webhook.service -n 80 --no-pager
```

## Réseau Windows/LAN (checklist)
1) Le serveur écoute sur `0.0.0.0:PORT` (pas 127.0.0.1)
2) Le port est ouvert en LAN (UFW/iptables)
3) Test depuis Windows :
```powershell
curl http://IP_LAN:8010/dash
curl http://IP_LAN:8010/perf/ui
```

## Smoke test
Voir `scripts/smoke.sh`.
