---
doc_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01_VALIDATION_GATES
doc_type: validation_gates
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01
status: draft_for_review
lifecycle_stage: child_gates
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01
topic_keys:
  - opt-trading
  - deepseek
  - validation-gates
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01/04_VALIDATION_GATES.md
point_de_reprise: "Gates de validation avant toute implementation DeepSeek."
updated_at: 2026-05-13
links:
  - docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01/02_RUNTIME_CONSOLIDATION_PLAN.md
---

# 04_VALIDATION_GATES

## 1_GATES AVANT IMPLEMENTATION

```text
G1. audit complet des callers de deepseek_response et deepseek_thinking
G2. inventaire des scripts effectivement presents dans scripts/student/
G3. verification que deepseek_hub patches sont appliques sur toutes les machines
G4. test du workflow post_change avec les commandes actuelles
G5. backup des shortcuts operateurs et des scripts legacy
G6. plan de rollback documente et teste sur papier
```

## 2_GATES PENDANT IMPLEMENTATION

```text
G7. chaque phase de retrait est validee separement
G8. les scripts retires sont archives, pas supprimes
G9. les shortcuts sont testes apres chaque modification
G10. le workflow post_change est re-teste apres chaque retrait de module
```

## 3_PREUVES ATTENDUES

```text
- liste exhaustive des callers (rg dans tout le repo)
- logs de test post_change avant/apres
- backups des fichiers retires dans _archive/
- confirmation operateur que les raccourcis fonctionnent
```

## 4_ROLLBACK ATTENDU

```text
- restaurer les fichiers depuis _archive/
- restaurer les shortcuts precedents
- re-test post_change
- documenter la raison du rollback
```

## 5_NEXT APRES VALIDATION

```text
GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_01
```

Condition :

```text
toutes les gates G1-G6 sont satisfaites et validees.
```
