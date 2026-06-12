---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01_20_PAYLOAD
doc_type: chantier/payload
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01
machine: admin-trading
status: active
lifecycle_stage: telegram_enable_test
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01/10_TELEGRAM_ENABLE_PROCEDURE.md
---

# 20_SAFE_PAYLOAD_TEST — Tests TV_TEST avec Telegram

## Payload safe (engine TV_TEST)

Payload a envoyer sur admin-trading APRES activation Telegram :

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
    'reason': 'GO_TELEGRAM_NOTIFY_TEST_01'
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

Reponse attendue :

```json
{"ok": true}
```

## Tests de robustesse

### Test 1 : BUY

Memo payload que ci-dessus. Verifier Telegram.

### Test 2 : SELL

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
    'reason': 'GO_TELEGRAM_NOTIFY_TEST_02_SELL'
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

### Test 3 : Rejeu rapide (test anti-spam)

Envoyer 3 payloads en sequence rapide et verifier que les 3 messages arrivent.

### Test 4 : Payload invalide (pas de notification)

Envoyer un payload avec `signal: "INVALID"` et verifier qu'aucun message Telegram n'est envoye.

## Verification Telegram

Pour chaque test, ouvrir le chat Telegram et confirmer :

| Check | Attendu |
| --- | --- |
| Message arrive | Oui |
| Format | `BUY/SYMBOL TF` |
| `engine: TV_TEST` | Visible |
| `reason: GO_TELEGRAM_NOTIFY_*` | Visible |
| Token/secret | Aucun |
| Chat ID | Aucun |
| Doublons | Pas de doublons intempestifs |
| Invalid payload | Pas de message pour signal INVALID |

## Format attendu du message Telegram

```
BUY TEST/USDT 1m
engine: TV_TEST
price: 100.0 | tp: 110.0 | sl: 95.0
reason: GO_TELEGRAM_NOTIFY_TEST_01
qty: 20.0 | risk_usd: 100.0
```

## Checks post-test

```bash
# Verifier events
tail -5 /opt/trading/state/events.jsonl | python3 -m json.tool | grep reason

# Verifier no-trade
curl -sS http://127.0.0.1:8010/perf/open | python3 -c "
import json, sys
trades = json.load(sys.stdin).get('open', [])
tv = [t for t in trades if t.get('engine') == 'TV_TEST']
print(f'TV_TEST trades: {len(tv)}')
assert len(tv) == 0
"
```

## RISKS

- À qualifier.
