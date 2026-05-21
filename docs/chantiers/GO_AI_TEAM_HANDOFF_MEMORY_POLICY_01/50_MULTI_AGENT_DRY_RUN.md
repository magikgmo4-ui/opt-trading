---
doc_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01_DRY_RUN
doc_type: dry_run_scenario
go_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01
status: draft
---

# 50_MULTI_AGENT_DRY_RUN

## Scenario

Lecture d'un inventaire, analyse d'un gap, proposition de correctif, passage par le manager.

### Steps

1. **specialist_volume** reçoit `READ_INVENTORY` sur un scope défini
   → lit les fichiers, produit un inventaire structuré
2. **specialist_volume** handoff vers **manager** avec completion packet
3. **manager** analyse l'inventaire, identifie un gap
4. **manager** handoff vers **specialist_reasoning** avec `PATCH_DRAFT`
5. **specialist_reasoning** analyse, produit un patch draft
6. **specialist_reasoning** handoff vers **manager** avec completion
7. **manager** valide le patch, soit l'approuve, soit le rejette, soit escalade à l'humain

### Résultat attendu

```text
1. READ_INVENTORY → specialist_volume → PASS (inventaire produit)
2. Handoff → manager → PASS (réception)
3. Analyse gap → manager → PASS (gap identifié)
4. Handoff → specialist_reasoning → PASS (réception)
5. PATCH_DRAFT → specialist_reasoning → PASS (draft produit)
6. Handoff → manager → PASS (réception)
7. Validation → manager → PASS (draft approuvé ou rejeté)
```

### Preuve

- Tous les handoffs sont loggés dans le ledger
- Aucun write n'est effectué (dry-run)
- Le résultat complet est traçable
