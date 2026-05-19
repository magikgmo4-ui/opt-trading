---
doc_id: GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01_COST_BENEFIT_DECISION
doc_type: decision
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01
status: draft_for_review
lifecycle_stage: child_decision
parent_go_id: GO_COLLECTORS_OPERATOR_SURFACE_ALIGNMENT_01
topic_keys:
  - opt-trading
  - collectors
  - cost-benefit
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01/02_COST_BENEFIT_DECISION.md
point_de_reprise: "Rendre la decision explicite: extraire un peu, ou garder la separation runtime."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01/01_EXTRACTION_CANDIDATES.md
---

# 02_COST_BENEFIT_DECISION

## 1_ANALYSE

```text
Benefices potentiels d'une extraction selective :
- reduire duplications utilitaires
- converger doctrine/famille
- faciliter futurs collectors spot/derives

Couts/risques :
- risque de toucher le runtime derives canonique
- risque de casser les consumers historiques
- risque de glisser vers une broad refactor interdite
```

## 2_DECISION

```text
Decision retenue :
KEEP RUNTIME SEPARATION, with only selective helper extraction IF and ONLY IF
une duplication concrete et isolee est prouvee dans un GO cible.
```

## 3_CONSEQUENCE

```text
Pas de broad extraction now.
Autoriser seulement de petits lots cibles sur helpers generiques,
jamais sur semantics metier derives.
```
