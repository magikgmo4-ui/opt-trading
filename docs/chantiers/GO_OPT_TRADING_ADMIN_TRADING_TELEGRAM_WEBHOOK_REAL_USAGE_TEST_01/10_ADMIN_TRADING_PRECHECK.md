---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01_10_PRECHECK
doc_type: chantier/precheck
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01
machine: admin-trading
status: active
lifecycle_stage: real_usage_test
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01/00_START.md
  - scripts/admin_trading/runtime_guard.sh
  - modules/tradingview_observer/templates/alert_webhook_template_v1.json
---

# 10_ADMIN_TRADING_PRECHECK — Verification etat admin-trading

## Objet

Verifier l'etat de la machine admin-trading avant tout test webhook/Telegram :
services actifs, guards operationnels, flags securite, endpoints en ecoute.

## Checklist pre-test

### 1. Services systemd

Executer sur admin-trading :

```bash
systemctl is-active tv-webhook.service   # doit etre active
systemctl is-active ngrok-tv.service     # doit etre active (si expose)
systemctl is-active tv-perf.service      # doit etre active (si perf integre)
```

- [ ] `tv-webhook.service` actif
- [ ] `ngrok-tv.service` actif (optionnel selon expo)
- [ ] `tv-perf.service` actif (optionnel selon perf)

### 2. Endpoints HTTP

```bash
curl -sS -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/dash
curl -sS -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/api/state
```

- [ ] `GET /dash` -> 200
- [ ] `GET /api/state` -> 200

### 3. Flags securite template

Verifier `alert_webhook_template_v1.json` :

```bash
python3 -c "
import json
with open('modules/tradingview_observer/templates/alert_webhook_template_v1.json') as f:
    t = json.load(f)
assert t['risk']['trade_allowed'] == False, 'FAIL: trade_allowed is True'
assert t['routing']['admin_trading_runtime'] == False, 'FAIL: admin_trading_runtime is True'
print('PASS: trade_allowed=false, admin_trading_runtime=false')
"
```

- [ ] `trade_allowed=false` dans le template
- [ ] `admin_trading_runtime=false` dans le template
- [ ] `mode: test_only` dans le template
- [ ] `signal: TEST_ONLY` dans le template

### 4. Runtime guard

Executer le guard admin-trading :

```bash
bash scripts/admin_trading/runtime_guard.sh
```

- [ ] Verdict PASS ou WARN (pas de FAIL bloquant)
- [ ] Aucun pattern critique dans journalctl (HTTPError, 5xx, missing in env)

### 5. Verification git diff

Aucune modification non intentionnelle :

```bash
git diff -- modules/ | grep "trade_allowed.*true"    # doit etre VIDE
git diff -- modules/ | grep "admin_trading_runtime.*true"  # doit etre VIDE
git diff -- webhook_server.py                         # doit etre VIDE (ou patch minimal documente)
```

- [ ] `trade_allowed` non modifie en `true`
- [ ] `admin_trading_runtime` non modifie en `true`
- [ ] `webhook_server.py` non modifie (pas de changement runtime)

### 6. Variables d'environnement

Sur admin-trading, verifier que les variables Telegram sont configurees sans exposer les valeurs :

```bash
# Presence
test -n "${TELEGRAM_BOT_TOKEN:-}" && echo "PASS: TELEGRAM_BOT_TOKEN set" || echo "WARN: TELEGRAM_BOT_TOKEN not set"
test -n "${TELEGRAM_CHAT_ID:-}" && echo "PASS: TELEGRAM_CHAT_ID set" || echo "WARN: TELEGRAM_CHAT_ID not set"

# Mode webhook key
test -n "${TV_WEBHOOK_KEY:-}" && echo "INFO: TV_WEBHOOK_KEY set (production auth)" || echo "INFO: TV_WEBHOOK_KEY not set (localhost-only mode)"

# Telegram enabled flag
test "${TELEGRAM_ENABLED:-}" = "1" && echo "PASS: TELEGRAM_ENABLED=1" || echo "INFO: TELEGRAM_ENABLED not set to 1"
```

- [ ] `TELEGRAM_BOT_TOKEN` set
- [ ] `TELEGRAM_CHAT_ID` set
- [ ] `TELEGRAM_ENABLED` mode connu
- [ ] `TV_WEBHOOK_KEY` mode connu (localhost ou production)

### 7. No real secrets in repo

```bash
grep -rE "(TELEGRAM_BOT_TOKEN|TELEGRAM_CHAT_ID|TV_WEBHOOK_KEY)=" scripts/ modules/ --include="*.py" --include="*.sh" --include="*.json" | grep -v ".env.example" | grep -v "os.getenv" | grep -v "os.environ" && echo "FAIL: possible secret in repo" || echo "PASS: no exposed secrets"
```

- [ ] Aucun secret dans les sources du repo
- [ ] `.env` non committe

## Tableau de verdict precheck

| Check | Description | Attendu | Resultat |
| --- | --- | --- | --- |
| 1 | systemd services actifs | active | |
| 2 | Endpoints HTTP 200 | 200 | |
| 3 | Flags securite template | false | |
| 4 | Runtime guard | PASS/WARN | |
| 5 | Git diff clean | VIDE | |
| 6 | Variables env Telegram | set | |
| 7 | No secrets in repo | PASS | |

## Point de blocage

Si le check 3 ou 5 echoue (trade_allowed modifie en true, ou webhook_server.py modifie), le test est BLOQUE. Ne pas proceder au-dela de ce point.
