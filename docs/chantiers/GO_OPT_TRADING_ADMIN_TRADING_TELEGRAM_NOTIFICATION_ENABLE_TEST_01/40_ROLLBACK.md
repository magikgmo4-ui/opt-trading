---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01_40_ROLLBACK
doc_type: chantier/rollback
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01
machine: admin-trading
status: active
lifecycle_stage: telegram_enable_test
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01/10_TELEGRAM_ENABLE_PROCEDURE.md
---

# 40_ROLLBACK — Desactivation Telegram

## Rollback standard (post-test normal)

Si le test est termine et qu'on veut desactiver Telegram :

```bash
# 1. Supprimer ou commenter les lignes Telegram dans .env
sed -i '/^TELEGRAM_ENABLED=/d' /opt/trading/.env
sed -i '/^TELEGRAM_BOT_TOKEN=/d' /opt/trading/.env
sed -i '/^TELEGRAM_CHAT_ID=/d' /opt/trading/.env

# 2. Redemarrer le service
sudo systemctl restart tv-webhook.service
sleep 2

# 3. Verifier que Telegram est desactive
systemctl show tv-webhook.service -p Environment | tr ' ' '\n' | grep -i telegram
# Attendu : rien (aucune variable Telegram)

# 4. Verifier que le service repond encore
curl -sS http://127.0.0.1:8000/api/state
```

## Rollback d'urgence (anomalie)

### Scénario A : Spam Telegram

Si trop de messages sont envoyes :

```bash
# 1. Desactiver immediatement
sudo sed -i 's/^TELEGRAM_ENABLED=1/TELEGRAM_ENABLED=0/' /opt/trading/.env
sudo systemctl restart tv-webhook.service

# 2. Verifier
journalctl -u tv-webhook.service --since "1 min ago" --no-pager
```

### Scenario B : Bot bloque / token revoque

```bash
# Verifier l'etat du bot
python3 -c "
import os, requests
token = os.getenv('TELEGRAM_BOT_TOKEN')
r = requests.post(f'https://api.telegram.org/bot{token}/getMe', timeout=10)
print(r.json())
"
# Si KO -> suivre rollback standard
```

### Scenario C : Service instable apres ajout Telegram

```bash
# 1. Restaurer le .env depuis le backup
cp /opt/trading/.env.bak /opt/trading/.env  # si backup cree avant
sudo systemctl restart tv-webhook.service

# 2. Si pas de backup, rollback standard
```

## Nettoyage post-test

```bash
# Supprimer les backup eventuels
rm -f /opt/trading/.env.bak
```
