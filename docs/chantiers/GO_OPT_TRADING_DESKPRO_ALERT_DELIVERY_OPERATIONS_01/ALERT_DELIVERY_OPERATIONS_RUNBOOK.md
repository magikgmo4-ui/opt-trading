---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_OPERATIONS_01
doc_type: runbook
status: ACTIVE
updated_at: 2026-05-18
---

# Desk Pro — Alert Delivery Operations Runbook

Pipeline cible :

```
webhook → perf → /desk/status → health → alert → dispatch → Telegram / webhook
                                                           ↘ JSONL fallback
```

---

## 1. Variables d'environnement

### Requises pour la livraison Telegram

| Variable | Rôle |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Token du bot Telegram |
| `TELEGRAM_CHAT_ID` | ID du chat destinataire |

### Requise pour la livraison webhook

| Variable | Rôle |
|---|---|
| `ALERT_WEBHOOK_URL` | URL cible (POST JSON) |

### Optionnelle

| Variable | Défaut | Rôle |
|---|---|---|
| `ALERT_COOLDOWN_SEC` | `300` | Silence entre deux alertes réelles |

### Lues au runtime

Les variables sont lues à chaque dispatch via `_env_str()` — pas au démarrage.
Un changement en cours de session est pris en compte au prochain dispatch.

### Chargement

```bash
source /opt/trading/scripts/load_env.sh
# lit /opt/trading/.env puis exporte TV_PERF_BASE_URL=http://127.0.0.1:8010
```

Ou via `.env` à la racine du repo (jamais commité).

### Vérification sans afficher les valeurs

```bash
# Confirme que les variables sont présentes (non vides) :
[[ -n "$TELEGRAM_BOT_TOKEN" ]] && echo "TELEGRAM_BOT_TOKEN: SET" || echo "TELEGRAM_BOT_TOKEN: ABSENT"
[[ -n "$TELEGRAM_CHAT_ID" ]]  && echo "TELEGRAM_CHAT_ID: SET"  || echo "TELEGRAM_CHAT_ID: ABSENT"
[[ -n "$ALERT_WEBHOOK_URL" ]] && echo "ALERT_WEBHOOK_URL: SET" || echo "ALERT_WEBHOOK_URL: ABSENT"
```

Ou via l'API (aucun secret exposé) :

```bash
curl -s http://127.0.0.1:8010/desk/status | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('telegram configured:', d.get('destinations', {}).get('telegram'))
print('webhook configured:', d.get('destinations', {}).get('webhook'))
"
```

---

## 2. Démarrage du serveur

```bash
cd /opt/trading

# Charger l'environnement
source scripts/load_env.sh

# Démarrer uvicorn (mode production)
PERF_DB_PATH=/opt/trading/data/db/perf.db \
nohup /opt/trading/venv/bin/python -m uvicorn modules.perf.app:app \
  --host 0.0.0.0 --port 8010 \
  > /opt/trading/tmp/uvicorn_8010.log 2>&1 &

echo "PID: $!"
```

Vérifier que le serveur est up :

```bash
curl -s http://127.0.0.1:8010/desk/health
```

Réponse attendue : `{"status": "up", ...}` ou `"degraded"`.

---

## 3. Smoke test — déclencher un test d'alerte manuel

```bash
curl -s -X POST http://127.0.0.1:8010/desk/alert/test | python3 -m json.tool
```

Réponse attendue (sans env) :

```json
{
  "ok": true,
  "alert": {
    "ts": "2026-05-18T09:30:00.000000Z",
    "status": "test",
    "message": "Desk Pro test alert — this is a smoke test"
  },
  "dispatch": [
    {"destination": "telegram", "status": "skipped", "reason": "not configured"},
    {"destination": "webhook",  "status": "skipped", "reason": "not configured"}
  ]
}
```

Réponse attendue (avec env) :

```json
{
  "dispatch": [
    {"destination": "telegram", "status": "delivered", "reason": "telegram"},
    {"destination": "webhook",  "status": "delivered", "reason": "webhook status=200"}
  ]
}
```

