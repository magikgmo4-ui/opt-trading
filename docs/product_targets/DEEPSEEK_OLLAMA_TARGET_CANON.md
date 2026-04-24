---
doc_id: OPT_TRADING_DEEPSEEK_OLLAMA_TARGET_CANON
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
  - deepseek
  - ollama
  - student
search_tags:
  - surface:continuity
  - doc_role:carte
surface: continuity
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 4. ECART EXACT"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/product_targets/RUNTIME_TO_TARGET_MAPPING.md
  - docs/status/deepseek_student_canonique.md
---

# DEEPSEEK / OLLAMA — TARGET CANON

## Role documentaire

- role_actuel: annexe produit partielle sur la ligne DeepSeek / Ollama cote student
- role_cible: annexe produit non souveraine alignee sur la matrice maitre doc ops ; V2 reste une annexe stable secondaire utile
- souverainete: ne remplace ni la matrice, ni `GO_INDEX.md`, ni une synthese produit transverse
- lecture_de_reprise: lire cette fiche apres `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, puis recroiser `MATRICE_GOUVERNANTE_V2.md` avant de revalider le mapping runtime associe

## 1. OBJECTIF PRODUIT DESIRE (ETABLI)

Stack IA locale en duo:

- thinking model
- response model

Fonctions:
- analyse locale
- journalisation
- integration Student
- validation externe obligatoire

Acces via:
- API HTTP (/api/chat)
- hub/menu unifie

---

## 2. ROLE SYSTEME

Position:
- couche cognitive locale

Interactions:
- consomme donnees Student
- produit analyse
- expose resultats via API/menu

---

## 3. ETAT REPO REEL

- deepseek_hub (candidat)
- deepseek_student (operateur)
- scripts/student runtime actif
- runbook partiel

---

## 4. ECART EXACT

- separation thinking/response non generalisee
- hub/menu non completement unifie
- usage encore mixte (CLI / scripts)

---

## 5. CONTRAINTES

- eviter ollama run en SSH
- privilegier API HTTP
- validation externe obligatoire
- learning-only (pas decision autonome)

---

## 6. NON_OBJECTIFS

- ne devient pas:
  - systeme autonome de trading
  - decisionnaire final
  - moteur non valide
