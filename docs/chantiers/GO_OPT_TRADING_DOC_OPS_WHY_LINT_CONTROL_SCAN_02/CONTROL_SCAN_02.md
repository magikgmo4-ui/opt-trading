# GO_OPT_TRADING_DOC_OPS_WHY_LINT_CONTROL_SCAN_02

## 1_MASTER_TARGET
Figer un controle WHY lint read-only post-PR #471 pour mesurer l'etat reel apres refinement des regles, sans auto-fix, sans correction documentaire et sans nouveau changement du validateur.

## 3_INITIAL_NEED
La sequence canonique a deja etabli que les `110 findings` restants du `CONTROL_SCAN_01` relevaient de `15 FALSE_POSITIVE` et `95 RULE_TOO_BROAD`, sans `TRUE_GAP` confirme ni ouverture justifiee de `V1_BATCH_02`.

Le besoin de ce GO est donc strictement de re-mesurer le scope apres `RULE_REFINEMENT_01`, puis de decider si le flux peut etre cloture ou s'il reste un bruit reel.

## 7_CANONICAL_STATE
- PR #437 mergee : remediation plan V1 canonique.
- PR #442 mergee : real gaps fix plan V1 canonique.
- PR #452 mergee : first manual WHY lint gap fix batch canonique.
- PR #457 mergee : first WHY lint V1 fix pass canonique.
- PR #461 mergee : `CONTROL_SCAN_01` canonique (`34 scanned / 1 skipped / 110 findings / exit 1`).
- PR #464 mergee : `FALSE_POSITIVE_TRIAGE_01` canonique (`FALSE_POSITIVE = 15`, `RULE_TOO_BROAD = 95`, `TRUE_GAP = 0`, `DEFER_TO_BATCH_02 = 0`).
- PR #471 mergee selon GitHub : `fix: refine WHY lint static validator rules`, merge commit `2d67acc37ee116c996a2e646b122109ae521103d`, merged at `2026-05-16T10:33:53Z`.
- Le diff attendu de PR #471 reste borne a 4 fichiers : `RULE_REFINEMENT_01.md`, `test_why_lint_static_validator.py`, `tools/why_lint_static_validator/README.md`, `tools/why_lint_static_validator/why_lint_static_validator.py`.

## 13_ESTABLISHED
- `git fetch origin sot/mainline` a mis a jour `origin/sot/mainline`, mais n'a pas expose l'objet Git `2d67acc...` ni les 4 changements de PR #471 dans l'historique localement fetchable.
- `gh pr view 471` confirme pourtant l'etat `MERGED`, la base `sot/mainline`, la head `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_01` et le merge commit `2d67acc37ee116c996a2e646b122109ae521103d`.
- La branche distante `origin/go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_01` contient exactement le diff attendu de 4 fichiers et a donc ete retenue, avec accord explicite, comme meilleur proxy disponible du post-PR #471 pour ce GO read-only.
- Branche de travail creee : `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_CONTROL_SCAN_02` depuis `origin/go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_01`.
- Suite de verification executee sans mutation du validateur ni des docs cibles du scan.
- Commande executee : `python -m pytest tests/why_lint_static_validator/test_why_lint_static_validator.py`
- Commande executee : `python tools/why_lint_static_validator/why_lint_static_validator.py --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`
- Commande executee : `python tools/why_lint_static_validator/why_lint_static_validator.py --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01 --format json`
- Resultat de test : `23 passed`.
- Resultat du scan read-only : `34 scanned / 1 skipped / 0 findings / exit 0`.

