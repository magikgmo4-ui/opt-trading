---
doc_id: GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01_PLAN
doc_type: chantier_plan
repo: opt-trading
project: memory_bricks
module: memory_bricks
go_id: GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01
status: active
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - memory_bricks
  - pilot
  - mapping
surface: memory
source_kind: canonical
updated_at: 2026-04-11
links:
  - docs/chantiers/GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01/00_cadrage.md
  - docs/governance/MEMORY_BRICKS_MAPPING.md
---

# 01_plan — GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01

## But du plan
- but : établir un premier cas canonique directement rattaché à `memory_bricks`
- ordre d’exécution retenu : cadrage -> plan -> décisions -> closeout initial -> enrichissement factuel si nécessaire

## Étapes
1. ancrer le chantier dans le schéma réel `memory_bricks`
2. stabiliser les décisions minimales de cadrage utiles au cas pilote
3. produire un closeout utilisable comme référence de dérivation compacte
4. répercuter le nouveau point de reprise dans les index locaux

## Zones de travail pressenties
- `docs/chantiers/GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01/`
- `docs/governance/MEMORY_BRICKS_MAPPING.md`
- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/REPRISE.md`

## Validations prévues
- cohérence avec le schéma documentaire `memory_bricks`
- cohérence avec la gouvernance locale déjà posée
- utilité réelle comme modèle pilote pour le repo et pour la suite inter-repos

## Risques
- risque : chantier trop méta et pas assez rattaché au composant réel
- mitigation : référencer explicitement la spec et le module `memory_bricks` existants

## Point d’arrêt acceptable
- arrêt acceptable si : le pilote produit déjà un cadrage, des décisions et un closeout suffisamment ancrés pour servir de référence initiale

## RISKS

- À qualifier.
