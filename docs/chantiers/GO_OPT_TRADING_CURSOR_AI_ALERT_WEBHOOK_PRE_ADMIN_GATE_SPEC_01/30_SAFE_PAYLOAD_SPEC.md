---
doc_id: GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01_30_SAFE_PAYLOAD_SPEC
doc_type: chantier/safe_payload_spec
repo: opt-trading
machine: cursor-ai
status: active
links:
  - modules/tradingview_observer/templates/alert_webhook_template_v1.json
---

# 30_SAFE_PAYLOAD_SPEC — Spec de payload safe alert_webhook

## Objectif

Definir ce qu'est un payload safe (autorisé en documentation cursor-ai) vs un payload dangereux (interdit sans admin-trading ouvert).

## Structure payload safe

Payload type pour documentation et spec uniquement :

```json
{
  "schema": "opt_trading_tradingview_alert_template_v1",
  "mode": "test_only",
  "signal": "TEST_ONLY",
  "trade_allowed": false,
  "admin_trading_runtime": false,
  "ticker": "{{ticker}}",
  "exchange": "{{exchange}}",
  "interval": "{{interval}}",
  "price": "{{close}}",
  "volume": "{{volume}}",
  "time": "{{time}}",
  "action": "alert",
  "message": "TEST_ONLY — no real alert"
}
```

## Champs obligatoires pour payload safe

| Champ | Valeur obligatoire | Raison |
| --- | --- | --- |
| `trade_allowed` | `false` | Bloque toute action de trading |
| `admin_trading_runtime` | `false` | Bloque toute connexion runtime admin-trading |
| `mode` | `test_only` | Indique mode test/documentation |
| `signal` | `TEST_ONLY` | Signal non executable |

## Champs interdits dans un payload cursor-ai

| Champ | Raison |
| --- | --- |
| URL webhook reelle | Pointe vers un endpoint de production |
| Token d'authentification | Secret |
| Cle API | Secret |
| `trade_allowed: true` | Ouvre le trading |
| `admin_trading_runtime: true` | Ouvre la connexion runtime |
| Coordonnees bancaires | Donnee sensible |
| IP reelle | Vie privee / securite |
| `signal` non-TEST_ONLY | Risque d'execution reelle |

## Regle anti-secret

```text
Aucun payload dans docs/ ou bundles/ ne doit contenir :
- une URL webhook reelle
- un token
- une cle API
- un mot de passe
- une donnee financiere reelle
- une IP non anonymisee
```

## Exemple anonymise accepte

```json
{
  "webhook_url": "http://127.0.0.1:9999/tv-test",
  "note": "localhost mock only — no production endpoint"
}
```

## Exemple refuse

```json
{
  "webhook_url": "https://real-server.com/webhook",
  "token": "sk-abc123..."
}
```
→ Ce payload ne doit jamais apparaitre dans le repo.

## Placer les payloads safe

- `docs/chantiers/` : OK pour spec et documentation.
- `bundles/` : OK pour templates et exemples.
- `modules/` : OK si flags securite actifs et `mode: test_only`.
- Hors repo : toute instance avec donnees reelles.
