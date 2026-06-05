---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_04_DEEPSEEK_STUDENT_ROLE_MAP
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - modules
  - step-04
  - deepseek
  - student
  - role-map
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - docs/status/deepseek_student_canonique.md
  - docs/product_targets/DEEPSEEK_OLLAMA_TARGET_CANON.md
  - docs/student_deepseek_runbook.md
  - docs/ot/trae/OT_OPS_04B_STUDENT_RUNTIME_FREEZE_NOTE.md
  - scripts/student/deepseek_student_cmd.sh
  - modules/deepseek_hub/README.md
  - modules/deepseek_student/README.md
  - modules/deepseek_response/README.md
  - modules/deepseek_thinking/README.md
---

# Step 04 - role map `DeepSeek/student`

## Statut
Complete.

## Objet
Figer la carte de role `DeepSeek/student` en distinguant clairement runtime reel, facade module candidate, couches de compatibilite et cible de transition.

## Verifications utilisees
- lecture de `docs/status/deepseek_student_canonique.md`
- lecture de `docs/product_targets/DEEPSEEK_OLLAMA_TARGET_CANON.md`
- lecture de `docs/student_deepseek_runbook.md`
- lecture de `docs/ot/trae/OT_OPS_04B_STUDENT_RUNTIME_FREEZE_NOTE.md`
- lecture de `scripts/student/deepseek_student_cmd.sh`
- lecture des README de :
  - `modules/deepseek_hub`
  - `modules/deepseek_student`
  - `modules/deepseek_response`
  - `modules/deepseek_thinking`

## Hierarchie d'entrypoints
| Niveau | Surface | Entree retenue | Role |
|---|---|---|---|
| runtime operatoire actuel | `scripts/student/` | `scripts/student/deepseek_student_cmd.sh` | verite runtime actuelle |
| wrapper installe | machine `student` | `deepseek-student` | facade utilisateur courante apres install |
| facade module candidate | `modules/deepseek_hub` | `modules/deepseek_hub/scripts/deepseek_hub_cmd.sh` | candidat unifie cote `modules/` |
| compatibilite | `modules/deepseek_response`, `modules/deepseek_thinking` | wrappers propres | couches specialisees encore utiles |

## Carte de role
| Composant | Statut | Role retenu | Frontiere |
|---|---|---|---|
| `scripts/student/` | actif | runtime reel | source de verite operatoire aujourd'hui |
| `deepseek_hub` | actif | facade module candidate | unifie progressivement la famille cote `modules/` |
| `deepseek_response` | actif | compatibilite response | reste utile tant que l'absorption n'est pas complete |
| `deepseek_thinking` | actif | compatibilite thinking | reste utile tant que l'absorption n'est pas complete |
| `deepseek_student` | transition | cible de consolidation incomplete | ne pas lire comme runtime actif |

## Points de duplication ou d'ambiguite
- `scripts/student/deepseek_student_cmd.sh` expose deja une facade globale et delegue partiellement vers `deepseek_hub`, ce qui cree un recouvrement volontaire mais instable.
- `deepseek_hub` orchestre encore des patches vers `deepseek_response` et `deepseek_thinking`, donc la famille n'est pas encore absorbee dans un seul module autonome.
- les sorties sont eparpillees entre `data/logs/deepseek_student` et `_student_archive/*`, ce qui complique une lecture unique du stockage.
- `deepseek_student` existe comme module cible, mais sa propre documentation confirme qu'il ne faut pas le promouvoir en source de verite runtime.

## Risques de consolidation
- basculer trop tot hors `scripts/student/` casserait la verite runtime actuellement documentee et exploitee.
- supprimer `deepseek_response` ou `deepseek_thinking` avant absorption complete dans `deepseek_hub` casserait la compatibilite.
- traiter `deepseek_student` comme survivant final masquerait un ecart connu entre cible structurelle et runtime reel.
- fusionner trop vite les surfaces logs / archives sans contrat de retention ferait disparaitre des preuves utiles.

## Decision retenue
- runtime canonique actuel confirme : `scripts/student/`
- survivant module candidat confirme : `deepseek_hub`
- `deepseek_response` et `deepseek_thinking` maintenus comme compatibilite
- `deepseek_student` maintenu comme transition non-runtime
- aucun move physique autorise dans ce lot

## Rollback
- revert doc-only de cette note
- revert doc-only du plan si besoin

## Point de reprise
Carte P1 `DeepSeek/student` complete. Poursuivre avec `reseau/share/transfer`, puis basculer en `Step 05`.

## RISKS

- À qualifier.
