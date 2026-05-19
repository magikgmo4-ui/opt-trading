---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01_30_TEST_PLAN
doc_type: chantier/test_plan
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01
machine: admin-trading
status: active
lifecycle_stage: real_usage_test
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01/10_ADMIN_TRADING_PRECHECK.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01/20_TELEGRAM_WEBHOOK_SCOPE.md
---

# 30_REAL_USAGE_TEST_PLAN — Plan de test en usage reel controle

## Objet

Decrire la procedure de test pas-a-pas a executer sur la machine admin-trading
pour valider le flux webhook → Telegram en conditions reelles, sans aucun trade.

## Pre-requis

- [ ] Precheck 10_ADMIN_TRADING_PRECHECK.md complete (tous les checks PASS)
- [ ] Machine admin-trading accessible (SSH ou console locale)
- [ ] `tv-webhook.service` actif et en ecoute sur `127.0.0.1:8000`
- [ ] `TELEGRAM_BOT_TOKEN` et `TELEGRAM_CHAT_ID` configures dans l'environnement
- [ ] `TELEGRAM_ENABLED=1` dans l'environnement du service
- [ ] Aucun autre test concurrent sur la machine
- [ ] Un canal Telegram accessible pour verifier la reception

## Phase 1 — Verification pre-test

### Etape 1.1 : Verifier l'etat pre-test

```bash
# Etat des services
systemctl status tv-webhook.service --no-pager -l

# Logs recents (derniere minute)
journalctl -u tv-webhook.service --since "1 min ago" --no-pager

# Endpoint dashboard accessible
curl -sS http://127.0.0.1:8000/api/state | python3 -m json.tool
```

- [ ] Service actif
- [ ] Pas d'erreurs recentes dans les logs
- [ ] Dashboard retourne un JSON valide

### Etape 1.2 : Capturer l'etat initial (baseline)

```bash
# Snapshot des evenements avant le test
wc -l state/events.jsonl 2>/dev/null || echo "no events yet"

# Dernier evenement
tail -1 state/events.jsonl 2>/dev/null | python3 -m json.tool || echo "no events"
```

- [ ] Nombre d'evenements avant test note
- [ ] Dernier evenement capture

## Phase 2 — Test localhost (sans Telegram)

Si `TV_WEBHOOK_KEY` n'est pas configure, le serveur accepte les requetes
depuis localhost seulement. Premier test sans Telegram pour valider la
reception pure.

### Etape 2.1 : Envoyer un payload test minimal

```bash
curl -sS -X POST http://127.0.0.1:8000/tv \
  -H "Content-Type: application/json" \
  -d '{
    "engine": "TV_TEST",
    "signal": "BUY",
    "symbol": "TEST/USDT",
    "tf": "1m",
    "price": 100.0,
    "tp": 110.0,
    "sl": 95.0,
    "reason": "GO_TEST_01_LOCALHOST_NO_TELEGRAM"
  }' | python3 -m json.tool
```

Reponse attendue : `{"ok": true}`

- [ ] Code HTTP 200
- [ ] Body : `{"ok": true}`
- [ ] Pas d'erreur dans la reponse

### Etape 2.2 : Verifier l'evenement enregistre

```bash
tail -1 state/events.jsonl | python3 -m json.tool
```

Verifications :
- [ ] `engine: "TV_TEST"`
- [ ] `signal: "BUY"`
- [ ] `symbol: "TEST/USDT"`
- [ ] `reason: "GO_TEST_01_LOCALHOST_NO_TELEGRAM"`
- [ ] `_ts` timestamp present
- [ ] `_ip: "127.0.0.1"`

### Etape 2.3 : Verifier les logs du service

```bash
journalctl -u tv-webhook.service --since "1 min ago" --no-pager | grep -i "TV_TEST"
```

- [ ] Trace de traitement dans les logs
- [ ] Pas d'HTTPError
- [ ] Pas de 400/403/409/500

## Phase 3 — Test avec Telegram active

### Etape 3.1 : Activer Telegram (si pas deja fait)

Verifier que `TELEGRAM_ENABLED=1` est bien dans l'environnement du service :

```bash
# Si le service est gere par systemd avec un fichier d'environnement
systemctl show tv-webhook.service -p Environment

# Ou si gere par .env
cat .env 2>/dev/null | grep TELEGRAM
```

- [ ] `TELEGRAM_ENABLED=1`
- [ ] `TELEGRAM_BOT_TOKEN` set (valeur non affichee)
- [ ] `TELEGRAM_CHAT_ID` set (valeur non affichee)

### Etape 3.2 : Envoyer un payload test avec notification Telegram

```bash
curl -sS -X POST http://127.0.0.1:8000/tv \
  -H "Content-Type: application/json" \
  -d '{
    "engine": "TV_TEST",
    "signal": "BUY",
    "symbol": "TEST/USDT",
    "tf": "1m",
    "price": 100.0,
    "tp": 110.0,
    "sl": 95.0,
    "reason": "GO_TEST_02_WITH_TELEGRAM"
  }' | python3 -m json.tool
```

- [ ] Code HTTP 200
- [ ] Body : `{"ok": true}`

### Etape 3.3 : Verifier reception Telegram

Ouvrir le canal/cible Telegram et verifier :

- [ ] Message recu dans le chat Telegram
- [ ] Contenu du message contient `BUY TEST/USDT 1m`
- [ ] Contenu du message contient `engine: TV_TEST`
- [ ] Contenu du message contient `reason: GO_TEST_02_WITH_TELEGRAM`
- [ ] Contenu du message contient `price: 100.0 | tp: 110.0 | sl: 95.0`
- [ ] Pas d'information sensible (pas de token, pas de cle)

