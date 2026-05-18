---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_ENV_VALIDATION_01
doc_type: closeout
repo: opt-trading
status: CLOSED / VALIDATED
closed_at: 2026-05-18
pr: 560
---

# GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_ENV_VALIDATION_01 — CLOSEOUT

## 7_CANONICAL_STATE

```text
ALERT_DELIVERY_ENV_VALIDATION = CLOSED / VALIDATED
CODE_CHANGES = NONE
UNITTEST = 107_PASS
SECRETS = NOT_INCLUDED
ENV_STATUS = PARTIAL (webhook testable, Telegram no local credentials)
```

## 13_ESTABLISHED

| Élément | État |
|---|---|
| Smoke sans env | `skipped` × 2 — confirmé |
| Smoke avec `ALERT_WEBHOOK_URL` local | webhook `delivered` (status=200), telegram `skipped` |
| Fallback JSONL | `/opt/trading/tmp/desk_pro_alerts.jsonl` — 5 entrées réelles |
| Smoke ne touche pas JSONL | confirmé — entrées JSONL = alertes réelles uniquement |
| Cooldown cycle complet | `triggered → cooldown (269s)` — confirmé |
| Non-fuite secret | destinations = bool, JSONL = `{ts, status}`, payload smoke sans token |
| Tests | 107/107 PASS |

## Résultats détaillés

### Statut env

| Variable | État |
|---|---|
| `TELEGRAM_BOT_TOKEN` | ABSENT |
| `TELEGRAM_CHAT_ID` | ABSENT |
| `ALERT_WEBHOOK_URL` | absent en prod — testé avec récepteur local `127.0.0.1:9999` |

### Smoke — résultats par scénario

| Scénario | telegram | webhook |
|---|---|---|
| Env absent | `skipped` (not configured) | `skipped` (not configured) |
| `ALERT_WEBHOOK_URL=http://127.0.0.1:9999/hook` | `skipped` | `delivered` (status=200) |

### Fallback JSONL

- Contenu : `{ts, status}` uniquement — aucun credential
- Persistant entre redémarrages
- Non écrit par `POST /desk/alert/test`

### Nuance critique — cooldown in-memory

`_alert_state` est un dict process-local. Il se reset au redémarrage du serveur.
Le JSONL persiste ; le cooldown ne persiste pas.

**Comportement attendu** : à chaque démarrage en mode mock (webhook port 8000 absent),
le premier appel à `/desk/status` déclenche une alerte et écrit dans le JSONL.
À partir du 2e appel : `reason: cooldown` actif pendant `ALERT_COOLDOWN_SEC` (défaut 300s).

Ce comportement est non bloquant pour l'usage opérationnel réel
(le serveur reste up en continu — le reset ne se produit qu'au redémarrage).

## Gap identifié (non bloquant)

Si la persistance du cooldown entre redémarrages est requise :
persister `_alert_state` dans un fichier JSON au côté du JSONL.
Non urgent — à traiter dans un GO dédié si besoin opérationnel confirmé.
