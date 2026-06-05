# 40_EXECUTION_RUNBOOK_DRAFT

1. Vérifier la configuration (`.env` local, non commité).
2. Lancer le service en mode simulation (`RUNNER_MODE=PAPER`).
3. Envoyer un signal de test (`/tv`) depuis TradingView (ou simuler le webhook).
4. Surveiller Telegram (notifications `PAPER_ORDER_SIMULATED`).
5. Vérifier `ledger_paper.json`.
6. Vérifier l'absence de logs d'erreur de connexion API réelle.

## RISKS

- À qualifier.
