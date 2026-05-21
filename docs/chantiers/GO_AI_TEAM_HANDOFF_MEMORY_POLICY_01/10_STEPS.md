---
doc_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01_STEPS
doc_type: steps
go_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
---

# 10_STEPS

1. Définir le manager agent (rôle, modèle, limites, validation)
2. Définir les spécialistes (4 profils, chacun avec rôle et modèle)
3. Définir le handoff packet (champs, validation, rejet)
4. Définir le memory broker (stockage, clés, rotation, recovery)
5. Définir le task router (affectation par tâche, priorité, file)
6. Définir la validation humaine (gates par type d'action)
7. Tester un scénario multi-agent complet en dry-run
8. Documenter la preuve

## Critères de succès

- Un packet de handoff peut être émis, validé, routé vers un spécialiste
- Le memory broker stocke et restitue un contexte de session
- Le task router affecte une tâche au bon spécialiste
- Le scénario multi-agent produit un résultat auditable sans write
