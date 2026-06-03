---
doc_id: GO_OPT_TRADING_OPENCLAW_GOVERNANCE_CHILD_SECURITY_CREDENTIALS_METHOD_01_ROTATION_RUNBOOK
doc_type: runbook
repo: opt-trading
go_id: GO_OPT_TRADING_OPENCLAW_GOVERNANCE_CHILD_SECURITY_CREDENTIALS_METHOD_01
status: ACTIVE
created_at: 2026-06-03
---

# 60_ROTATION_RUNBOOK — Credentials Rotation

## Règle générale

```
1. Générer le nouveau secret CÔTÉ SOURCE (console, BotFather, etc.)
2. Mettre à jour le fichier local (jamais Git)
3. Redémarrer uniquement le(s) service(s) concerné(s)
4. Vérifier health / smoke
5. Révoquer l'ancien secret côté source
6. Émettre un CREDENTIAL_CHANGE_REQUEST ROTATE dans le registry
```

Ne jamais écrire de valeur réelle dans Git, les logs, les docs, les screenshots.

---

## TELEGRAM_BOT_TOKEN

**Propriétaire** : @BotFather sur Telegram
**Fichiers** : `/opt/trading/.env` (ligne `TELEGRAM_BOT_TOKEN=`)
**Services impactés** : gateway OpenClaw, `shared/telegram_notify.py`, tous les canaux multi-canal

```bash
# 1. Générer nouveau token via @BotFather → /revoke → copier le nouveau token
# 2. Mettre à jour .env
nano /opt/trading/.env   # modifier TELEGRAM_BOT_TOKEN=<nouveau>

# 3. Redémarrer gateway
sudo -u openclaw tmux send-keys -t openclaw-gateway C-c
sleep 2
sudo -u openclaw tmux send-keys -t openclaw-gateway \
  "openclaw gateway run >> ~/.openclaw/logs/gateway_foreground.log 2>&1" Enter
sleep 5

# 4. Vérifier
sudo -u openclaw openclaw gateway health
# Attendu : Gateway Health OK, Telegram: ok (@<nom_bot>)

# 5. Smoke Telegram
python3 -c "
from shared.telegram_channels import get_channel
from shared.telegram_notify import send_message
send_message('rotation-smoke OK')
"
```

---

## TV_WEBHOOK_KEY (TradingView)

**Propriétaire** : Console TradingView → Alerts → Webhook URL
**Fichiers** : `/opt/trading/.env` (ligne `TV_WEBHOOK_KEY=`)
**Services impactés** : `webhook_server.py` (validation HMAC sur `POST /tv`)

```bash
# 1. Générer nouvelle clé (openssl ou manuel)
openssl rand -hex 32

# 2. Mettre à jour .env
nano /opt/trading/.env   # modifier TV_WEBHOOK_KEY=<nouveau>

# 3. Redémarrer webhook server
# (via systemd ou tmux selon déploiement)
sudo systemctl restart opt-trading-webhook.service 2>/dev/null || \
  tmux send-keys -t webhook-server C-c && \
  tmux send-keys -t webhook-server "python3 webhook_server.py" Enter

# 4. Mettre à jour le webhook URL dans TradingView avec la nouvelle clé
# TradingView → Alert → Webhook URL → ?key=<nouveau>

# 5. Smoke
curl -s -X POST http://127.0.0.1:8000/tv \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Key: <nouveau>" \
  -d '{"ticker":"BTCUSDT","action":"GO_LONG"}' | python3 -m json.tool
```

---

## Bitget API Keys (readonly_main)

**Propriétaire** : Console Bitget → API Management
**Fichiers** : `/opt/trading/.secrets/bitget.env` (chmod 600, hors git)
**Services impactés** : `modules/simex_bitget_bridge/`, `modules/derivatives_collector/`

