---
doc_id: GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01_DECISIONS
doc_type: decision
repo: opt-trading
project: memory_bricks
module: memory_bricks
go_id: GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01
status: active
lifecycle_stage: validation
topic_keys:
  - opt-trading
  - memory_bricks
  - decisions
  - pilot
surface: memory
source_kind: canonical
updated_at: 2026-04-11
links:
  - docs/governance/MEMORY_BRICKS_MAPPING.md
---

# 03_decisions — GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01

## Décision 1
- sujet : type de pilote retenu
- option retenue : pilote directement rattaché au composant réel `memory_bricks`
- raison du choix : valider la méthode sur un cas compact canonique réel
- impact : le pilote reste ancré sur les artefacts existants du module

## Décision 2
- sujet : portée du lot
- option retenue : chantier documentaire sans modification du module
- raison du choix : sécuriser d’abord la méthode et la dérivation
- impact : faible risque, forte valeur de référence

## Décision 3
- sujet : niveau de preuve attendu
- option retenue : closeout relié aux artefacts existants
- raison du choix : conserver un lien clair entre doc longue et schéma `memory_bricks`
- impact : fermeture exploitable comme exemple pour la suite

## RISKS

- À qualifier.
