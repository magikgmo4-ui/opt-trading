---
doc_id: GO_HITL_APPROVAL_GATES_01_STEPS
doc_type: steps
go_id: GO_HITL_APPROVAL_GATES_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: passed_with_evidence
---

# 10_STEPS

1. Définir le proposal packet (action_id, actor, surface, justification, risque, dry_run)
2. Définir l'approval packet (proposal_id, approver, decision, signature, conditions)
3. Définir l'execution packet (approval_id, commande, rollback, scope)
4. Définir la verification packet (execution_id, status, preuve, logs)
5. Définir les approver roles (humain, team_ai_manager, safety_gate)
6. Définir la politique de dual confirm (actions L6+)
7. Tester un write-gated scenario complet

## Critères de succès

- Un packet proposal peut être créé, soumis, approuvé/rejeté
- Un packet approuvé peut être exécuté avec rollback
- La vérification produit un résultat lisible
- Le dual confirm bloque les actions sans double signature