## SCAN_SOURCE
- Base Git effective du controle : `origin/go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_01`.
- Raison de cette base : `origin/sot/mainline` mis a jour localement ne rendait pas le merge commit PR #471 fetchable, alors que GitHub confirmait le merge et que la head branch exposait le diff attendu.
- Racine scannee : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`.
- Fichier ignore par le validateur : `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md`.
- Mode : read-only, report-only, sans auto-fix, sans correction documentaire, sans mutation d'index global.

## SCAN_METHOD
1. `git fetch origin` puis `git fetch origin sot/mainline`.
2. Verification de l'historique local, de la visibilite du merge commit `2d67acc...` et du diff attendu de PR #471.
3. Verification GitHub via `gh pr view 471 --json number,state,baseRefName,headRefName,mergeCommit,mergedAt,title`.
4. Creation de `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_CONTROL_SCAN_02` depuis `origin/go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_01`.
5. Execution des tests unitaires WHY lint sur le validateur raffine.
6. Re-execution du scan WHY lint en texte puis en JSON, sans auto-fix.
7. Aucun document sous `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01` n'a ete modifie dans ce GO.
8. Aucun changement supplementaire du validateur n'a ete effectue dans ce GO.

## SCAN_RESULT

| Metric | Value |
| --- | ---: |
| scanned_files | 34 |
| skipped_files | 1 |
| findings | 0 |
| exit_code | 0 |
| status | PASS |

Lecture du resultat :
- le scan post-refinement est propre ;
- aucun finding residuel n'est observe dans le scope canonique WHY lint ;
- aucun auto-fix n'a ete lance ;
- aucune correction documentaire n'a ete appliquee ;
- aucun nouveau changement du validateur n'a ete introduit pour obtenir ce resultat.

## DELTA_VS_CONTROL_SCAN_01
Reference : `CONTROL_SCAN_01 = 34 scanned / 1 skipped / 110 findings / exit 1`.

| Metric | Control scan 01 | Control scan 02 | Delta |
| --- | ---: | ---: | ---: |
| scanned_files | 34 | 34 | 0 |
| skipped_files | 1 | 1 | 0 |
| findings | 110 | 0 | -110 |
| exit_code | 1 | 0 | -1 |

Lecture du delta :
- le scope scanne est strictement identique ;
- les `110 findings` restants du controle precedent ont disparu ;
- aucune regression nouvelle n'apparait au passage ;
- le raffinement de regles produit l'effet attendu sans remediation documentaire.

## DELTA_VS_FALSE_POSITIVE_TRIAGE_01
Reference : `FALSE_POSITIVE_TRIAGE_01 = FALSE_POSITIVE 15 / RULE_TOO_BROAD 95 / TRUE_GAP 0 / DEFER_TO_BATCH_02 0`.

| Triage class | Triage 01 | Control scan 02 | Delta |
| --- | ---: | ---: | ---: |
| FALSE_POSITIVE | 15 | 0 active findings | -15 |
| RULE_TOO_BROAD | 95 | 0 active findings | -95 |
| TRUE_GAP | 0 | 0 | 0 |
| DEFER_TO_BATCH_02 | 0 | 0 | 0 |

Lecture du delta :
- les `15 FALSE_POSITIVE` confirmes par triage ne remontent plus ;
- les `95 RULE_TOO_BROAD` ne remontent plus ;
- aucun `TRUE_GAP` n'apparait apres scan sur la base raffinee ;
- la decision de ne pas ouvrir `V1_BATCH_02` avant refinement etait correcte.

## DELTA_VS_RULE_REFINEMENT_01
Reference : `RULE_REFINEMENT_01` documentait `34 scanned / 1 skipped / 0 findings / exit 0` sur re-scan read-only.

| Metric | Rule refinement 01 | Control scan 02 | Delta |
| --- | ---: | ---: | ---: |
| scanned_files | 34 | 34 | 0 |
| skipped_files | 1 | 1 | 0 |
| findings | 0 | 0 | 0 |
| exit_code | 0 | 0 | 0 |

Conclusion : le controle post-merge reproduit exactement le resultat annonce par `RULE_REFINEMENT_01`. L'effet reel du raffinement est donc confirme sur le scope WHY lint, meme si la visibilite locale de `origin/sot/mainline` ne permettait pas d'attraper l'objet de merge annonce.

## 15_REMAINING_GAP
- `0` finding WHY lint reste ouvert dans le scope `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`.
- `0` `TRUE_GAP` documentaire est confirme apres scan sur base raffinee.
- `0` faux positif residuel n'est observe.
- `0` suivi `RULE_REFINEMENT_FOLLOWUP_01` n'est justifie par le resultat du scan.
- Point de vigilance hors lint : la visibilite Git locale de `origin/sot/mainline` et du merge commit `2d67acc...` reste incoherente avec les metadonnees GitHub, mais cela n'affecte pas la mesure read-only obtenue sur la head branch PR #471.

## 16_TODO
1. Ouvrir `GO_OPT_TRADING_DOC_OPS_WHY_LINT_CLOSEOUT_01`.
2. Ne pas ouvrir `GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_FOLLOWUP_01` : aucun faux positif residuel n'est mesure.
3. Ne pas ouvrir `GO_OPT_TRADING_DOC_OPS_WHY_LINT_TRUE_GAP_PLAN_01` : aucun vrai gap n'est confirme.
4. Considerer une verification Git separee plus tard si l'ancestralite exacte de `sot/mainline` doit etre reconciliee avec le merge commit GitHub `2d67acc...`.

## 17_RESUME_POINT
Reprendre sur :

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_CLOSEOUT_01
```

Objectif immediat :
clore proprement la sequence WHY lint V1 puisque le control scan post-refinement est a `0 findings` sans remediation documentaire supplementaire.

## RISKS

- À qualifier.
