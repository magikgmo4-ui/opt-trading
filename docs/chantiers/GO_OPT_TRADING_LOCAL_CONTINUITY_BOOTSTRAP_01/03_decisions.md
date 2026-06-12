---
doc_id: GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01_DECISIONS
doc_type: decision
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01
status: active
lifecycle_stage: validation
topic_keys:
  - opt-trading
  - continuity
  - decisions
  - bootstrap
surface: chantier
source_kind: canonical
updated_at: 2026-04-11
links:
  - docs/chantiers/GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01/01_plan.md
  - docs/governance/MEMORY_BRICKS_MAPPING.md
---

# 03_decisions — GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01

## Décision 1
- sujet : ordre de migration documentaire initial
- options envisagées :
  - commencer par `openclaw`
  - commencer par `localcms`
  - commencer par `opt-trading`
- option retenue : commencer par `opt-trading`
- raison du choix : `opt-trading` est le repo canonique principal et porte déjà `memory_bricks`, donc toute erreur de structure y serait la plus coûteuse
- impact : la méthode locale et la dérivation vers `memory_bricks` sont sécurisées avant propagation aux autres repos
- suites ouvertes : aligner ensuite `openclaw`, puis `localcms`, puis `llm_wiki_minimal`

## Décision 2
- sujet : stratégie de migration
- options envisagées :
  - réécriture massive immédiate
  - migration progressive par pilotes
- option retenue : migration progressive par pilotes
- raison du choix : réduire le risque de contradiction, valider le pattern sur un cas réel avant généralisation
- impact : la migration commence par un socle local puis un premier chantier pilote complet
- suites ouvertes : choisir ensuite un chantier plus directement lié à `memory_bricks`

## Décision 3
- sujet : premier chantier pilote local
- options envisagées :
  - chantier historique lourd
  - chantier `memory_bricks` complexe
  - bootstrap de continuité locale de `opt-trading`
- option retenue : bootstrap de continuité locale de `opt-trading`
- raison du choix : cas simple, réel, déjà entamé, directement relié à la migration du socle documentaire
- impact : un premier exemple canonique complet est disponible rapidement
- suites ouvertes : ouvrir ensuite un pilote plus proche d’un cas métier ou `memory_bricks`

## RISKS

- À qualifier.
