---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_NEXT_PHASE_DECISION_AFTER_DAILY_BASELINE_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #506  (Daily session baseline final closeout — merged)
  - PR #505  (Google Sheets controlled sync closeout — merged)
  - PR #504  (gspread + google-auth dependency pin — merged)
  - PR #493  (7-day dry-run observation — merged)
created_at: 2026-05-17
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_NEXT_PHASE_DECISION_AFTER_DAILY_BASELINE_01

## Objectif

Arbitrer la prochaine phase OpenClaw après validation complète de la
baseline daily session observability (11 PRs PASS, PR #506).

## Contexte établi

- Daily session observability baseline = PASS (PR #506)
- Timer systemd actif, trigger minuit quotidien
- TMUX 9 sessions stables, 3 critiques
- LocalCMS 4/4 endpoints opérationnels
- Journal quotidien JSON/CSV opérationnel
- Google Sheets controlled sync opérationnel via ADC
- Controlled-write PASS — run_id=20260516_013, row appended
- gspread==6.2.1, google-auth==2.53.0 figés dans requirements.txt
- 7/7 dry-run runs OK, P&L paper +438.03/run reproductible

## Options à arbitrer

### A. Observation continue 7-14 jours
Laisser le timer systemd actif sans modification. Accumuler des runs
quotidiens en dry-run. Révision hebdomadaire via LocalCMS `/journal`.

### B. Multi-signal paper-mode BTC/ETH/SOL
Étendre le pipeline à plusieurs tickers en parallèle, toujours
en paper-mode. Nécessite un GO dédié d'implémentation.

### C. Dashboard métriques LocalCMS
Construire une vue agrégée LocalCMS lisant `data/journal/daily/*.json`
et affichant P&L cumulé, win-rate, durée moyenne.

### D. Préparation live trading — doc-only, sans activation
Rédiger le protocole de passage paper → live : critères, garde-fous,
approbations requises. Aucune exécution réelle dans ce GO.

## Contraintes

- Ne pas activer live trading dans ce GO
- Ne pas activer auto-write Sheets
- Conserver controlled-write manuel uniquement
- Conserver rollback systemd
- No Bitget order

## RISKS

- À qualifier.
