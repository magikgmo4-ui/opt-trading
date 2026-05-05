---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01_40_LOGS
doc_type: chantier/logs
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01
machine: admin-trading
status: active
lifecycle_stage: real_usage_test
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01/30_REAL_USAGE_TEST_PLAN.md
---

# 40_LOGS_AND_EVIDENCE — Logs et preuves de reception

## Objet

Collecter, documenter et attacher les preuves de reception webhook et
notification Telegram generees pendant le test en usage reel.

## Sources de preuves

### 1. Journal systemd (tv-webhook.service)

```bash
# Extraire les logs de la session de test
journalctl -u tv-webhook.service --since "2026-05-05 12:00:00" --until "2026-05-05 13:00:00" --no-pager
```

Format de capture attendu :
```
May 05 12:34:56 admin-trading webhook[pid]: INFO - POST /tv - engine=TV_TEST signal=BUY symbol=TEST/USDT
May 05 12:34:56 admin-trading webhook[pid]: INFO - event recorded
May 05 12:34:56 admin-trading webhook[pid]: INFO - telegram sent
```

### 2. Fichier d'evenements (state/events.jsonl)

```bash
# Extraire les evenements de test (filtrer par reason)
python3 -c "
import json
with open('state/events.jsonl') as f:
    for line in f:
        e = json.loads(line)
        if 'GO_TEST' in e.get('reason', ''):
            print(json.dumps(e, indent=2))
            print('---')
"
```

### 3. Capture d'ecran Telegram (preuve visuelle)

- Capture du message Telegram recu
- Doit montrer le contenu du message avec `GO_TEST_02_WITH_TELEGRAM`
- Ne doit pas montrer de token ou de cle

### 4. API state / metrics / events

```bash
# Snapshot API state
curl -sS http://127.0.0.1:8000/api/state | python3 -m json.tool

# Snapshot API metrics
curl -sS http://127.0.0.1:8000/api/metrics | python3 -m json.tool

# Snapshot derniers events
curl -sS "http://127.0.0.1:8000/api/events?limit=10" | python3 -m json.tool
```

## Template de preuve : Evenement JSONL

```json
{
    "key": null,
    "engine": "TV_TEST",
    "signal": "BUY",
    "symbol": "TEST/USDT",
    "tf": "1m",
    "price": 100.0,
    "tp": 110.0,
    "sl": 95.0,
    "reason": "GO_TEST_02_WITH_TELEGRAM",
    "_ts": "2026-05-05T12:34:56Z",
    "_ip": "127.0.0.1",
    "qty": 1.0,
    "risk_usd": 5.0,
    "risk_real_usd": 5.0
}
```

Champs a verifier :
- [ ] `engine: "TV_TEST"` — engine de test, pas de trading
- [ ] `key: null` — pas de cle exposee dans l'evenement
- [ ] `reason` contient l'identifiant du test
- [ ] `_ip: "127.0.0.1"` — origine locale
- [ ] `_ts` timestamp coherent

## Template de preuve : Message Telegram

Format attendu :

```
BUY TEST/USDT 1m
engine: TV_TEST
price: 100.0 | tp: 110.0 | sl: 95.0
reason: GO_TEST_02_WITH_TELEGRAM
qty: 1.0 | risk_usd: 5.0
```

Verifications :
- [ ] Pas de `TELEGRAM_BOT_TOKEN` dans le message
- [ ] Pas de `TELEGRAM_CHAT_ID` dans le message
- [ ] Pas de `TV_WEBHOOK_KEY` dans le message
- [ ] Engine bien `TV_TEST`

## Template de preuve : Logs service

Extrait attendu (lignes-cles) :

```
INFO:uvicorn.access:127.0.0.1:0 - "POST /tv HTTP/1.1" 200
INFO:webhook_server:event recorded: engine=TV_TEST signal=BUY reason=GO_TEST_02_WITH_TELEGRAM
INFO:webhook_server:telegram sent: chat_id=*****
```

Verifications :
- [ ] Code HTTP 200 pour chaque requete valide
- [ ] Code HTTP 400 pour chaque requete invalide
- [ ] Pas de code 403 (auth failure)
- [ ] Pas de code 409 (engine lock conflict)
- [ ] Pas de code 500 (internal server error)
- [ ] `chat_id` masque dans les logs (si sensible)

## Tableau de collecte des preuves

| Preuve | Source | Fichier/commande | Collectee |
| --- | --- | --- | --- |
| Logs systemd | `journalctl -u tv-webhook.service` | `logs/journalctl_test_01.log` | |
| Evenements JSONL | `state/events.jsonl` | `logs/events_test_01.jsonl` | |
| API state | `GET /api/state` | `logs/api_state_01.json` | |
| API metrics | `GET /api/metrics` | `logs/api_metrics_01.json` | |
| API events | `GET /api/events` | `logs/api_events_01.json` | |
| Capture Telegram | Telegram client | `logs/telegram_capture_01.png` | |
| Runtime guard | `scripts/admin_trading/runtime_guard.sh` | `logs/runtime_guard_01.txt` | |

## Stockage des preuves

Les preuves sont stockees sur la machine admin-trading (pas dans le repo) :

```
~/opt-trading-logs/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01/
├── logs/
│   ├── journalctl_test_01.log
│   ├── events_test_01.jsonl
│   ├── api_state_01.json
│   ├── api_metrics_01.json
│   ├── api_events_01.json
│   ├── telegram_capture_01.png
│   └── runtime_guard_01.txt
└── README.md (repertoire de preuves, pas de secrets)
```

Ne pas committer ces fichiers dans le repo opt-trading.
