---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PAPER_MODE_EXPANSION_DECISION_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #506  (Daily session baseline final closeout — merged)
  - PR #508  (Next phase decision A+C+D — merged)
  - PR #509  (LocalCMS metrics dashboard — merged)
  - PR #510  (Live trading readiness protocol — merged)
created_at: 2026-05-17
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PAPER_MODE_EXPANSION_DECISION_01

## Objectif

Arbitrer la prochaine phase paper-mode après baseline finale et
publication du protocole readiness (PR #510). Choisir entre
continuation mono-signal, expansion multi-signal, validation des
garde-fous, ou préparation GO_LIVE_ACTIVATION doc-only.

## Contexte établi

- Phase 0 PASS : 13 runs, 0 fail, P&L +5694.39, win_rate=100%
- Phase 1 (paper élargi) requiert ≥ 30 runs, ≥ 14 jours, kill switch testé,
  Telegram end-to-end testé
- Live activation : GO_LIVE_ACTIVATION_* séparé obligatoire
- Principe : en cas de doute = pas de live

## Options

### A. Observation continue mono-signal
Laisser le timer systemd tourner. Atteindre ≥ 30 runs.
Aucun changement.

### B. Paper élargi BTC/ETH/SOL
Étendre le pipeline à 2-3 tickers simultanément en paper-mode.
Nécessite un GO d'implémentation.

### C. Tester kill switch + Telegram avant tout multi-signal
Valider les garde-fous critiques (kill switch, Telegram alerting)
en dry-run avant d'élargir. GO de validation.

### D. Préparer GO_LIVE_ACTIVATION doc-only sans activation
Rédiger le template et les conditions d'entrée du futur GO
d'activation live. Aucune exécution.

## Contraintes

- no live trade
- no Bitget order
- no automatic Sheets write
- controlled-write manuel uniquement
- no secrets

## RISKS

- À qualifier.
