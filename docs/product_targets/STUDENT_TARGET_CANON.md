---
doc_id: OPT_TRADING_STUDENT_TARGET_CANON
doc_type: product_target
repo: opt-trading
project: opt-trading
module:
go_id:
status: validated
lifecycle_stage: reprise
topic_keys:
  - opt-trading
  - product_target
  - student
  - continuity
  - desk_pro
search_tags:
  - surface:continuity
  - doc_role:carte
  - product:desk_pro
surface: continuity
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 4. ECART EXACT"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md
  - docs/status/deepseek_student_canonique.md
---

# STUDENT — TARGET CANON

## Role documentaire

- role_actuel: annexe produit partielle centree sur la machine Student
- role_cible: annexe produit non souveraine, lue comme satellite machine de Desk Pro
- souverainete: ne remplace ni la matrice, ni la hierarchie produit, ni les runbooks machine
- lecture_de_reprise: lire cette fiche apres `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, puis recroiser `MATRICE_GOUVERNANTE_V2.md` et `PRODUCT_CONTINUITY_HIERARCHY_01` avant de verifier l'ecart avec le runtime reel

## 1. OBJECTIF PRODUIT DESIRE (ETABLI)

Student est un hub leger / archiviste central dans opt-trading.

Fonctions:
- journaling
- ingest HTTP
- archivage
- events append-only
- services de collecte
- IA locale de soutien

Contrainte forte:
- pas de DB layer lourd

---

## 2. ROLE SYSTEME

Position:
- machine de continuite (3e machine)

Interactions:
- recoit donnees (ingest)
- archive evenements
- alimente IA locale
- support analyse DeepSeek/Ollama

---

## 3. ETAT REPO REEL

- runtime reel: `scripts/student/`
- runbook operateur existant
- logique ingest partielle
- journal actif

---

## 4. ECART EXACT

- objectif produit clair (journal)
- mais:
  - pas de doc canon opposable unique
  - pas d'architecture explicitee
  - pas de contrat formel ingest / archive

---

## 5. CONTRAINTES

- runtime gele (exception)
- pas de refactor lourd
- append-only obligatoire

---

## 6. NON_OBJECTIFS

- ne devient pas:
  - DB layer
  - moteur analytics lourd
  - cluster distribue
