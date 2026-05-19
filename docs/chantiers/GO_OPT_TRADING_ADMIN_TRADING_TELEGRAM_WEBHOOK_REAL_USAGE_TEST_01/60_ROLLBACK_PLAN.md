---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01_60_ROLLBACK
doc_type: chantier/rollback
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01
machine: admin-trading
status: active
lifecycle_stage: real_usage_test
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01/30_REAL_USAGE_TEST_PLAN.md
---

# 60_ROLLBACK_PLAN — Plan de rollback

## Objet

Definir la procedure de retour a l'etat nominal apres le test, et les actions
correctives en cas d'anomalie.

## Principe

Ce GO est doc-only. Aucune modification de code ou de configuration n'est
apportee au repo. Le test lui-meme est non-invasif :
- `engine: "TV_TEST"` ne genere aucun trade
- Les evenements dans `events.jsonl` sont append-only (non destructifs)
- Les logs systemd sont en rotation automatique

## Rollback standard (post-test normal)

Aucun rollback necessaire. Actions de cloture :

```bash
# 1. Verifier que le service est toujours operationnel
systemctl status tv-webhook.service --no-pager

# 2. Optionnel : purger les evenements de test si souhaité
# (non recommande : les evenements sont des preuves utiles)
# python3 -c "
# import json
# lines = []
# with open('state/events.jsonl') as f:
#     for line in f:
#         e = json.loads(line)
#         if 'GO_TEST' not in e.get('reason', ''):
#             lines.append(line)
# open('state/events.jsonl', 'w').writelines(lines)
# "

# 3. Verifier l'etat final
bash scripts/admin_trading/runtime_guard.sh

# 4. Checker le dashboard
curl -sS http://127.0.0.1:8000/dash > /dev/null && echo "dash OK"
```

## Rollback d'urgence (anomalie pendant le test)

### Scenario A : Le service webhook ne repond plus (500 / crash)

```bash
# 1. Verifier les logs
journalctl -u tv-webhook.service --since "5 min ago" --no-pager -n 50

# 2. Redemarrer le service
sudo systemctl restart tv-webhook.service

# 3. Verifier la sante
sleep 3
curl -sS http://127.0.0.1:8000/api/state

# 4. Si toujours ko, restaurer le binaire/deploy precedent
# (depend du mecanisme de deploiement en place)
```

### Scenario B : Telegram ne recoit pas (bot bloque / token expire)

```bash
# 1. Verifier la config
systemctl show tv-webhook.service -p Environment | tr ' ' '\n' | grep TELEGRAM

# 2. Tester le bot Telegram directement
python3 -c "
import os, requests
token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
r = requests.post(f'https://api.telegram.org/bot{token}/getMe')
print(r.json())
"

# 3. Si KO, desactiver TELEGRAM_ENABLED le temps du diagnostic
# export TELEGRAM_ENABLED=0
# sudo systemctl restart tv-webhook.service
```

### Scenario C : Apparition d'un trade dans perf ledger par erreur

```bash
# 1. Identifier le trade
curl -sS http://127.0.0.1:8010/perf/open | python3 -m json.tool

# 2. Verifier l'engine et le symbol
# Si engine == TV_TEST -> anomalie (ne devrait pas arriver via le code)
# Si engine == COINM_SHORT/USDTM_LONG -> alerte critique

# 3. Arreter le service webhook
sudo systemctl stop tv-webhook.service

# 4. Fermer manuellement le trade si possible
# (procedure dependante du broker/perf system)

# 5. Diagnostic complet avant redemarrage
```

### Scenario D : Service systemd instable apres le test

```bash
# 1. Logs detailles
journalctl -u tv-webhook.service -u ngrok-tv.service -u tv-perf.service --since "10 min ago" --no-pager

# 2. Redemarrer les services dans l'ordre
sudo systemctl restart tv-perf.service
sleep 2
sudo systemctl restart tv-webhook.service
sleep 2
sudo systemctl restart ngrok-tv.service

# 3. Verifier
bash scripts/admin_trading/runtime_guard.sh
```

## Cleanup post-test

Aucune action de cleanup obligatoire. Recommandations :

1. **Evenements JSONL** : conserver comme preuve de test. Les evenements
   `TV_TEST` sont inoffensifs et ne declenchent aucun traitement aval.

2. **Logs systemd** : la rotation automatique les effacera progressivement.
   Conserver un extrait dans `~/opt-trading-logs/` si necessaire.

3. **Branche Git** : merger dans `sot/mainline` apres closeout documente.
   La branche est doc-only, le merge n'affecte pas le runtime.

4. **Dashboard /metrics** : les compteurs `buy`/`sell` incrementes par le test
   peuvent etre reinitialises via `POST /api/reset_lock` (admin key requise).

## Verification post-rollback

```bash
# Checklist finale
echo "=== Post-test / rollback verification ==="

# Service actif
systemctl is-active tv-webhook.service && echo "PASS: service active" || echo "FAIL: service not active"

# Dashboard repond
curl -sS -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/api/state | grep -q 200 && echo "PASS: api/state 200" || echo "FAIL: api/state"

# Runtime guard
bash scripts/admin_trading/runtime_guard.sh
```

## Notes

- Le test est concu pour etre **non-invasif par construction** (engine `TV_TEST`).
- Le rollback le plus lourd serait un `systemctl restart tv-webhook.service`.
- Aucune restauration de base de donnees ou de state n'est necessaire.
- Les evenements de test dans `events.jsonl` sont append-only et non bloquants.
