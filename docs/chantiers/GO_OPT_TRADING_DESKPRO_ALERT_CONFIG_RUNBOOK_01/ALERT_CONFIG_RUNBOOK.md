---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_CONFIG_RUNBOOK_01
doc_type: runbook
status: ACTIVE
updated_at: 2026-05-18
---

# Desk Pro — Alert Configuration Runbook

Référence de configuration finale pour les alertes Desk Pro.
Valide à partir de PR #569 (`GO_OPT_TRADING_DESKPRO_ALERT_WEBHOOK_ADAPTER_01`).

---

## 1. Décision rapide — quelle variable utiliser ?

| Besoin | Variable(s) | Chemin |
|---|---|---|
| Recevoir les alertes sur Telegram | `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` | Telegram natif |
| Connecter un outil externe (Slack, n8n, webhook maison…) | `ALERT_WEBHOOK_URL` | Webhook générique JSON |
| Tester un webhook externe depuis le PC | `ALERT_WEBHOOK_URL` + ngrok temporaire | Smoke test local |
| Aucune config — traces locales uniquement | aucune | Fallback JSONL |

**Règle fondamentale :**

```
TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID  ──►  chemin Telegram natif
ALERT_WEBHOOK_URL                       ──►  webhook générique JSON uniquement
                                             ≠ api.telegram.org
```

---

## 2. Variables d'environnement

### Telegram natif (alertes personnelles)

```bash
TELEGRAM_BOT_TOKEN=<token_du_bot>
TELEGRAM_CHAT_ID=<id_du_chat_ou_groupe>
```

- Lues à chaque dispatch — pas au démarrage
- Absentes → destination `skipped`, pas d'erreur
- Le chemin Telegram envoie un message texte formaté :
  `"Desk Pro ALERT: status=<status>"`

### Webhook générique JSON

```bash
ALERT_WEBHOOK_URL=https://your-endpoint.example.com/hook
```

- Doit accepter `POST` avec `Content-Type: application/json`
- Payload envoyé :
  ```json
  {"ts": "2026-05-18T17:46:29Z", "status": "down"}
  ```
- Absente → `skipped`
- Retourne 200 → `delivered`
- Retourne autre code → `failed (status=<code>)`
- Erreur réseau → `failed (<message>)`

### Cooldown

```bash
ALERT_COOLDOWN_SEC=300   # défaut si absent
```

---

## 3. Ce qu'il NE FAUT PAS faire

### ❌ Mettre `api.telegram.org` dans `ALERT_WEBHOOK_URL`

```bash
# INCORRECT — rejeté explicitement depuis PR #569
ALERT_WEBHOOK_URL=https://api.telegram.org/bot<token>/sendMessage
```

**Pourquoi :** Le dispatcher webhook envoie du JSON brut (`{ts, status}`),
incompatible avec le format attendu par l'API Telegram (`{chat_id, text}`).
Depuis PR #569, ce cas est détecté et retourne :

```
webhook: failed
reason: webhook_url_is_telegram_api — use TELEGRAM_BOT_TOKEN for Telegram
```

Sans appel HTTP (pas de 401, pas de fuite de token dans les logs).

**Solution :** utiliser `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` à la place.

### ❌ Committer `.env`, tokens ou credentials

```bash
# Ces fichiers ne doivent jamais apparaître dans git :
.env          # gitignored ligne 37
.env.local    # gitignored ligne 87
secrets/      # gitignored
```

---

## 4. Configuration minimale recommandée (`.env` local)

```bash
# Alertes Telegram personnelles
TELEGRAM_BOT_TOKEN=<token>        # jamais commité
TELEGRAM_CHAT_ID=<chat_id>        # jamais commité

# Optionnel — webhook générique
# ALERT_WEBHOOK_URL=https://...   # jamais commité

# Optionnel — cooldown personnalisé
# ALERT_COOLDOWN_SEC=300
```

Vérification sans afficher les valeurs :

