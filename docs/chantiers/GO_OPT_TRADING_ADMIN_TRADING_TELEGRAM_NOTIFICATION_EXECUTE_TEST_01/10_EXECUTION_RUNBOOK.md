---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_EXECUTE_TEST_01_10_RUNBOOK
doc_type: chantier/runbook
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_EXECUTE_TEST_01
machine: admin-trading
status: active
lifecycle_stage: telegram_execute_test
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01/10_TELEGRAM_ENABLE_PROCEDURE.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01/20_SAFE_PAYLOAD_TEST.md
---

# 10_EXECUTION_RUNBOOK — Runbook d'execution Telegram

## Etape 1 : Precheck

```bash
ssh admin-trading
cd /opt/trading
git log -1 --oneline

# Verifier flags
python3 -c "
import json
with open('modules/tradingview_observer/templates/alert_webhook_template_v1.json') as f:
    t = json.load(f)
assert t['risk']['trade_allowed'] == False
assert t['routing']['admin_trading_runtime'] == False
print('PASS: flags ok')
"

# Verifier TV_TEST config
python3 -c "
import json
with open('state/risk_config.json') as f:
    cfg = json.load(f)
assert 'TV_TEST' in cfg.get('accounts', {}), 'TV_TEST missing'
print('PASS: TV_TEST config present')
"
```

- [ ] Flags `false` confirmes
- [ ] TV_TEST config present

## Etape 2 : Appliquer credentials Telegram

Editer `/opt/trading/.env` (sur admin-trading uniquement, NE PAS COMMITTER) :

```bash
# Ajouter en fin de fichier :
TELEGRAM_ENABLED=1
TELEGRAM_BOT_TOKEN=<token_reel>
TELEGRAM_CHAT_ID=<chat_id_reel>
```

Redemarrer :

```bash
sudo systemctl restart tv-webhook.service
sleep 3
systemctl is-active tv-webhook.service
```

- [ ] `.env` edite (credentials reels, pas de guillemets)
- [ ] Service redemarre actif

## Etape 3 : Tester connectivite Telegram

```bash
source /opt/trading/.env
python3 -c "
import os, requests
token = os.getenv('TELEGRAM_BOT_TOKEN')
r = requests.get(f'https://api.telegram.org/bot{token}/getMe', timeout=10)
d = r.json()
assert d.get('ok'), f'getMe failed: {d}'
print(f'Bot: {d[\"result\"][\"first_name\"]} (@{d[\"result\"][\"username\"]})')
"
```

- [ ] `getMe` retourne `{"ok": true}`
- [ ] Bot name correct

## Etape 4 : Envoyer payload TV_TEST avec Telegram

```bash
python3 -c "
import urllib.request, json
data = json.dumps({
    'engine': 'TV_TEST',
    'signal': 'BUY',
    'symbol': 'TEST/USDT',
    'tf': '1m',
    'price': 100.0,
    'tp': 110.0,
    'sl': 95.0,
    'reason': 'GO_TELEGRAM_EXECUTE_TEST_BUY_01'
}).encode()
req = urllib.request.Request(
    'http://127.0.0.1:8000/tv',
    data=data,
    headers={'Content-Type': 'application/json'}
)
resp = urllib.request.urlopen(req, timeout=15)
print('HTTP:', resp.status)
print(resp.read().decode())
"
```

Reponse attendue : `HTTP: 200 {"ok": true}`

- [ ] HTTP 200
- [ ] `{"ok": true}`

## Etape 5 : Verifier Telegram

Ouvrir le chat Telegram cible :

- [ ] Message recu
- [ ] Contient `BUY TEST/USDT 1m`
- [ ] Contient `engine: TV_TEST`
- [ ] Contient `GO_TELEGRAM_EXECUTE_TEST_BUY_01`
- [ ] Aucun token/secret visible

## Etape 6 : Envoyer SELL

```bash
python3 -c "
import urllib.request, json
data = json.dumps({
    'engine': 'TV_TEST',
    'signal': 'SELL',
    'symbol': 'TEST/USDT',
    'tf': '1m',
    'price': 100.0,
    'tp': 90.0,
    'sl': 110.0,
    'reason': 'GO_TELEGRAM_EXECUTE_TEST_SELL_01'
}).encode()
req = urllib.request.Request(
    'http://127.0.0.1:8000/tv',
    data=data,
    headers={'Content-Type': 'application/json'}
)
resp = urllib.request.urlopen(req, timeout=15)
print('HTTP:', resp.status)
print(resp.read().decode())
"
```

- [ ] HTTP 200
- [ ] Message Telegram SELL recu

## Etape 7 : Rejeu x3

```bash
for i in 1 2 3; do
  python3 -c "
import urllib.request, json
data = json.dumps({
    'engine': 'TV_TEST',
    'signal': 'BUY',
    'symbol': 'TEST/USDT',
    'tf': '1m',
    'price': 100.0,
    'sl': 95.0,
    'reason': 'GO_TELEGRAM_REJEU_$i'
}).encode()
req = urllib.request.Request('http://127.0.0.1:8000/tv', data=data, headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req, timeout=15)
print(f'Rejeu #$i:', resp.status)
"
done
```

- [ ] 3/3 HTTP 200
- [ ] 3 messages Telegram recus

## Etape 8 : Verifications finales

```bash
# Events
tail -6 /opt/trading/state/events.jsonl | python3 -c "
import json, sys
for line in sys.stdin:
    e = json.loads(line.strip())
    print(f'  engine={e[\"engine\"]} reason={e.get(\"reason\",\"?\")[:50]}')
"

# No-trade
curl -sS http://127.0.0.1:8010/perf/open | python3 -c "
import json, sys
trades = json.load(sys.stdin).get('open', [])
tv = [t for t in trades if t.get('engine') == 'TV_TEST']
print(f'TV_TEST in perf: {len(tv)}')
assert len(tv) == 0
print('PASS: 0 TV_TEST trades')
"
```

- [ ] Events TV_TEST confirmes
- [ ] 0 TV_TEST trades

## Etape 9 : Rollback Telegram (optionnel)

Si on veut desactiver apres le test :

```bash
sed -i '/^TELEGRAM_ENABLED=/d' /opt/trading/.env
sed -i '/^TELEGRAM_BOT_TOKEN=/d' /opt/trading/.env
sed -i '/^TELEGRAM_CHAT_ID=/d' /opt/trading/.env
sudo systemctl restart tv-webhook.service
```

## Tableau de resultats

| Etape | Test | HTTP | Telegram | No-trade | Resultat |
| --- | --- | --- | --- | --- | --- |
| 1 | Precheck | - | - | - | |
| 2 | Credentials .env | - | - | - | |
| 3 | getMe | 200 `ok:true` | - | - | |
| 4 | BUY TV_TEST | 200 | Message | - | |
| 5 | Verif Telegram | - | Format OK | - | |
| 6 | SELL TV_TEST | 200 | Message | - | |
| 7 | Rejeu x3 | 200x3 | 3 messages | - | |
| 8 | Verif finale | - | - | 0 trades | |
