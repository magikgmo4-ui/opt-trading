---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_STRATEGY_BACKFILL_DISCOVERY_01
doc_type: next_go_decision
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-18
---

# 50_NEXT_GO_DECISION

## Décision prochain GO

---

## 1_RECOMMANDATION

Prochain GO recommandé après ce backfill discovery :

```text
GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_COINM_SHORT_REGULARIZATION_01
```

Justification :

```text
COINM_SHORT a le plus haut degré de maturité technique :
- Engine enum existant dans strategy_logic.py
- Logique de décision dédiée (lignes 125, 198)
- Entrée dans le registry engines
- Utilisé en paper mode
```

---

## 2_ORDRE_RECOMMANDÉ

```text
1. COINM_SHORT      → regularization + registry (P0)
2. USDTM_LONG       → regularization + registry (P1)
3. GOLD_CFD_LONG    → regularization + registry (P2)
4. range_strategy_v1 → reprise cadrage + registry (P3)
5. btc_coinm_accumulation → validation concept + registry (P4)
6. modules/strategy/ physical consolidation (après stabilisation)
```

---

## 3_NE_PAS_FAIRE_MAINTENANT

```text
- Ne pas créer modules/strategy/ maintenant
- Ne pas backfiller automatiquement la registry
- Ne pas refactor les engines
- Ne pas modifier le comportement runtime
```

## RISKS

- À qualifier.
