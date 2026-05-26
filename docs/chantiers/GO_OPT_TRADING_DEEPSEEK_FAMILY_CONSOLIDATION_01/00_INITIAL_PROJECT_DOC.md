---
doc_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01_INITIAL_PROJECT_DOC
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - deepseek
  - consolidation
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_REGISTRY_STACK_REALIGNMENT_IMPL_01/40_REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv
  - docs/product/guides/DEEPSEEK_STUDENT.md
---

# 00_INITIAL_PROJECT_DOC

## Objet

Cartographier la famille `deepseek*` pour distinguer les roles `hub`, `response`, `thinking`, `student`, puis fixer si l'ensemble releve :

- d'une stack complementaire ;
- d'une lignee fragmentee ;
- d'un survivant owner documentaire entoure de satellites de compatibilite ;
- d'une surface legacy encore maintenue pour transition.

## Perimetre cible

- `modules/deepseek_hub`
- `modules/deepseek_response`
- `modules/deepseek_student`
- `modules/deepseek_thinking`

## Etat d'entree

- `sot/mainline` est a jour apres merge `#815`
- `secrets/` est hors perimetre
- les 4 modules restent hors `modules_registry.yaml`
- les documents produits par d'autres chantiers mentionnent deja :
  - `deepseek_hub` comme candidat module unifie le plus avance
  - `deepseek_response` et `deepseek_thinking` comme surfaces de compatibilite
  - `deepseek_student` comme surface de transition / ferme cote parc principal, mais encore utilisable en mode limite sur `student`

## Questions a trancher

1. Quel module est owner canonique de la famille DeepSeek ?
2. `deepseek_hub` est-il hub operateur ou owner runtime ?
3. `deepseek_response` est-il runtime utile, formatteur, ou legacy ?
4. `deepseek_student` est-il encore actif ou legacy lie a `student`/Ollama ?
5. `deepseek_thinking` est-il composant de raisonnement actif ou archive ?
6. La famille forme-t-elle une stack complementaire ou une lignee a consolider ?
7. Quelles actions registry sont requises ?

## Contraintes appliquees

- mode `doc-only`
- aucun runtime
- aucune mutation registry
- aucun index global ajoute
- aucun toucher a `secrets/`
