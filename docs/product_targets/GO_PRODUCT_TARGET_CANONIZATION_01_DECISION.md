---
doc_id: OPT_TRADING_GO_PRODUCT_TARGET_CANONIZATION_01_DECISION
doc_type: product_target_decision
repo: opt-trading
project: opt-trading
module: product_targets
go_id:
status: reference
lifecycle_stage: continuity
topic_keys:
  - opt-trading
  - product_targets
  - target_decision
  - revalidation
surface: continuity
source_kind: derived
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/product_targets/RUNTIME_TO_TARGET_MAPPING.md
---

# GO_PRODUCT_TARGET_CANONIZATION_01

## Role aligne avec la matrice maitre

- role actuel : note de decision partielle sur des cibles produit
- role cible : support derive de revalidation produit
- ce document ne fixe pas une souverainete transverse ; son statut `A_REVALIDER` interdit de le lire comme canon maitre

## 1. QUESTION

Quelle cible produit canonique finale doit etre retenue pour:

- Student
- DeepSeek/Ollama
- OpenClaw

---

## 2. OPTIONS

1. maintenir scripts/student comme runtime durable
2. basculer vers deepseek_hub
3. officialiser deepseek-student comme surface canonique
4. combinaison structuree (hub + operator + runtime)

---

## 3. ETAT ACTUEL

- aucune cible finale unique figee repo-sourcee
- convergence partielle visible
- dependance forte au runtime existant

---

## 4. DECISION

Statut:
A_REVALIDER

---

## 5. CONDITIONS DE CLOTURE

- doc canon produit validee
- mapping runtime stabilise
- choix explicite:
  - hub
  - runtime
  - operator

- plan de migration defini
- retrait explicite de l'exception runtime si applicable

---

## 6. POINT CRITIQUE

Ne pas:
- casser scripts/student
- forcer unification prematuree
- perdre tracabilite runtime reel