```bash
# 1. Créer nouvelles clés sur console Bitget (scope READ ONLY uniquement)
# Confirmer : Order=NO, Trade=NO, Withdraw=NO, Read=YES

# 2. Mettre à jour le fichier secrets
nano /opt/trading/.secrets/bitget.env
# BITGET_READONLY_MAIN_API_KEY=<nouveau>
# BITGET_READONLY_MAIN_SECRET_KEY=<nouveau>
# BITGET_READONLY_MAIN_PASSPHRASE=<nouveau>

# 3. Vérifier chargement
python3 -c "
from modules.auth.bitget_credentials import load_credentials, secrets_file_status
print(secrets_file_status())
status, creds = load_credentials()
print('status:', status)
"
# Attendu : status=ok

# 4. Révoquer anciennes clés sur console Bitget
# 5. Smoke collector
bash modules/derivatives_collector/scripts/cmd.sh smoke
```

---

## OpenAI / OpenRouter (via OpenClaw)

**Propriétaire** : platform.openai.com / openrouter.ai
**Fichiers** : `~/.openclaw/openclaw.json` (géré par openclaw CLI, jamais édité manuellement)
**Services impactés** : gateway OpenClaw, tous les agents

```bash
# 1. Générer nouvelle clé sur platform.openai.com ou openrouter.ai

# 2. Mettre à jour via openclaw (interactive — ne pas éditer le JSON directement)
sudo -u openclaw openclaw configure --section model

# 3. Redémarrer gateway
sudo -u openclaw tmux send-keys -t openclaw-gateway C-c
sleep 2
sudo -u openclaw tmux send-keys -t openclaw-gateway \
  "openclaw gateway run >> ~/.openclaw/logs/gateway_foreground.log 2>&1" Enter
sleep 5
sudo -u openclaw openclaw gateway health

# 4. Révoquer l'ancienne clé côté source
```

---

## Telegram CHAT_IDs multi-canal

**Propriétaire** : groupes Telegram (OT_ALERTS_CRITICAL, OT_PIPELINE_GATES, OT_PUSH_MARKET_DATA, OT_OPS_TOOLS)
**Fichiers** : `/etc/opt-trading/env.d/roles/telegram_collector.env` (chmod 600, hors git)
**Quand** : si un groupe est recréé ou si le bot est retiré/ré-invité

```bash
# 1. Ajouter le bot au nouveau groupe → récupérer le CHAT_ID via @userinfobot ou /getUpdates
# 2. Mettre à jour le fichier système
sudo nano /etc/opt-trading/env.d/roles/telegram_collector.env

# 3. Aligner groupAllowFrom dans openclaw
NEW_IDS=$(sudo cat /etc/opt-trading/env.d/roles/telegram_collector.env \
  | grep '^TELEGRAM_CHAT_ID' | cut -d= -f2 \
  | python3 -c "import sys,json; ids=[l.strip() for l in sys.stdin if l.strip()]; print(json.dumps(ids))")
sudo -u openclaw openclaw config set channels.telegram.groupAllowFrom "$NEW_IDS"

# 4. Redémarrer gateway
sudo -u openclaw tmux send-keys -t openclaw-gateway C-c
sleep 2
sudo -u openclaw tmux send-keys -t openclaw-gateway \
  "openclaw gateway run >> ~/.openclaw/logs/gateway_foreground.log 2>&1" Enter
sleep 5
sudo -u openclaw openclaw gateway health
```

---

## Sync multi-machine (fantome → admin-trading)

Après rotation sur fantome, synchroniser vers admin-trading :

```bash
# Depuis admin-trading
ssh fantome "cat /etc/opt-trading/env.d/roles/telegram_collector.env" \
  | grep '^TELEGRAM_CHAT_ID' \
  | sudo tee /etc/opt-trading/env.d/roles/telegram_collector.env > /dev/null
sudo chmod 600 /etc/opt-trading/env.d/roles/telegram_collector.env

# Puis réaligner groupAllowFrom + redémarrer gateway (voir section CHAT_IDs ci-dessus)
```

---

## Checklist post-rotation

```
[ ] Nouveau secret généré côté source
[ ] Fichier local mis à jour (chmod correct)
[ ] Service(s) redémarré(s)
[ ] Health / smoke PASS
[ ] Ancien secret révoqué côté source
[ ] CREDENTIAL_CHANGE_REQUEST ROTATE émis dans configs/env/registry/credentials.yaml
[ ] fantome synchronisé si applicable
```
