# GO_OPT_TRADING_DOC_OPS_WHY_LINT_CONTROL_SCAN_01

## 1_MASTER_TARGET
Figer un controle read-only post-merge apres PR #457 pour mesurer l'effet reel de la passe WHY lint V1 avant toute ouverture de `V1_BATCH_02`.

## WHY
Ce controle existe pour confirmer l'etat canonique apres merge, separer la mesure de toute correction supplementaire, et justifier le prochain GO a partir des resultats reels du scan.

## 2_INITIAL_PROJECT_DOC
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_PLAN_V1_01/REAL_GAPS_FIX_PLAN_V1_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_BATCH_01/README.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_V1_01/README.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_TRIAGE_V1_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_BASELINE_V1_01.md`
- `python tools/why_lint_static_validator/why_lint_static_validator.py --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`

## 3_INITIAL_NEED
La sequence canonique a deja produit une baseline V1, un plan de remediation, un batch manuel, puis une passe V1 ciblee mergee via PR #457.

Le besoin de ce GO est de mesurer l'etat reel apres merge sans corriger :
- gaps effectivement retires ;
- gaps restants ;
- bruit V1 encore present ;
- eventuels nouveaux gaps ;
- prochain GO justifie par le resultat observe.

## 6_FINAL_TARGET
Produire un rapport de controle read-only post-PR #457 avec un re-scan canonique, les deltas versus les etats V1 precedents, et une recommandation claire de suite sans mutation documentaire ni changement du validateur.

## 7_CANONICAL_STATE
- PR #437 mergee : remediation plan V1 canonique.
- PR #442 mergee : real gaps fix plan V1 canonique.
- PR #452 mergee : first manual WHY lint gap fix batch canonique.
- PR #457 mergee : first WHY lint V1 fix pass canonique, merge commit `da871ef2c37a7fe51b6d60e3faaae6c9be7e7423`.
- `sot/mainline` contient bien PR #457 dans son historique.
- `sot/mainline` a ensuite avance avec d'autres merges, mais le scope du scan WHY lint reste borne a `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`.
- Le validateur WHY lint reste read-only/report-only ; aucun autofix ; aucune CI bloquante.

## 13_ESTABLISHED
- Branche de controle creee : `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_CONTROL_SCAN_01`.
- Commande canonique relancee en texte et JSON, sans auto-fix.
- Scan courant : `34 scanned / 1 skipped / 110 findings / exit 1`.
- Le resultat courant est identique au resultat documente en fin de PR #457.
- Aucun nouveau gap n'apparait par rapport a la passe V1 mergee.
- Les six corrections WHY de PR #457 tiennent apres merge.
- Les findings restants se concentrent sur 23 docs legacy multi-marqueurs et 3 docs outil/spec a bruit V1.

## 14_HYPOTHESIS
- La classe "WHY isole a haute confiance" traitee par PR #457 est probablement epuisee dans ce scope.
- Le bloc legacy restant demande une decision de classe documentaire avant toute correction massive.
- Le bloc residuel sur les 3 docs outil/spec reste un candidat fort de faux positifs/examples noise V1.
- Un `V1_BATCH_02` identique a la passe precedente risque d'etre moins net et moins reviewable qu'un triage de faux positifs.

## 15_REMAINING_GAP
- 110 findings restent ouverts.
- 23 docs legacy cumulent encore `MISSING_WHY_SECTION`, `MISSING_FINAL_TARGET`, `MISSING_INVARIANTS` et `MISSING_RESUME_POINT`.
- 3 docs outil/spec cumulent encore `MISSING_WHY_SECTION` avec `AUTOFIX_ENABLED`, `APPLY_PATCH_ENABLED`, `EXECUTE_COMMAND_ENABLED`, `CI_BLOCKING_ENABLED` et `RUNTIME_BINDING_ENABLED` lies a des exemples ou a des contraintes documentees.
- Il ne reste plus de `MISSING_WHY_SECTION` isoles du meme type que ceux traites par PR #457.

## SCAN_INPUTS
- Base Git de travail : `sot/mainline` mis a jour depuis `origin/sot/mainline`, puis branche `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_CONTROL_SCAN_01`.
- Scan root : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`.
- Fichier explicitement ignore par le validateur : `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md`.
- Refs de comparaison : baseline V1 acceptee `31 / 1 / 114`, observation post-PR433 `32 / 1 / 115`, pre-fix V1 `34 / 1 / 116`, post-fix V1 `34 / 1 / 110`.

## SCAN_METHOD
1. `git fetch origin`
2. `git checkout sot/mainline`
3. `git pull --rebase origin sot/mainline`
4. verification de `git status --short` et `git log --oneline --decorate -10`
5. verification de la presence de PR #457 dans l'historique
6. creation de `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_CONTROL_SCAN_01`
7. relecture des surfaces canoniques de baseline, triage, remediation, batch 01 et fix V1
8. execution du scan read-only existant :

```text
python tools/why_lint_static_validator/why_lint_static_validator.py --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
python tools/why_lint_static_validator/why_lint_static_validator.py --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01 --format json
```

9. aucun auto-fix, aucune correction documentaire, aucun changement du validateur

Note de transparence : un fichier non suivi hors scope WHY lint etait deja present localement au debut du GO ; il a ete laisse intact et n'affecte ni le scan ni le diff Git cible de ce GO.

