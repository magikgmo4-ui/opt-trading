---
doc_id: GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01_CADRAGE
doc_type: chantier_parent
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - modules
  - canonical
  - archive
  - consolidation
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/91_synthese_resultats.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/92_plans_execution_sous_lots.md
  - _archive/legacy_modules
  - _archive/root_backups
  - docs/chantiers/GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01/01_grille_decision.md
  - docs/chantiers/GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01/02_plan_operationnel_step_by_step.md
  - docs/chantiers/GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01/03_priorisation_familles.md
---

# GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01

## Objet
Transformer la doctrine implicite actuelle en regle d'execution simple :
- consolider ce qui est canonique et prouve utile
- sortir ce qui est depasse vers archive ou backup
- eliminer les variantes actives paralleles `step`, `fix`, `patch`, `vN` quand elles n'ont plus de raison d'etre

## Cible finale
Obtenir pour chaque categorie :
- un proprietaire canonique clair
- zero duplication active non justifiee
- zero wrapper pointant vers une surface depassee
- une voie explicite de sortie vers `_archive`

## Regle structurante
La cible n'est pas :
- un seul module physique pour tout un domaine

La cible est :
- un seul module canonique proprietaire par capacite
- des sous-roles distincts gardes separes seulement si leur frontiere runtime est reelle
- toute surface depassee bascule en :
  - compat temporaire
  - legacy fige
  - archive/backup

## Portee
- doctrine de classement pour `modules/`
- priorisation des familles a consolider
- regles de bascule vers `_archive/legacy_modules`
- regles de retention pour `root_backups`

## Anti-cibles
- pas de moves physiques massifs dans ce lot parent
- pas de fusion rhetorique entre modules qui ont des roles runtime differents
- pas d'archivage sans preuve de non-usage

## Livrables
- [01_grille_decision.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01/01_grille_decision.md)
- [02_plan_operationnel_step_by_step.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01/02_plan_operationnel_step_by_step.md)
- [03_priorisation_familles.md](/C:/Users/ghost/opt-trading/docs/chantiers/GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01/03_priorisation_familles.md)

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
