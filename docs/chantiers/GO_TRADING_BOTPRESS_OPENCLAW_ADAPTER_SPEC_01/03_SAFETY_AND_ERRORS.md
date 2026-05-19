---
doc_id: GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01_SAFETY
doc_type: safety_spec
repo: opt-trading
go_id: GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01
updated_at: 2026-05-06
links:
  - docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01/01_ADAPTER_CONTRACT.md
---

# 03_SAFETY_AND_ERRORS — Adapter Botpress ↔ OpenClaw

## Safety Gate (dans l adapter)

L adapter est le point de blocage. Safety gate s execute avant tout appel OpenClaw.

### Blocage permanent

| Intent | Action | Reponse |
| --- | --- | --- |
| `execute_trade` | Bloque | "Trading reel non autorise V1" |
| `git_push` | Bloque | "Push Git automatique non autorise" |
| `modify_production` | Bloque | "Modification production non autorisee" |
| `expose_secret` | Bloque | "Donnee sensible bloquee" |

### Liste blanche (passe direct)

| Intent | Condition |
| --- | --- |
| `screener` | Read-only market scan |
| `analysis` | Read-only single symbol |
| `journal` | Read-only query |
| `status` | Read-only cockpit |
| `help` | Static commands |

### Confirmation requise

| Intent | Condition | Message |
| --- | --- | --- |
| `backtest_run` | > 5 symbols | "Backtest sur >5 symbols, confirme?" |
| `multi_scan` | > 5 symbols | "Scan multi (>5), confirme?" |

## Error Handling

### Gateway errors

| Code | Message Adapter | Log |
| --- | --- | --- |
| 4xx | "Requete invalide, verifie les parametres" | WARN |
| 5xx | "Gateway indisponible, reessaie plus tard" | ERROR |
| timeout | "Delai depasse, analyse en cours..." | WARN |
| connection_refused | "Gateway inaccessible" | ERROR |

### Botpress errors

| Scenario | Action |
| --- | --- |
| Intent inconnu | Repondre "Intent non reconnu. /help pour la liste" |
| Payload invalide | Repondre "Format invalide. /help pour exemples" |
| Rate limit | Repondre "Trop de requetes, attend 30s" |

## Rate Limiting

- Max 10 requetes / minute / user
- Max 3 appels consecutifs sans reponse utilisateur = session terminee
- Cooldown: 5s entre 2 requetes

## Circuit Breaker

Si Gateway echoue > 3 fois en 60s:
- Adapter passe en mode "degrades"
- Repond "Gateway en maintenance, reessaie dans 2 minutes"
- Log ALERT

## Smoke Test minimal

1. POST `/api/v1/botpress/intent` avec intent `help`
2. Verifier reponse OK avec texte aide
3. POST avec intent `execute_trade`
4. Verifier reponse BLOCKED
5. POST avec intent `screener` (si Gateway UP)
6. Verifier reponse OK avec data

Verdict smoke: PASS si 1-2-3-4 OK (5-6 depend du Gateway).
