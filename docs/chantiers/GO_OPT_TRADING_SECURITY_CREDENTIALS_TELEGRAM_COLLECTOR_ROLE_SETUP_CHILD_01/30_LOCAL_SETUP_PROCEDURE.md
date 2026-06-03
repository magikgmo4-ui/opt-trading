# Local Setup Procedure

Cette procédure doit être effectuée manuellement sur chaque machine autorisée. **Ne jamais saisir de secrets réels dans un environnement partagé (Git, ChatGPT, Logs).**

## 1. Structure des répertoires
```bash
sudo install -d -m 700 /etc/opt-trading/env.d/roles
sudo install -d -m 700 /etc/opt-trading/secrets/telegram
```

## 2. Configuration du Rôle
Utiliser `sudoedit` pour créer le fichier d'environnement :
```bash
sudoedit /etc/opt-trading/env.d/roles/telegram_collector.env
```

Contenu attendu (à remplir avec les vraies valeurs locales) :
```env
TELEGRAM_API_ID=XXXXX
TELEGRAM_API_HASH=YYYYY
TELEGRAM_SESSION_PATH=/etc/opt-trading/secrets/telegram/collector.session
TELEGRAM_BOT_TOKEN=ZZZZZ:AAAAA
TELEGRAM_CHANNELS_CONFIG=configs/telegram/channels.yaml
TELEGRAM_ALERT_CHAT_ID=NNNNN
# Multi-canal routing (PR #1063) — laisser vide pour fallback sur TELEGRAM_CHAT_ID
TELEGRAM_CHAT_ID_ALERTS=
TELEGRAM_CHAT_ID_PIPELINE=
TELEGRAM_CHAT_ID_PUSH=
TELEGRAM_CHAT_ID_OPS=
```

## 3. Sécurisation
```bash
sudo chmod 600 /etc/opt-trading/env.d/roles/telegram_collector.env
```

## 4. Fichier Session
Le fichier `.session` doit être placé ou généré dans `/etc/opt-trading/secrets/telegram/` et protégé avec un `chmod 600`.
