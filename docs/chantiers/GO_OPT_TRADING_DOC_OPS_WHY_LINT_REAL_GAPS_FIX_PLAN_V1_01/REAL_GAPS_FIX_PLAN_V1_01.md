# GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_PLAN_V1_01

## 1_MASTER_TARGET
Créer un plan de correction V1 pour les vrais gaps documentaires WHY lint identifiés par la chaîne canonique existante, sans correction automatique.

## 2_INITIAL_PROJECT_DOC
Références canoniques :
- SPEC parent : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md`
- spec review : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_SPEC_REVIEW_01.md`
- static validator spec : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01.md`
- real-docs scan spec : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md`
- scan report V1 : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01.md`
- triage report V1 : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_TRIAGE_V1_01.md`
- baseline V1 : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_BASELINE_V1_01.md`
- remediation plan V1 : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REMEDIATION_PLAN_V1_01.md`
- commande `--scan-docs` : `python tools/why_lint_static_validator/why_lint_static_validator.py --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`

## 3_INITIAL_NEED
La baseline V1 établit des findings acceptés. Il faut maintenant planifier la correction des vrais gaps documentaires sans toucher aux documents cibles :
- quels gaps sont réellement documentaires et doivent être corrigés ensuite ;
- quels findings relèvent du bruit V1 ou de la self-reference ;
- quelles exceptions doivent être documentées séparément ;
- quelles règles devront être raffinées plus tard ;
- quel GO ouvrir ensuite pour passer du plan à la correction.

## 4_MASTER_PROJECT_PLAN
Étapes :
1. relire la baseline V1 et le triage V1 ;
2. relire la chaîne canonique et le plan de remédiation V1 ;
3. isoler uniquement les gaps documentaires réels ;
4. classer ces gaps par type ;
5. définir le lot de corrections documentaires ciblées ;
6. séparer les sujets d’exceptions et de règles pour les GO futurs ;
7. garder la correction hors de ce GO ;
8. éviter toute mutation d’index global sauf preuve explicite ;
9. préparer le prochain GO de correction ciblée.

## 6_FINAL_TARGET
Produire un plan V1 de correction des vrais gaps documentaires WHY lint, classé par type, priorisé, et prêt à être exécuté dans un GO séparé, sans correction automatique ni mutation des documents scannés.

## 7_CANONICAL_STATE
- PR #437 mergée sur `sot/mainline` ;
- merge commit canonique : `5e7b755d7cbf91d8f4975436fca49e8fca74ac79` ;
- baseline V1 canonique disponible ;
- validateur V1 read-only/report-only ;
- scan V1 fonctionne sur le dossier parent WHY lint ;
- findings présents et attendus ;
- aucune correction encore appliquée ;
- aucun autofix ;
- aucune CI bloquante.

## 8_VALIDATED_PLAN
Plan de ce GO :
- documenter uniquement ;
- ne corriger aucun document métier cible ;
- ne pas modifier outil/tests/fixtures ;
- ne pas modifier les documents scannés ;
- ne pas faire d’auto-fix ;
- ne pas élargir le scan ;
- ne pas élargir les index globaux sans justification écrite.

## 9_SELECTED_SOLUTION
Rapport Markdown unique de planification des vrais gaps.

Lots de correction proposés :

