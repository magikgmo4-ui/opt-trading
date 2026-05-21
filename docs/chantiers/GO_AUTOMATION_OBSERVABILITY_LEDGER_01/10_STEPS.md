---
doc_id: GO_AUTOMATION_OBSERVABILITY_LEDGER_01_STEPS
doc_type: steps
go_id: GO_AUTOMATION_OBSERVABILITY_LEDGER_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
---

# 10_STEPS

1. Définir le schéma de l'event ledger (event_id, actor, action, surface, timestamp, status, payload, trace_id)
2. Définir le stockage (fichier JSONL, rotation, rétention)
3. Implémenter le writer unique
4. Produire 3 events sample (ex: read-only signal, draft patch, write gated)
5. Valider le replay/audit (rejouer les events, vérifier l'ordre)
6. Documenter la vue lecture LocalCMS

## Critères de succès

- Un event peut être écrit, lu, rejoué
- Le writer rejette les events invalides
- Le replay produit un état cohérent
