# GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REMEDIATION_PLAN_V1_01

## 1_MASTER_TARGET
Créer un plan de remédiation documentaire V1 basé sur la baseline WHY lint V1, sans correction automatique.

## 2_INITIAL_PROJECT_DOC
Référencer :
- SPEC parent : docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md
- scan spec : docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md
- scan implementation V1 : docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_V1_01.md
- scan report V1 : docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01.md
- triage report V1 : docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_TRIAGE_V1_01.md
- baseline V1 : docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_BASELINE_V1_01.md
- commande --scan-docs

## 3_INITIAL_NEED
La baseline V1 établit des findings acceptés. Il faut maintenant planifier quoi faire sans modifier les documents :
- quels gaps corriger plus tard ;
- quels findings traiter comme bruit V1 ;
- quelles exceptions documenter ;
- quelles règles ajuster ;
- quels GO ouvrir ensuite.

## 4_MASTER_PROJECT_PLAN
Étapes :
1. relire baseline V1 ;
2. relancer scan V1 pour contrôle ;
3. comparer métriques avec baseline ;
4. définir familles de remédiation ;
5. créer un plan de correction documentaire ;
6. créer un plan d’ajustement des règles ;
7. créer un plan d’exceptions documentées ;
8. définir l’ordre des prochains GO ;
9. ne corriger aucun fichier dans ce GO.

## 6_FINAL_TARGET
Produire un plan de remédiation V1 actionnable, séparant corrections documentaires, bruit V1, exceptions et ajustements de règles, sans aucune mutation des documents scannés.

## 7_CANONICAL_STATE
- PR #436 mergée ;
- baseline V1 canonique ;
- validateur V1 read-only/report-only ;
- scan V1 fonctionne ;
- findings présents et attendus ;
- aucun autofix ;
- aucune CI bloquante ;
- aucune correction encore appliquée.

## 8_VALIDATED_PLAN
Plan de ce GO :
- documenter uniquement ;
- ne pas corriger ;
- ne pas modifier outil/tests/fixtures ;
- ne pas modifier docs scannées ;
- proposer les prochains GO.

## 9_SELECTED_SOLUTION
Rapport Markdown unique de planification.

Le plan divise les actions futures en lots séparés :
1. corrections documentaires ciblées ;
2. exceptions documentées ;
3. ajustement des règles V1 ;
4. future baseline V2 ;
5. éventuelle extension de scan.

## 10_SELECTED_SETUP
Fichier :
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REMEDIATION_PLAN_V1_01.md

## 11_KEY_DECISIONS
- aucune correction dans ce GO ;
- remédiation séparée par GO ;
- ne pas mélanger correction documentaire et ajustement validateur ;
- ne pas assouplir les règles sans preuve ;
- ne pas étendre repo-wide avant stabilisation V1 ;
- ne pas rendre CI bloquante ;
- garder les findings comme signaux, pas permissions.

## 12_INVARIANTS
- read-only
- report-only
- no source mutation
- no autofix
- no runtime
- no MCP live
- no trade
- no secret
- no CI blocking
- no global index mutation
- findings are not permissions
- baseline precedes remediation
- remediation plan precedes correction

## 13_ESTABLISHED
- baseline initiale : 30 / 1 / 113 ;
- baseline post-report : 31 / 1 / 114 ;
- baseline post-triage : 32 / 1 / 115 ;
- dérive auto-référentielle documentée ;
- scan V1 ne modifie rien ;
- tests existants OK.

## 14_HYPOTHESIS
À valider :
- plusieurs findings sont des gaps réels ;
- plusieurs findings sont du bruit V1 ;
- certains documents nécessitent des exceptions ;
- certains marqueurs requis sont trop stricts pour certains types de docs ;
- le validateur devrait probablement ignorer ses propres rapports ou appliquer une catégorie spéciale aux rapports.

