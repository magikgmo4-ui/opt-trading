---
doc_id: OPT_TRADING_RUNTIME_TO_TARGET_MAPPING
doc_type: product_target_mapping
repo: opt-trading
project: opt-trading
module:
go_id:
status: validated
lifecycle_stage: consolidation
topic_keys:
  - opt-trading
  - runtime
  - product_target
  - mapping
  - continuity
search_tags:
  - surface:continuity
  - doc_role:carte
surface: continuity
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 2. MAPPING"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/product_targets/GO_PRODUCT_TARGET_CANONIZATION_01_DECISION.md
  - docs/product_targets/STUDENT_TARGET_CANON.md
  - docs/product_targets/DEEPSEEK_OLLAMA_TARGET_CANON.md
  - docs/product_targets/OPENCLAW_TARGET_CANON.md
---

# RUNTIME TO TARGET MAPPING

## Role documentaire

- role_actuel: tableau de correspondance runtime -> cible produit
- role_cible: support derive de lecture et de consolidation, non souverain
- souverainete: ne remplace ni les cibles produit, ni l'etat runtime prouve, ni une decision canonique transverse
- lecture_de_reprise: verifier ce mapping apres lecture de `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, puis recroiser `MATRICE_GOUVERNANTE_V2.md` contre les fiches source et contre le repo reel avant toute conclusion

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
