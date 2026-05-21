---
doc_id: GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01_STEPS
doc_type: steps
go_id: GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: passed_with_evidence
---

# 10_STEPS

1. Créer le template `APP_BRIDGE_CONTRACT`
2. Remplir contrat Airtable
3. Remplir contrat ClickUp
4. Remplir contrat Botpress
5. Remplir contrat Google Sheets
6. Remplir contrat Telegram
7. Remplir contrat Gmail
8. Remplir contrat Calendar
9. Remplir contrat Drive
10. Remplir contrat Figma
11. Remplir contrat LocalCMS
12. Valider les actions interdites
13. Relier chaque contrat à la matrice de capacité

## Template APP_BRIDGE_CONTRACT

- app_id
- purpose
- source_of_truth_rank
- allowed_reads
- allowed_writes
- forbidden_actions
- required_env_vars
- dry_run_mode
- approval_gate
- audit_log
- rollback_or_compensating_action
- evidence_ref

## Critères de succès

- Chaque app a un contrat signé (documenté)
- Toutes les actions interdites sont listées
- Chaque contrat référence les lignes correspondantes dans la capability matrix