## SCAN_RESULT

| Metric | Value |
| --- | ---: |
| scanned_files | 34 |
| skipped_files | 1 |
| findings | 110 |
| exit_code | 1 |
| status | FINDINGS_PRESENT |

Comptage courant par `finding_id` :

| finding_id | count |
| --- | ---: |
| MISSING_WHY_SECTION | 26 |
| MISSING_FINAL_TARGET | 23 |
| MISSING_INVARIANTS | 23 |
| MISSING_RESUME_POINT | 23 |
| APPLY_PATCH_ENABLED | 3 |
| AUTOFIX_ENABLED | 3 |
| CI_BLOCKING_ENABLED | 3 |
| EXECUTE_COMMAND_ENABLED | 3 |
| RUNTIME_BINDING_ENABLED | 3 |

Fichiers scannes sans finding dans le controle courant :
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/00_INITIAL_PROJECT_DOC.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_SPEC_REVIEW_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_BASELINE_V1_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REMEDIATION_PLAN_V1_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_TRIAGE_V1_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md`

Interpretation :
- pas de regression post-merge ;
- les 6 corrections WHY de PR #457 restent effectives ;
- le bruit V1 attendu sur les 3 docs outil/spec reste present ;
- aucun nouveau finding de self-reference n'apparait dans ce GO de controle.

## DELTA_VS_BASELINE_V1
Reference retenue : `ACCEPTED_BASELINE_V1_CURRENT = 31 scanned / 1 skipped / 114 findings`.

| Metric | Baseline V1 current | Control scan 01 | Delta |
| --- | ---: | ---: | ---: |
| scanned_files | 31 | 34 | +3 |
| skipped_files | 1 | 1 | 0 |
| findings | 114 | 110 | -4 |

Lecture du delta :
- le scope scanne a grandi de 3 artefacts canoniques mergés (`triage`, `baseline`, `remediation plan`) ;
- malgre ce scope plus large, le total baisse de 4 findings ;
- le controle est donc meilleur que la baseline V1 acceptee, sans regression cachee.

Reference additionnelle utile : versus la baseline V1 initiale `30 / 1 / 113`, le controle courant est `+4 scanned / -3 findings`.

## DELTA_VS_POST_BATCH_01
Reference retenue : etat pre-fix V1 documente au debut de PR #457, soit `34 scanned / 1 skipped / 116 findings / exit 1`.

| Metric | Post batch 01 | Control scan 01 | Delta |
| --- | ---: | ---: | ---: |
| scanned_files | 34 | 34 | 0 |
| skipped_files | 1 | 1 | 0 |
| findings | 116 | 110 | -6 |

Lecture du delta :
- le scope est strictement identique ;
- l'amelioration mesuree est exactement `-6 findings` ;
- les 6 findings retires correspondent aux 6 `MISSING_WHY_SECTION` corriges dans PR #457 sur :
  - `GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_SPEC_REVIEW_01.md`
  - `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md`
  - `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01.md`
  - `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_TRIAGE_V1_01.md`
  - `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_BASELINE_V1_01.md`
  - `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REMEDIATION_PLAN_V1_01.md`

## DELTA_VS_POST_FIX_V1
Reference retenue : resultat final documente par PR #457, soit `34 scanned / 1 skipped / 110 findings / exit 1`.

| Metric | Post fix V1 | Control scan 01 | Delta |
| --- | ---: | ---: | ---: |
| scanned_files | 34 | 34 | 0 |
| skipped_files | 1 | 1 | 0 |
| findings | 110 | 110 | 0 |

Conclusion : le merge n'a ni degrade ni ameliore artificiellement la mesure. Le controle reproduit exactement l'etat final annonce par PR #457.

## RISKS
- Les 23 docs legacy restants ne sont pas des quick wins comparables a PR #457 ; ils cumulent 4 marqueurs manquants chacun.
- Les 9 findings runtime/autofix/CI/apply-patch sur 3 docs outil/spec restent probablement du bruit V1, mais ils ne sont pas reclasses dans ce GO de mesure.
- `sot/mainline` a avance apres PR #457 ; le controle reste valide car le scan est borne au parent WHY lint et le resultat reproduit exactement le post-fix V1 attendu.
- Un fichier local non suivi hors scope etait present au depart ; il est reste hors de ce GO.

## 16_TODO
1. Ouvrir `FALSE_POSITIVE_TRIAGE_01` en priorite pour figer le traitement des 3 docs outil/spec encore bruyants.
2. Ne pas ouvrir `V1_BATCH_02` immediatement sur le meme modele que PR #457 : il ne reste plus de `MISSING_WHY_SECTION` isoles a haute confiance dans ce scope.
3. Revenir ensuite sur un lot de remediation seulement apres decision explicite sur :
   - les 23 docs legacy multi-marqueurs ;
   - les faux positifs/examples noise V1 ;
   - les eventuelles exceptions documentaires.
4. Ne pas cloturer temporairement la remediation V1 : 110 findings restent ouverts.

## 17_RESUME_POINT
Reprendre sur :

```text
FALSE_POSITIVE_TRIAGE_01
```

Objectif immediat :
mesurer et classer le bruit V1 restant sur les 3 docs outil/spec avant tout nouveau batch de correction documentaire.