### Interprétation des statuts

| Statut | Signification |
|---|---|
| `delivered` | `sent=true` — la destination a accepté l'envoi |
| `skipped` | `reason="not configured"` — variable env absente |
| `failed` | `sent=false` + erreur réseau ou HTTP non-200 |

### Via l'UI

`http://127.0.0.1:8010/desk/ui` → bouton **Test Alert** dans la carte *Pipeline Status*.
Résultat affiché : `✓ telegram  ✓ webhook` (delivered) ou `– telegram  – webhook` (skipped).

**Note importante** : le smoke test ne touche pas `_alert_state` — aucun cooldown déclenché.
Le JSONL (`/opt/trading/tmp/desk_pro_alerts.jsonl`) n'est PAS écrit par le smoke test.

---

## 4. Fallback JSONL

Fichier : `/opt/trading/tmp/desk_pro_alerts.jsonl`

**Écrit uniquement lors d'une alerte réelle** (health_status `degraded` ou `down`), avant dispatch.
Indépendant des destinations — persiste même si Telegram/webhook absent.

```bash
# Lire les dernières alertes réelles :
tail -n 20 /opt/trading/tmp/desk_pro_alerts.jsonl 2>/dev/null || echo "Aucune alerte réelle"

# Via API :
curl -s http://127.0.0.1:8010/desk/alerts | python3 -m json.tool
```

---

## 5. Diagnostic — alerte non reçue

```
Étape 1 — Variables env configurées ?
  curl -s http://127.0.0.1:8010/desk/status
  → vérifier destinations.telegram et destinations.webhook

Étape 2 — Smoke test retourne delivered ?
  curl -s -X POST http://127.0.0.1:8010/desk/alert/test
  → si "skipped" : variable env manquante
  → si "failed"  : erreur réseau, voir reason

Étape 3 — État de santé réel ?
  curl -s http://127.0.0.1:8010/desk/health
  → si "up" : pas d'alerte réelle attendue (comportement normal)
  → si "degraded" ou "down" : alerte devrait se déclencher

Étape 4 — Cooldown actif ?
  curl -s http://127.0.0.1:8010/desk/status | python3 -c "
  import sys, json; d=json.load(sys.stdin)
  a = d.get('alert', {})
  if not a.get('triggered') and a.get('reason') == 'cooldown':
      print('COOLDOWN actif:', a.get('cooldown_remaining_sec'), 's restants')
  "

Étape 5 — Alerte écrite dans JSONL ?
  tail -5 /opt/trading/tmp/desk_pro_alerts.jsonl

Étape 6 — Log serveur
  tail -100 /opt/trading/tmp/uvicorn_8010.log
```

---

## 6. Garanties de non-fuite de secret

- Tokens et URLs lus via `_env_str()` — jamais loggués, jamais retournés dans les réponses API
- `GET /desk/status` : `destinations.telegram` et `destinations.webhook` sont des **booléens** uniquement
- `POST /desk/alert/test` : le payload `alert` ne contient pas de variable d'env
- Le JSONL ne contient que `{ts, status}` — pas de token, pas d'URL
- `secrets/` est gitignored et jamais commité

---

## 7. Commandes quotidiennes récapitulatives

```bash
# Santé du pipeline
curl -s http://127.0.0.1:8010/desk/health

# Statut complet (config destinations, cooldown, alertes récentes)
curl -s http://127.0.0.1:8010/desk/status | python3 -m json.tool

# Smoke test
curl -s -X POST http://127.0.0.1:8010/desk/alert/test | python3 -m json.tool

# Historique alertes réelles
curl -s http://127.0.0.1:8010/desk/alerts | python3 -m json.tool

# Log serveur
tail -50 /opt/trading/tmp/uvicorn_8010.log

# Tests unitaires
cd /opt/trading && python3 -m unittest discover -s tests -p "test_*.py"
```