### Etape 3.4 : Verifier les logs post-Telegram

```bash
journalctl -u tv-webhook.service --since "1 min ago" --no-pager
```

- [ ] Trace de l'envoi Telegram reussi
- [ ] Pas d'erreur `RuntimeError: Telegram env vars not set`
- [ ] Pas d'HTTPError vers api.telegram.org

## Phase 4 — Test de robustesse

### Etape 4.1 : Payload invalide (signal incorrect)

```bash
curl -sS -X POST http://127.0.0.1:8000/tv \
  -H "Content-Type: application/json" \
  -d '{"engine": "TV_TEST", "signal": "INVALID", "symbol": "TEST", "tf": "1m", "price": 100.0, "sl": 95.0}'
```

- [ ] Code HTTP 400
- [ ] Message d'erreur : `signal must be BUY or SELL`
- [ ] Aucun evenement ajoute dans `state/events.jsonl`
- [ ] Aucun message Telegram envoye

### Etape 4.2 : Payload invalide (engine inexistant)

```bash
curl -sS -X POST http://127.0.0.1:8000/tv \
  -H "Content-Type: application/json" \
  -d '{"engine": "FAKE_ENGINE_XYZ", "signal": "BUY", "symbol": "TEST", "tf": "1m", "price": 100.0, "sl": 95.0}'
```

- [ ] Code HTTP 400
- [ ] Message d'erreur contient `not registered`
- [ ] Aucun evenement ajoute
- [ ] Aucun message Telegram

### Etape 4.3 : Payload sans price/sl valides

```bash
curl -sS -X POST http://127.0.0.1:8000/tv \
  -H "Content-Type: application/json" \
  -d '{"engine": "TV_TEST", "signal": "BUY", "symbol": "TEST", "tf": "1m"}'
```

- [ ] Code HTTP 400
- [ ] Message d'erreur : `Missing/invalid price or sl for risk sizing`
- [ ] Aucun evenement ajoute
- [ ] Aucun message Telegram

### Etape 4.4 : Rejeu rapide (meme payload)

```bash
for i in 1 2 3; do
  echo "--- Request $i ---"
  curl -sS -X POST http://127.0.0.1:8000/tv \
    -H "Content-Type: application/json" \
    -d '{"engine": "TV_TEST", "signal": "BUY", "symbol": "TEST/USDT", "tf": "1m", "price": 100.0, "sl": 95.0, "reason": "REJEU_'"$i"'"}'
  echo
done
```

- [ ] Les 3 requetes retournent `{"ok": true}`
- [ ] Les 3 evenements sont enregistres dans `state/events.jsonl`
- [ ] Les 3 messages sont envoyes sur Telegram

## Phase 5 — Verification post-test

### Etape 5.1 : Compter les evenements

```bash
wc -l state/events.jsonl
```

- [ ] Difference entre avant et apres correspond au nombre de tests reussis

### Etape 5.2 : Verifier le dashboard

```bash
curl -sS http://127.0.0.1:8000/api/events?limit=20 | python3 -m json.tool
```

- [ ] Les evenements de test apparaissent
- [ ] Tous les engines sont `TV_TEST`

### Etape 5.3 : Verifier les metriques

```bash
curl -sS http://127.0.0.1:8000/api/metrics | python3 -m json.tool
```

- [ ] Compteurs `buy` increments
- [ ] `events_per_min` reflete l'activite de test

### Etape 5.4 : Verifier qu'aucun trade reel n'a ete initie

```bash
# Verifier perf ledger (doit etre vide pour TV_TEST)
curl -sS http://127.0.0.1:8010/perf/open 2>/dev/null | python3 -m json.tool || echo "perf service non accessible (non bloquant)"
```

- [ ] Aucun trade OPEN avec engine TV_TEST dans le perf ledger
- [ ] Ou perf service non accessible (acceptable si pas deploye)

## Tableau de resultats

| Phase | Etape | Description | Resultat |
| --- | --- | --- | --- |
| 1 | 1.1 | Etat pre-test | |
| 1 | 1.2 | Baseline events | |
| 2 | 2.1 | Payload test localhost | |
| 2 | 2.2 | Evenement enregistre | |
| 2 | 2.3 | Logs service | |
| 3 | 3.1 | Telegram actif | |
| 3 | 3.2 | Payload avec Telegram | |
| 3 | 3.3 | Reception Telegram | |
| 3 | 3.4 | Logs post-Telegram | |
| 4 | 4.1 | Payload invalide (signal) | |
| 4 | 4.2 | Payload invalide (engine) | |
| 4 | 4.3 | Payload sans price/sl | |
| 4 | 4.4 | Rejeu rapide x3 | |
| 5 | 5.1 | Comptage evenements | |
| 5 | 5.2 | Dashboard events | |
| 5 | 5.3 | Metriques | |
| 5 | 5.4 | Aucun trade reel | |

## Criteres de PASS/FAIL

**PASS** si :
- Tous les payloads valides retournent `{"ok": true}`
- Tous les payloads invalides retournent 400 avec message approprie
- Les evenements sont correctement enregistres dans `events.jsonl`
- Les messages Telegram sont bien recus
- Aucun trade reel initie (engine == TV_TEST → pas de perf ledger)
- Aucune erreur 5xx dans les logs

**FAIL** si :
- Un payload valide retourne autre chose que `{"ok": true}`
- Un payload invalide ne retourne pas 400
- Telegram non recu alors que TELEGRAM_ENABLED=1
- Apparition d'un trade dans le perf ledger
- Erreur 5xx dans les logs
