---
doc_id: OPT_TRADING_STATUS_BOT_VISION_CANONIQUE
doc_type: family_status
repo: opt-trading
project: opt-trading
module:
go_id:
status: validated
lifecycle_stage: consolidation
topic_keys:
  - opt-trading
  - status
  - bot_vision
  - module_family
  - continuity
search_tags:
  - surface:module_family
  - doc_role:carte
  - product:bot_vision
surface: module_family
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Reprise"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md
  - docs/ot/project_cards/PROJECT_CARD_BOT_VISION_INGESTION_01.md
---

# BOT_VISION — STATUT CANONIQUE

## Role documentaire

- role_actuel: fiche courte de statut de famille Bot Vision
- role_cible: fiche annexe de consolidation de lignee, non souveraine
- souverainete: ne remplace ni la synthese produit, ni les closeouts, ni un arbitrage structurel complet
- lecture_de_reprise: lire d'abord `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, puis recroiser `MATRICE_GOUVERNANTE_V2.md` et la synthese Bot Vision avant d'utiliser cette fiche pour relire survivant / transition / legacy

## Objet
Fiche courte de lignée pour la famille vision (`bot_vision`, `bot_vision_step2`, `vision_bot`).

## ETABLI
- coexistence parallèle confirmée avec mélange nomenclature step/nom final
- risque de confusion survivant/entrée runtime reconnu
- paire opératoire transitoire confirmée : `vision_bot` + `bot_vision_step2`
- `bot_vision` confirmé comme héritage `step1`, utile pour trajectoire et placeholder mais non survivant implicite

## Survivant / Transition / Legacy / Archive
- survivant : aucun module unique figé dans ce lot ; la chaîne opératoire transitoire retenue est `vision_bot` + `bot_vision_step2`
- transition : `vision_bot` porte la capture / inbox-outbox ; `bot_vision_step2` porte l’analyse Vision / Telegram et les artefacts Desk Pro
- legacy : `bot_vision`
- archive : non figé dans ce lot

## Liens de preuve
- `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md`
- `docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md`
- `docs/ot/project_cards/PROJECT_CARD_BOT_VISION_INGESTION_01.md`

## Reprise
- reprise immédiate documentée dans `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01`
- arbitrage structurel final à reprendre plus loin dans `VISION_FAMILY_SURVIVOR_DECISION` si un survivant unique doit être matérialisé