| Gap type | Statut | Lecture de la baseline | Correction proposée | GO suivant |
| --- | --- | --- | --- | --- |
| manque de WHY explicite | réel pour les docs actifs de la chaîne | `MISSING_WHY_SECTION` reste le signal principal | ajouter un WHY explicite là où la fonction documentaire l’exige | `GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_V1_01` |
| continuité faible | réel pour les docs de transition | `MISSING_RESUME_POINT` montre une liaison de reprise incomplète | expliciter reprise, suite et lien vers le prochain GO | `GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_V1_01` |
| lien causal absent | réel pour les plans et baselines | les transitions baseline -> triage -> remédiation restent trop implicites | ajouter le pourquoi du classement et du prochain pas | `GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_V1_01` |
| état canonique ambigu | réel sur la chaîne de scan | l’écart 30/113 -> 31/114 -> 32/115 doit être expliqué comme état canonique et bruit auto-référentiel | figer le vocabulaire canonique et distinguer baseline / relance / self-reference | `GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_V1_01` |
| décision non reliée à un objectif | réel dans les recommandations | les next GO doivent pointer une intention documentaire explicite | relier chaque décision au but documenté | `GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_V1_01` |
| dérive documentaire probable | non corrigée dans ce GO | le rapport V1 et les artefacts scannés se re-scanne eux-mêmes | traiter dans un GO séparé de règle ou d’exception | `GO_OPT_TRADING_DOC_OPS_WHY_LINT_REPORT_SELF_REFERENCE_RULE_01` |

Synthèse de correction :
- le lot prioritaire est la continuité documentaire des GO actifs ;
- le lot secondaire est la clarification canonique baseline / relance / remédiation ;
- les sujets de self-reference restent hors de ce GO ;
- les exceptions et ajustements de règles restent séparés ;
- aucun document scanné n’est modifié ici.

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
- no global index mutation sans preuve explicite
- findings are not permissions
- baseline precedes remediation
- remediation plan precedes correction

## 13_ESTABLISHED
- baseline initiale : 30 / 1 / 113 ;
- baseline post-report : 31 / 1 / 114 ;
- baseline post-triage : 32 / 1 / 115 ;
- la dérive auto-référentielle est documentée ;
- le scan V1 ne modifie rien ;
- les tests existants sont OK ;
- le plan V1 de remédiation existe déjà et sépare corrections, exceptions et règles.

## 14_HYPOTHESIS
À valider dans les GO suivants :
- plusieurs findings sont des gaps réellement documentaires et non du bruit ;
- plusieurs findings sont du bruit V1 lié aux exemples ou aux artefacts ;
- certains docs exigent une exception formelle plutôt qu’une réécriture ;
- certains marqueurs sont trop stricts pour les docs de type plan, synthèse ou rapport ;
- le validateur doit probablement ignorer ou spécialiser ses propres rapports.

## 15_REMAINING_GAP
- pas encore de corrections documentaires appliquées ;
- pas encore de baseline V2 ;
- pas encore de règles d’exceptions codifiées ;
- pas encore d’ajustement validateur ;
- pas encore de mode ignore reports ;
- pas encore de scan élargi ;
- pas encore de CI ;
- pas encore de rapport automatisé persistant.

## 16_TODO
Créer les prochains GO recommandés :
1. `GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_V1_01`
2. `GO_OPT_TRADING_DOC_OPS_WHY_LINT_REPORT_SELF_REFERENCE_RULE_01`
3. `GO_OPT_TRADING_DOC_OPS_WHY_LINT_DOCUMENTED_EXCEPTIONS_V1_01`
4. `GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_V1_01`
5. `GO_OPT_TRADING_DOC_OPS_WHY_LINT_BASELINE_V2_01`

## 17_RESUME_POINT
Après merge :
`GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_V1_01`

Objectif :
appliquer uniquement les corrections documentaires classées comme vrais gaps, sans auto-fix.

## 18_TO_DOCUMENT
TAGS :
- WHY_LINT_REAL_GAPS_FIX_PLAN_V1
- WHY_LINT_BASELINE_TO_ACTION
- WHY_LINT_NO_AUTOFIX
- WHY_LINT_REAL_GAPS_NEXT
- WHY_LINT_RULE_REFINEMENT_LATER

## 19_TO_REMEMBER
Memory Bricks candidats :
- La remédiation doit rester séparée de la correction.
- Les vrais gaps documentaires doivent être distingués du bruit V1.
- Les rapports WHY lint peuvent produire de la self-reference à traiter explicitement.
- Le prochain GO recommandé est `GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_V1_01`, pas un auto-fix.
