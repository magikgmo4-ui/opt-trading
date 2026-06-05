---
doc_id: GO_RANGE_STRATEGY_V1_STRUCT_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: trading
module: range_strategy_v1
go_id: GO_RANGE_STRATEGY_V1_STRUCT_01
status: active
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - trading
  - range_strategy
  - cadrage
surface: chantier
source_kind: canonical
updated_at: 2026-04-14
links:
  - docs/ot/trading/22_RANGE_STRATEGY_V1_STRUCT_01.md
  - docs/ot/trading/INDEX.md
  - docs/master_pack/00_current_state_and_standards.md
  - docs/governance/REPO_ROLE.md
  - docs/governance/DOC_LAYERS.md
---

# 00_cadrage — GO_RANGE_STRATEGY_V1_STRUCT_01

## Identité
- GO : GO_RANGE_STRATEGY_V1_STRUCT_01
- Repo : opt-trading
- Branche : sot/mainline
- Statut : active
- Type de travail : module durable documentaire / cadrage stratégie trading

## État de départ retenu
- un besoin explicite existe pour cibler des actifs faciles à trader en range
- un noyau initial a été validé en séance : `AUD/NZD`, `USD/CHF`, `XAUUSD`
- aucun cadre canonique `Range Strategy V1` n'était encore figé dans `docs/ot/trading/`
- le chantier doit partir du besoin, de l'objectif final visé et du plan validé, sans sur-vendre une validation statistique inexistante

## Objectif du lot
- ouvrir un chantier canonique pour `Range Strategy V1`
- figer la cible finale visée, le plan validé reconstitué, l'état établi et le gap restant
- préparer la suite logique vers un lot règles opératoires explicites

## Non-objectifs
- ouvrir un bot
- annoncer un winrate
- produire un backtest présenté comme preuve finale
- ouvrir un runtime ou un module d'exécution

## Contexte utile
- la couche `docs/ot/trading/` porte déjà le canon trading principal du repo
- la couche `docs/chantiers/` doit porter le lot borné et sa traçabilité
- les couches `governance`, `master_pack`, `index`, `next`, `opportunities`, `product_targets` doivent être lues avant de décider si une mutation transverse est réellement justifiée

## Critères PASS / FAIL
- PASS si : le chantier est posé au format canonique, la cible visée est explicite, le plan est lisible et le point de reprise suivant est univoque
- FAIL si : le chantier reste ambigu, mélange cadrage et validation, ou crée une seconde source de vérité confuse

## Point de vigilance
- risque principal : confondre cadrage stratégique et stratégie déjà validée
- point d'arrêt acceptable : dossier chantier complet + ancre trading canonique + suite logique nommée

## RISKS

- À qualifier.
