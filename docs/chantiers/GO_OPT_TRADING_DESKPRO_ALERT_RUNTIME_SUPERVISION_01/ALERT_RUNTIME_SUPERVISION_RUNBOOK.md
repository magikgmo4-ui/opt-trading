---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_RUNTIME_SUPERVISION_01
doc_type: runbook
status: ACTIVE
updated_at: 2026-05-18
---

# Desk Pro — Alert Runtime Supervision Runbook

Supervision opérationnelle du pipeline d'alerte.
Complète `ALERT_CONFIG_RUNBOOK.md` (PR #571) avec la couche runtime.

---

## 1. Architecture des services

```
Port 8000  ──  webhook_server.py       ──  incoming TradingView webhooks
Port 8010  ──  modules.perf.app:app    ──  Desk Pro / perf FastAPI
                └── /desk/status       ──  health + alert dispatch
                └── /desk/alert/test   ──  smoke delivery
                └── /desk/ui           ──  interface opérateur
```

| Service | Port | Entrypoint | Mode local | Mode production |
|---|---|---|---|---|
| webhook | 8000 | `webhook_server.py` | tmux `trading-pipeline` | `tv-webhook.service` |
| perf/desk | 8010 | `modules.perf.app:app` | tmux `desk-pro` | `tv-perf.service` |

---

## 2. Démarrage local (tmux)

### Desk Pro / perf (port 8010)

```bash
cd /opt/trading
source scripts/load_env.sh   # charge .env, exporte TV_PERF_BASE_URL

# Option A — toolbox canonical (venv requis)
bash scripts/desk_pro_ui_toolbox_final_cmd.sh restart

# Option B — manuel (system python si venv absent)
PERF_DB_PATH=/opt/trading/tmp/perf_test.db \
nohup python3 -m uvicorn modules.perf.app:app \
  --host 127.0.0.1 --port 8010 \
  >> /opt/trading/tmp/uvicorn_8010.log 2>&1 &
```

Vérifier up :
```bash
curl -s http://127.0.0.1:8010/desk/health
# attendu : {"ok": true, "module": "desk_pro", ...}
```

### Webhook server (port 8000)

```bash
# Si modules/webhook/cmd.sh existe :
bash modules/webhook/cmd.sh run 2>&1 | tee logs/webhook.log

# Sinon, via tmux session :
bash scripts/tmux/sessions/trading-pipeline.sh
```

Vérifier up :
```bash
curl -s http://127.0.0.1:8000/api/state || echo "webhook DOWN"
```

### Démarrer tous les services via tmux

```bash
bash scripts/tmux/start_all.sh
```

---

## 3. Démarrage production (systemd — admin-trading)

```bash
sudo systemctl start  tv-webhook.service tv-perf.service
sudo systemctl status tv-webhook.service tv-perf.service --no-pager

# Restart :
sudo systemctl restart tv-webhook.service
bash scripts/desk_pro_ui_toolbox_final_cmd.sh restart   # perf/desk

# Logs :
sudo journalctl -u tv-webhook.service -n 100 --no-pager
sudo journalctl -u tv-perf.service    -n 100 --no-pager
tail -f /opt/trading/tmp/uvicorn_8010.log
```

---

## 4. Health checks

```bash
# Desk Pro health
curl -s http://127.0.0.1:8010/desk/health | python3 -m json.tool

# Desk Pro status complet (health + perf + alert + cooldown)
curl -s http://127.0.0.1:8010/desk/status | python3 -c "
import sys, json
d = json.load(sys.stdin)
a = d.get('alert', {})
print('alert.triggered:', a.get('triggered'))
print('alert.reason:', a.get('reason'))
print('cooldown_remaining:', a.get('cooldown_remaining_sec'))
dest = d.get('destinations', {})
print('telegram:', dest.get('telegram'))
print('webhook:', dest.get('webhook'))
"

# Destinations + historique alertes
curl -s http://127.0.0.1:8010/desk/alerts | python3 -m json.tool

# Webhook server
curl -s http://127.0.0.1:8000/api/state | python3 -m json.tool || echo "webhook DOWN"

# Diagnostic complet
bash scripts/diagnose.sh
```

---

## 5. Alert smoke test

```bash
# Tester les destinations configurées (sans cooldown, sans JSONL)
curl -s -X POST http://127.0.0.1:8010/desk/alert/test | python3 -c "
import sys, json
d = json.load(sys.stdin)
for dest in d['dispatch']:
    r = dest.get('reason','')
    print(f'  {dest[\"destination\"]}: {dest[\"status\"]}')
"
```

Résultats attendus selon config (voir `ALERT_CONFIG_RUNBOOK.md`) :
- Telegram configuré → `delivered`
- Webhook générique → `delivered`
- Config absente → `skipped`
- `ALERT_WEBHOOK_URL=api.telegram.org/...` → `failed` (reason explicite)

---

## 6. Vérification env (masqué)

```bash
# Vérifier présence sans afficher valeurs
[[ -n "$TELEGRAM_BOT_TOKEN" ]] && echo "BOT_TOKEN: SET" || echo "BOT_TOKEN: ABSENT"
[[ -n "$TELEGRAM_CHAT_ID" ]]   && echo "CHAT_ID: SET"   || echo "CHAT_ID: ABSENT"
[[ -n "$ALERT_WEBHOOK_URL" ]]  && echo "WEBHOOK: SET"   || echo "WEBHOOK: ABSENT"

# Via API (aucun secret exposé)
curl -s http://127.0.0.1:8010/desk/alerts | python3 -c "
import sys, json; d=json.load(sys.stdin)
print('telegram configured:', d['destinations']['telegram'])
print('webhook configured:', d['destinations']['webhook'])
"
```

---

## 7. Logs

| Flux | Localisation |
|---|---|
| uvicorn (perf/desk) | `/opt/trading/tmp/uvicorn_8010.log` |
| Desk Pro UI | `/opt/trading/tmp/desk_pro_ui.log` |
| Alertes réelles | `/opt/trading/tmp/desk_pro_alerts.jsonl` |
| webhook server | `logs/webhook.log` ou `journalctl -u tv-webhook.service` |
| perf service | `journalctl -u tv-perf.service` |

```bash
# Alertes réelles (JSONL — hors smoke)
tail -10 /opt/trading/tmp/desk_pro_alerts.jsonl

# ou via API
curl -s http://127.0.0.1:8010/desk/alerts | python3 -m json.tool
```

---

## 8. Restart séquence recommandée

```bash
# 1. Arrêt propre
pkill -f "uvicorn modules\.perf\.app" || true
sleep 1

# 2. Vérifier ports libres
ss -ltnp | grep -E ':8000|:8010' || echo "ports libres"

# 3. Charger env
source /opt/trading/scripts/load_env.sh

# 4. Redémarrer perf/desk
PERF_DB_PATH=/opt/trading/tmp/perf_test.db \
nohup python3 -m uvicorn modules.perf.app:app \
  --host 127.0.0.1 --port 8010 \
  >> /opt/trading/tmp/uvicorn_8010.log 2>&1 &
sleep 3

# 5. Health check
curl -s http://127.0.0.1:8010/desk/health

# 6. Smoke alert
curl -s -X POST http://127.0.0.1:8010/desk/alert/test | python3 -m json.tool
```

**Note cooldown :** `_alert_state` est process-local. Un restart remet le cooldown à zéro.
La prochaine alerte réelle post-restart déclenchera immédiatement si `health_status = down|degraded`.

---

## 9. Commandes quotidiennes récapitulatives

```bash
# État global
bash /opt/trading/scripts/diagnose.sh 2>/dev/null | grep -E "OK|FAIL|WARN|DOWN|UP" | head -20

# Sanity Desk Pro
bash /opt/trading/scripts/sanity_desk_pro.sh

# Tests unitaires
cd /opt/trading && python3 -m unittest discover -s tests -p "test_*.py"

# UI opérateur
echo "http://127.0.0.1:8010/desk/ui"
```