## 15_REMAINING_GAP
- pas encore de correction documentaire ;
- pas encore de baseline V2 ;
- pas encore de règles d’exception codifiées ;
- pas encore d’ajustement validateur ;
- pas encore de mode ignore reports ;
- pas encore de scan élargi ;
- pas encore de CI ;
- pas encore de rapport automatisé persistant.

## 16_TODO
Créer les prochains GO recommandés :
1. GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_PLAN_V1_01
2. GO_OPT_TRADING_DOC_OPS_WHY_LINT_REPORT_SELF_REFERENCE_RULE_01
3. GO_OPT_TRADING_DOC_OPS_WHY_LINT_DOCUMENTED_EXCEPTIONS_V1_01
4. GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_V1_01
5. GO_OPT_TRADING_DOC_OPS_WHY_LINT_BASELINE_V2_01

## 17_RESUME_POINT
Après merge :
GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_PLAN_V1_01

## 18_TO_DOCUMENT
TAGS :
- WHY_LINT_REMEDIATION_PLAN_V1
- WHY_LINT_BASELINE_TO_ACTION
- WHY_LINT_NO_AUTOFIX
- WHY_LINT_REAL_GAPS_NEXT
- WHY_LINT_RULE_REFINEMENT_LATER

## 19_TO_REMEMBER
Memory Bricks candidats :
- La remédiation V1 doit rester planifiée avant correction.
- Les rapports WHY lint produisent une dérive auto-référentielle à gérer explicitement.
- Les corrections documentaires, exceptions et ajustements de règles doivent rester séparés en GO distincts.
- Le prochain GO recommandé est REAL_GAPS_FIX_PLAN_V1_01, pas une correction automatique.

## Baseline inputs
| Source | Status | Notes |
| :--- | :--- | :--- |
| scan report V1 | OK | Baseline initiale |
| triage report V1 | OK | Findings triés |
| baseline V1 | OK | Référence canonique |
| current scan relaunch | OK | Confirmé |

## Remediation buckets
| Bucket | Meaning | Allowed next action | Forbidden action |
| :--- | :--- | :--- | :--- |
| REAL_GAP | Correction nécessaire | Planifier correction | Ignorer |
| V1_NOISE | Bruit du validateur | Ajuster règle validateur | Corriger doc |
| DOCUMENTED_EXCEPTION | Exception justifiée | Documenter | Ignorer |
| RULE_REFINEMENT_NEEDED | Règle trop stricte | Ajuster règle | Ignorer |
| NEED_MORE_EVIDENCE | Analyse incomplète | Enquêter | Décider |
| SELF_REFERENCE_DRIFT | Rapport validateur | Ignorer rapports | Corriger rapports |

## Proposed GO split
| GO_ID | Purpose | Scope | Allowed changes | Forbidden changes |
| :--- | :--- | :--- | :--- | :--- |
| GO_..._REAL_GAPS_FIX_PLAN_V1_01 | Correction gaps | Doc uniquement | Plan doc | Mutation auto |
| GO_..._REPORT_SELF_REFERENCE_RULE_01 | Gestion rapports | Validateur | Règle | Mutation doc |
| GO_..._DOCUMENTED_EXCEPTIONS_V1_01 | Exception | Doc | Doc exception | Mutation validateur |
| GO_..._RULE_REFINEMENT_V1_01 | Ajustement règles | Validateur | Règle | Mutation doc |
| GO_..._BASELINE_V2_01 | V2 Baseline | Baseline | Baseline | Mutation doc |

## Remediation policy
- un finding ne doit pas être corrigé sans classification ;
- une correction documentaire doit être distincte d’un ajustement validateur ;
- un ajustement validateur exige preuve de bruit ;
- une exception doit être documentée ;
- une baseline V2 doit suivre les changements.

## Non-goals
- pas de correction dans ce GO ;
- pas d’autofix ;
- pas de CI ;
- pas de scan repo-wide ;
- pas de mutation runtime ;
- pas de suppression de findings sans justification.

## Recommended next GO
GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_PLAN_V1_01
Objectif : Planifier uniquement les corrections des vrais gaps documentaires.
