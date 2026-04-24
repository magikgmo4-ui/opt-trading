---
doc_id: OPT_TRADING_OPENCLAW_TARGET_CANON
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
  - openclaw
  - provider
  - cockpit
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
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/ot/project_cards/PROJECT_CARD_OPENCLAW_01.md
---

# OPENCLAW — TARGET CANON

## Role documentaire

- role_actuel: annexe produit partielle sur le role local OpenClaw dans `opt-trading`
- role_cible: annexe produit non souveraine, subordonnee a la continuite globale et aux frontieres repo deja retenues
- souverainete: ne remplace ni la matrice, ni la hierarchie produit, ni les arbitrages de frontiere `openclaw` / `opt-trading`
- lecture_de_reprise: lire cette fiche apres `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, puis recroiser `MATRICE_GOUVERNANTE_V2.md` et `PRODUCT_CONTINUITY_HIERARCHY_01` avant de revalider l'ecart reel

## 1. OBJECTIF PRODUIT DESIRE (ETABLI)

OpenClaw est un labo Linux cloisonne et gouverne.

Caracteristiques:
- installation sur db-layer
- utilisateur dedie
- environnement isole
- regles strictes

---

## 2. ROLE SYSTEME

Position:
- couche experimentale / provider

Interactions:
- peut servir modeles
- integre sous controle strict
- non expose directement aux flux critiques

---

## 3. ETAT REPO REEL

- modules partiels
- provider layer existant
- doc gouvernance presente

---

## 4. ECART EXACT

- pas encore industrialise
- pas de pipeline stable complet
- pas de position finale fixee

---

## 5. CONTRAINTES

- Linux natif uniquement
- environnement cloisonne
- pas d'ouverture:
  - tools
  - channels
  - nodes

---

## 6. NON_OBJECTIFS

- ne devient pas:
  - produit user-facing
  - runtime principal
  - systeme ouvert non controle
