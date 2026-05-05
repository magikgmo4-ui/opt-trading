---
doc_id: WEBHOOK_REVIEW_01_NEXT_GO
doc_type: next_go_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 50_NEXT_GO_DECISION — Webhook Review

## Verdict

**PASS** — Runtime webhook cartographie. 7 risques identifies.

## Finding critique

**Aucun signal TradingView recu depuis 33 jours.** Le webhook est UP (port 8000, process actif)
mais idle. Le ngrok tunnel est UP. Soit TradingView n'envoie plus de signaux, soit le stratum/URL
a change.

## Prochain GO recommande (P1)

### GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01

**Objectif**: Diagnostiquer pourquoi les signaux TradingView sont arretes.

**Actions**:
1. Verifier stratum ngrok (URL publique, connectivity)
2. Verifier config TradingView (webhook URL, alertes actives)
3. Tester POST /tv avec payload valide mais non-trading (dry-run)
4. Verifier log ngrok pour erreurs
5. Confirmer que le flux peut etre retabli

**Ne pas faire**:
- Ne pas modifier les engines de trading
- Ne pas fermer les trades ouverts
- Ne pas changer la config ngrok sans backup

## Backlog

| GO | Priorite | Description |
| --- | --- | --- |
| GO_SIGNAL_DIAG_01 | P1 | Diagnostic signal TradingView |
| GO_PERF_USER_FIX_01 | P2 | Passer tv-perf de root a ghost |
| GO_HEALTH_ENDPOINT_ADD_01 | P2 | Ajouter /health au webhook |
| GO_PERF_ENGINE_REVIEW_01 | P3 | Review engines COINM_SHORT/BITGET_SM_LITE |
