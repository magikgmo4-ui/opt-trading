---
doc_id: GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01_STEPS
doc_type: steps
go_id: GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
---

# 10_STEPS

1. Définir le signal schema (id, source, type, timestamp, payload, confiance)
2. Documenter les source adapters (TradingView webhook, Telegram, collecteurs data)
3. Définir les règles de recroisement (combien de sources pour valider)
4. Définir les règles d'invalidation (hors plage, malformé, conflicting)
5. Implémenter le dry-run guard (bloquer toute émission d'ordre live)
6. Créer le journal des signaux (log horodaté de chaque signal)
7. Définir les backtest stats (win rate, drawdown, nombre de signaux)
8. Documenter la preuve

## Critères de succès

- Un signal peut être reçu, validé, recroisé, journalisé
- Aucun ordre live ne peut être émis via la chaîne
- Les backtest stats sont calculables
