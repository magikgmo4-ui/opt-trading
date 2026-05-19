---
doc_id: GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01_SAFETY_GATE
doc_type: safety_gate
repo: opt-trading
go_id: GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01
status: open
lifecycle_stage: specification
updated_at: 2026-05-06
links:
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/04_api_contract_openclaw_gateway.md
---

# 05_SAFETY_GATE — Botpress Operator

## Regles de blocage

### Blocage automatique (pas de bypass possible)

1. **Trade reel**: tout ordre avec `action=execute_trade` est bloque
2. **Push Git**: toute action `git push` est bloquee
3. **Modification production**: toute modif hors `student/Trading Labs` est bloquee
4. **Credentials**: toute demande de token, cles, `.env` est bloquee
5. **Boucle**: plus de 3 appels consecutifs sans intervention humaine = session terminee

### Blocage avec confirmation utilisateur

1. **Analyse multi-symbols** (>5 symbols): demande confirmation
2. **Backtest lourd**: avertit du temps d execution
3. **Export data**: confirme le format et la destination

### Liste blanche (no safety gate)

1. `screener` read-only scan market
2. `analysis` single symbol analyse
3. `journal` consultation historique
4. `status` cockpit GO statut
5. `help` commandes disponibles

## Journalisation

Chaque interaction est loggee dans Airtable (table `Botpress_Logs`) ou opt-trading journal:

```json
{
  "timestamp": "ISO-8601",
  "user_id": "telegram_id",
  "intent": "screener",
  "gateway_response": "ok",
  "safety_status": "passed|blocked|confirmed",
  "trace_id": "uuid",
  "duration_ms": 1234
}
```

## Smoke Test V1

1. Envoyer `/screener BTCUSDT` depuis Telegram
2. Botpress recoit, classifie `screener`
3. Safety gate: liste blanche → passe
4. Appel Gateway → student/Trading Labs
5. Reponse formatee → Telegram
6. Log dans journal

Resultat attendu: scan market returned, pas de trade, pas de push Git.

## Verdict

**PASS** si smoke V1 reussi sans bypass safety gate.
**FAIL** si trade reel, push Git ou modif production non autorise.
