---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_REAL_DESTINATION_SMOKE_01
doc_type: closeout
repo: opt-trading
status: CLOSED / VALIDATED_SKIPPED
closed_at: 2026-05-18
---

# GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_REAL_DESTINATION_SMOKE_01 — CLOSEOUT

## 7_CANONICAL_STATE

```text
REAL_DESTINATION_SMOKE = CLOSED / VALIDATED_SKIPPED
CODE_CHANGES = NONE
UNITTEST = 107_PASS
SECRETS = NOT_INCLUDED
TELEGRAM_REAL_DELIVERY = SKIPPED (env absent)
WEBHOOK_EXTERNAL_DELIVERY = SKIPPED (env absent)
FALLBACK_JSONL = CONFIRMED (5 entries, smoke did not add)
```

## Statut env (2026-05-18)

| Variable | État | Source |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | **ABSENT** | env + .env |
| `TELEGRAM_CHAT_ID` | **ABSENT** | env + .env |
| `ALERT_WEBHOOK_URL` | **ABSENT** | env + .env (non documenté dans .env.example) |

Seul `TV_WEBHOOK_KEY` présent dans `.env` — concerne le webhook entrant, pas le dispatch d'alerte.
`secrets/` contient uniquement `google_oauth_client.json`.

## Résultats smoke

| Destination | Statut | Raison |
|---|---|---|
| `telegram` | `skipped` | not configured |
| `webhook` | `skipped` | not configured |

Comportement attendu et confirmé — aucune régression.

## Fallback JSONL

- `/opt/trading/tmp/desk_pro_alerts.jsonl` : **5 entrées** (inchangé après smoke)
- `POST /desk/alert/test` n'écrit pas dans JSONL — confirmé
- Toutes les entrées : `{ts, status: "down"}` — aucun credential

## Condition de déblocage

Pour valider la livraison réelle externe :

```bash
# Dans .env (jamais commité) :
TELEGRAM_BOT_TOKEN=<token>
TELEGRAM_CHAT_ID=<chat_id>
# et/ou
ALERT_WEBHOOK_URL=<url_externe>
```

Puis :

```bash
source /opt/trading/scripts/load_env.sh
# démarrer le serveur
curl -s -X POST http://127.0.0.1:8010/desk/alert/test | python3 -m json.tool
# attendre delivered (token non affiché, URL non affichée)
```

Ce GO peut être ré-ouvert dès que l'une des variables est disponible localement.

## RISKS

- À qualifier.
