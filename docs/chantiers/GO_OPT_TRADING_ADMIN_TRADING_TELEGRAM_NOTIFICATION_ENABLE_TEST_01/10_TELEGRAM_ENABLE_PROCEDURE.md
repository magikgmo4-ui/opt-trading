---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01_10_PROCEDURE
doc_type: chantier/procedure
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01
machine: admin-trading
status: active
lifecycle_stage: telegram_enable_test
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01/00_START.md
---

# 10_TELEGRAM_ENABLE_PROCEDURE — Activation Telegram

## Etat actuel

- Service : `tv-webhook.service`
- EnvironmentFile : `/opt/trading/.env`
- `.env` actuel : placeholders commentes pour TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID
- `TELEGRAM_ENABLED` : non defini (defaut `0`)

## Procedure pas-a-pas

### Etape 1 : Verifier l'etat pre-activation

```bash
ssh admin-trading

# Verifier que le service est actif
systemctl is-active tv-webhook.service  # doit etre active

# Verifier l'env actuel
systemctl show tv-webhook.service -p Environment | tr ' ' '\n' | grep -i telegram
# Attendu : rien (TELEGRAM non configure)

# Verifier l'API state
curl -sS http://127.0.0.1:8000/api/state  # doit retourner 200
```

- [ ] Service actif
- [ ] TELEGRAM non configure
- [ ] API accessible

### Etape 2 : Verifier les flags securite

```bash
python3 -c "
import json
with open('/opt/trading/modules/tradingview_observer/templates/alert_webhook_template_v1.json') as f:
    t = json.load(f)
assert t['risk']['trade_allowed'] == False, 'FAIL'
assert t['routing']['admin_trading_runtime'] == False, 'FAIL'
print('PASS: trade_allowed=false, admin_trading_runtime=false')
"
```

- [ ] `trade_allowed=false`
- [ ] `admin_trading_runtime=false`

### Etape 3 : Editer .env (NE PAS COMMITTER)

Ajouter dans `/opt/trading/.env` :

```bash
# A executer sur admin-trading uniquement
# Remplacer <TOKEN> et <CHAT_ID> par les valeurs reelles

cat >> /opt/trading/.env << 'ENVEOF'

# Telegram notification (GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01)
TELEGRAM_ENABLED=1
TELEGRAM_BOT_TOKEN=<TOKEN>
TELEGRAM_CHAT_ID=<CHAT_ID>
ENVEOF
```

Verifier que les valeurs ne contiennent pas de guillemets superflus :

```bash
grep TELEGRAM /opt/trading/.env
# Attendu :
# TELEGRAM_ENABLED=1
# TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
# TELEGRAM_CHAT_ID=-100123456...
```

- [ ] `TELEGRAM_ENABLED=1` dans `.env`
- [ ] `TELEGRAM_BOT_TOKEN` avec token valide (pas de guillemets)
- [ ] `TELEGRAM_CHAT_ID` avec chat ID valide
- [ ] `.env` non committe (verifier `git status`)

### Etape 4 : Redemarrer le service

```bash
sudo systemctl restart tv-webhook.service
sleep 2
systemctl is-active tv-webhook.service  # doit etre active

# Verifier que le service a bien charge les variables
systemctl show tv-webhook.service -p Environment | tr ' ' '\n' | grep -E "TELEGRAM_ENABLED=1|TELEGRAM_BOT_TOKEN|TELEGRAM_CHAT_ID"
# Attendu : les 3 variables apparaissent (token et chat_id masques ici)
```

- [ ] Service redemarre sans erreur
- [ ] `TELEGRAM_ENABLED=1` charge
- [ ] `TELEGRAM_BOT_TOKEN` charge
- [ ] `TELEGRAM_CHAT_ID` charge

### Etape 5 : Tester la connectivite Telegram (hors webhook)

```bash
python3 -c "
import os, requests
token = os.getenv('TELEGRAM_BOT_TOKEN')
r = requests.post(f'https://api.telegram.org/bot{token}/getMe', timeout=10)
print(r.json())
# Attendu : {\"ok\": true, \"result\": {\"first_name\": \"...\", \"username\": \"...\"}}
"
```

- [ ] `getMe` retourne `{"ok": true}`
- [ ] Bot name correct

### Etape 6 : Envoyer un payload TV_TEST

Voir `20_SAFE_PAYLOAD_TEST.md` pour la procedure de test.

### Etape 7 : Verifier la reception Telegram

Ouvrir le chat Telegram cible et verifier :

- [ ] Message recu
- [ ] Contient `BUY TEST/USDT 1m`
- [ ] Contient `engine: TV_TEST`
- [ ] Contient le `reason` du test
- [ ] Aucun token/secret visible

### Etape 8 : Verifier les logs

```bash
journalctl -u tv-webhook.service --since "2 min ago" --no-pager | grep -i telegram
```

- [ ] Pas d'erreur `RuntimeError: Telegram env vars not set`
- [ ] Pas d'HTTPError vers `api.telegram.org`
