---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_LIVE_TRADING_READINESS_DOC_ONLY_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #506  (Daily session baseline final closeout — merged)
  - PR #508  (Next phase decision — Option D sélectionnée)
  - PR #509  (LocalCMS metrics dashboard — merged)
created_at: 2026-05-17
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_LIVE_TRADING_READINESS_DOC_ONLY_01

## Objectif

Documenter le protocole de passage dry-run → paper élargi → live trading.
Aucune activation dans ce GO. Aucun ordre Bitget. Aucun secret committé.

## Livrables

1. `01_READINESS_CRITERIA.md` — critères et conditions d'entrée par phase
2. `02_SURFACE_AUDIT.md` — audit des surfaces à valider avant live
3. `03_CHECKLISTS.md` — checklists opérationnelles (risk, kill switch, keys, monitoring)
4. `04_REFUSAL_CRITERIA.md` — critères de refus et conditions de blocage

## Contraintes absolues

- DOC-ONLY — aucune exécution, aucune activation
- NO live trade
- NO Bitget order
- NO automatic Sheets write
- NO secrets in repo or logs
- La décision de passer en live requiert un GO séparé avec approbation explicite

## RISKS

- À qualifier.
