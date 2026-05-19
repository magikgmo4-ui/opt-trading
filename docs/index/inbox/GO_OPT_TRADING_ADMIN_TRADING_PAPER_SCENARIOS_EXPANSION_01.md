---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_SCENARIOS_EXPANSION_01_INBOX
doc_type: index/inbox_entry
repo: opt-trading
machine: admin-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_SCENARIOS_EXPANSION_01
status: pass_all_scenarios
scope: paper_scenarios_expansion
---

# GO_OPT_TRADING_ADMIN_TRADING_PAPER_SCENARIOS_EXPANSION_01

Scénarios paper additionnels exécutés sur admin-trading.

Résultat: 5/5 scénarios PASS.

Scénarios testés:
- A. PAPER_SELL_VALID: SELL paper accepté, position ouverte
- B1. PAPER_INVALID_PAYLOAD: rejet HTTP 400 (champs manquants)
- B2. PAPER_INVALID_SIGNAL: rejet HTTP 400 (signal invalide)
- C. PAPER_GUARD_FAILURE: blocage HTTP 409 (engine agressif)
- D. PAPER_LEDGER_REGRESSION: ledger_paper uniquement, pas de ledger_live

Invariants maintenus:
- Aucun ordre réel
- Aucun live trading
- Aucun secret exposé
- Guards ok:true avant/après
- Positions nettoyées

Prochaine suite: validation production ou scénarios supplémentaires.
