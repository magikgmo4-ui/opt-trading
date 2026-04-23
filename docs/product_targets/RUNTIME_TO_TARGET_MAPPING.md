---
doc_id: OPT_TRADING_RUNTIME_TO_TARGET_MAPPING
doc_type: product_target_mapping
repo: opt-trading
project: opt-trading
module: product_targets
go_id:
status: reference
lifecycle_stage: continuity
topic_keys:
  - opt-trading
  - runtime
  - product_targets
  - mapping
surface: continuity
source_kind: derived
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/product_targets/GO_PRODUCT_TARGET_CANONIZATION_01_DECISION.md
---

# RUNTIME TO TARGET MAPPING

## Role aligne avec la matrice maitre

- role actuel : mapping de lecture runtime -> cible
- role cible : support derive de mapping produit
- ce document n'est pas une decision canonique finale ; il reste subordonne a la matrice maitre et a la revalidation produit

## 1. RUNTIME ACTUEL (ETABLI)

- scripts/student/
- modules/deepseek_student/
- modules/deepseek_hub/
- openclaw (modules)

---

## 2. MAPPING

scripts/student/
-> Student
Statut: ETABLI (runtime canonique actuel)

deepseek_hub
-> DeepSeek/Ollama
Statut: PARTIEL (candidat d'unification)

deepseek-student
-> surface operateur DeepSeek
Statut: PARTIEL

openclaw
-> OpenClaw labo gouverne
Statut: PARTIEL

---

## 3. LECTURE GLOBALE

- runtime reel != cible produit finale
- convergence en cours
- aucune cible unique figee

---

## 4. GAP PRINCIPAL

- absence de decision canonique finale
- coexistence:
  - runtime legacy
  - hub candidat
  - couche operateur