```bash
[[ -n "$TELEGRAM_BOT_TOKEN" ]] && echo "BOT_TOKEN: SET" || echo "BOT_TOKEN: ABSENT"
[[ -n "$TELEGRAM_CHAT_ID" ]]   && echo "CHAT_ID: SET"   || echo "CHAT_ID: ABSENT"
[[ -n "$ALERT_WEBHOOK_URL" ]]  && echo "WEBHOOK: SET"   || echo "WEBHOOK: ABSENT"
```

Ou via l'API (aucun secret exposé) :

```bash
curl -s http://127.0.0.1:8010/desk/alerts | python3 -c "
import sys, json; d=json.load(sys.stdin)
print('telegram:', d['destinations']['telegram'])
print('webhook:', d['destinations']['webhook'])
"
```

---

## 5. Smoke test

### Tester les destinations configurées

```bash
curl -s -X POST http://127.0.0.1:8010/desk/alert/test | python3 -m json.tool
```

Résultats attendus :

| Scénario | telegram | webhook |
|---|---|---|
| Aucune config | `skipped` | `skipped` |
| Telegram configuré | `delivered` | `skipped` |
| Webhook générique configuré | `skipped` | `delivered` |
| Les deux configurés | `delivered` | `delivered` |
| `ALERT_WEBHOOK_URL=api.telegram.org/...` | selon config | `failed` (reason explicite) |

**Note :** le smoke test ne déclenche pas de cooldown et n'écrit pas dans le JSONL.

### Tester un webhook externe via ngrok (temporaire, optionnel)

```bash
# 1. Démarrer un receiver local
python3 -c "
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, time

class H(BaseHTTPRequestHandler):
    def do_POST(self):
        l = int(self.headers.get('Content-Length','0'))
        body = json.loads(self.rfile.read(l))
        print('received:', body)
        self.send_response(200); self.end_headers()
        self.wfile.write(b'{\"ok\":true}')
    def log_message(self, *a): pass

HTTPServer(('127.0.0.1', 9999), H).serve_forever()
" &

# 2. Exposer via ngrok (dans un autre terminal)
ngrok http 9999

# 3. Utiliser l'URL ngrok comme variable locale (ne pas committer)
export ALERT_WEBHOOK_URL="https://<ngrok-host>/hook"

# 4. Redémarrer le serveur avec la nouvelle variable, puis tester
curl -s -X POST http://127.0.0.1:8010/desk/alert/test | python3 -m json.tool

# 5. Nettoyer : tuer ngrok et le receiver
```

---

## 6. Fallback JSONL

Fichier : `/opt/trading/tmp/desk_pro_alerts.jsonl`

- Écrit **uniquement** lors d'alertes réelles (`health_status = degraded | down`)
- Contenu : `{"ts": "...", "status": "down"}` — aucun credential
- Indépendant des destinations — persiste si Telegram et webhook sont absents
- **Non** écrit par `POST /desk/alert/test`

```bash
# Lire l'historique :
curl -s http://127.0.0.1:8010/desk/alerts | python3 -m json.tool
# ou directement :
tail -10 /opt/trading/tmp/desk_pro_alerts.jsonl
```

---

## 7. Statuts de delivery

| Statut | Signification |
|---|---|
| `delivered` | Envoi accepté par la destination (Telegram ok=true ou HTTP 200) |
| `skipped` | Variable env absente — comportement normal |
| `failed` | Erreur réseau, HTTP non-200, ou URL incompatible |

---

## 8. Garanties de non-fuite secret

| Point de contrôle | Garantie |
|---|---|
| `GET /desk/status` | `destinations.*` = bool uniquement |
| `GET /desk/alerts` | `destinations.*` = bool + historique `{ts,status}` |
| `POST /desk/alert/test` | payload `{ts,status,message}` — aucun token |
| JSONL | `{ts,status}` — aucun credential |
| Logs uvicorn | chemins HTTP uniquement, aucun header Authorization loggué |
| `.env` | gitignored ligne 37 — vérifié via `git check-ignore -v .env` |
