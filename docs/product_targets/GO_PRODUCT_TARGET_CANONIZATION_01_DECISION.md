---
doc_id: OPT_TRADING_GO_PRODUCT_TARGET_CANONIZATION_01_DECISION
doc_type: product_target_decision
repo: opt-trading
project: opt-trading
module:
go_id: GO_PRODUCT_TARGET_CANONIZATION_01
status: validated
lifecycle_stage: consolidation
topic_keys:
  - opt-trading
  - product_target
  - decision
  - student
  - deepseek
  - openclaw
search_tags:
  - surface:continuity
  - doc_role:decision
surface: continuity
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 4. DECISION"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/product_targets/RUNTIME_TO_TARGET_MAPPING.md
---

# GO_PRODUCT_TARGET_CANONIZATION_01

## Role documentaire

- role_actuel: decision locale du lot `product_targets` avec arbitrage encore marque `A_REVALIDER`
- role_cible: annexe de decision bornee, utile pour la reprise mais non souveraine a elle seule
- souverainete: ne redefinit ni la hierarchie produit transverse, ni le canon du repo
- lecture_de_reprise: relire cette decision apres `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, puis recroiser `MATRICE_GOUVERNANTE_V2.md` et verifier les cibles et le mapping derives

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
