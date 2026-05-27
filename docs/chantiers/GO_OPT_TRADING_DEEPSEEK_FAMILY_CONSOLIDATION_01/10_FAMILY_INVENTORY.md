---
doc_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01_FAMILY_INVENTORY
doc_type: family_inventory
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - deepseek
  - inventory
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01/00_INITIAL_PROJECT_DOC.md
---

# 10_FAMILY_INVENTORY

## Baseline current

| Module | Baseline current | Registry modules | Family |
| --- | --- | --- | --- |
| `deepseek_hub` | oui | non | `deepseek` |
| `deepseek_response` | oui | non | `deepseek` |
| `deepseek_student` | oui | non | `deepseek` |
| `deepseek_thinking` | oui | non | `deepseek` |

## Vue d'ensemble

| Module | Role constate | Classement retenu |
| --- | --- | --- |
| `deepseek_hub` | menu/cmd unifies, patches famille, point d'orchestration | owner documentaire + hub operateur |
| `deepseek_response` | reponses finales via Ollama, sorties archivees | satellite de compatibilite actif |
| `deepseek_thinking` | mode thinking via Ollama, sorties archivees | satellite de compatibilite actif |
| `deepseek_student` | surface de transition vers runtime `student`, roadmaps et wrappers limites | legacy de transition / surface limitee |

## Detail par module

### `deepseek_hub`

- README: menu unifie DeepSeek
- applique des patches sur `deepseek_thinking` et `deepseek_response`
- se presente comme candidat module unifie le plus avance
- orchestre encore `deepseek_thinking`, `deepseek_response` et `deepseek_student` pour certaines roadmaps

### `deepseek_response`

- produit les reponses finales cote `student`
- archive dans `_student_archive/response`
- garde un statut actif en compatibilite operatoire
- explicitement non survivant de famille a ce stade

### `deepseek_thinking`

- produit le thinking cote `student`
- archive dans `_student_archive/thinking`
- garde un statut actif en compatibilite operatoire
- explicitement non survivant de famille a ce stade

### `deepseek_student`

- README explicite: pas source de verite runtime actuelle
- runtime actif situe plutot dans `scripts/student/` et cible `student/scripts/`
- reste une cible de transition / consolidation
- le guide produit le classe en `USABLE_LIMITED`, learning-only, avec legacy encore present

## Nature de la famille

La famille n'est pas une simple lignee lineaire.

Etat retenu:

- `deepseek_hub` = owner documentaire et hub de convergence
- `deepseek_response` + `deepseek_thinking` = satellites de compatibilite encore utilises
- `deepseek_student` = surface legacy/transitoire, non owner runtime canonique

Conclusion:

- famille `deepseek` = **stack complementaire avec noyau convergent**, pas survivant physique unique deja abouti
