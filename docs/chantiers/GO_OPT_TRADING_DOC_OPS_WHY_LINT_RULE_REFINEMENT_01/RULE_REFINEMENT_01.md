# GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_01

## 1_MASTER_TARGET
Raffiner les regles WHY lint V1 a partir du triage canonique PR #464 pour absorber les `FALSE_POSITIVE` et `RULE_TOO_BROAD` confirmes, sans corriger les documents cibles ni quitter le mode read-only.

## WHY
Ce GO existe pour retirer le bruit de regle majoritaire avant tout nouveau batch documentaire et pour eviter de transformer des exemples, des specs outil ou des docs thematiques legacy en faux gaps canoniques.

## 2_INITIAL_PROJECT_DOC
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_FALSE_POSITIVE_TRIAGE_01/FALSE_POSITIVE_TRIAGE_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_CONTROL_SCAN_01/CONTROL_SCAN_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_PLAN_V1_01/REAL_GAPS_FIX_PLAN_V1_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/00_INITIAL_PROJECT_DOC.md`
- `tools/why_lint_static_validator/why_lint_static_validator.py`
- `tools/why_lint_static_validator/README.md`
- `tests/why_lint_static_validator/test_why_lint_static_validator.py`

## 3_INITIAL_NEED
Le triage canonique a etabli :
- `FALSE_POSITIVE = 15` sur 3 docs outil/spec a cause de champs interdits cites comme exemples ou contraintes ;
- `RULE_TOO_BROAD = 95` dont `92` sur 23 docs legacy soumis a tort au squelette GO numerote et `3` sur un matching `## WHY` trop strict ;
- `TRUE_GAP = 0` ;
- aucun `V1_BATCH_02` documentaire ne doit etre ouvert avant refinement de regles.

## 4_MASTER_PROJECT_PLAN
1. Borner les checks de marqueurs GO aux docs qui portent deja une structure GO numerotee.
2. Rendre la detection `WHY` moins stricte seulement pour la classe outil/spec `STATIC_VALIDATOR` justifiee par le triage.
3. Limiter les checks de champs interdits aux lignes actives hors code-fences et hors listes d'exemples.
4. Ajouter des tests unitaires minimaux.
5. Rejouer le scan read-only canonique et documenter le delta.

## 6_FINAL_TARGET
Diff minimal pret a etre relu, reliant chaque changement de regle a PR #464, avec scan read-only rejoue et sans mutation documentaire hors trace chantier.

## 7_CANONICAL_STATE
- PR #461 mergee : `CONTROL_SCAN_01` canonique (`34 scanned / 1 skipped / 110 findings / exit 1`).
- PR #464 mergee : `FALSE_POSITIVE_TRIAGE_01` canonique (`FALSE_POSITIVE = 15`, `RULE_TOO_BROAD = 95`, `TRUE_GAP = 0`).
- Le validateur WHY lint reste local, read-only, report-only, sans auto-fix et sans CI bloquante.

## 8_VALIDATED_PLAN
- Aucun document cible du parent WHY lint n'est corrige.
- Aucun auto-fix n'est ajoute.
- Aucun index global n'est modifie.
- Aucun elargissement repo-wide du scan n'est introduit.
- Le raffinement reste borne a la logique `--scan-docs` du validateur WHY lint.

## 9_SELECTED_SOLUTION
Raffinement retenu :
- appliquer les marqueurs GO numerotes uniquement aux docs qui portent deja des headings H2 numerotes ;
- accepter, pour les docs `STATIC_VALIDATOR` structures, le couple `1_MASTER_TARGET + 3_INITIAL_NEED` comme equivalent WHY documente ;
- detecter les champs interdits seulement sur des lignes de champs actives hors code-fences Markdown.

Justification directe par le triage :
- `92` findings provenaient d'une application trop large du squelette GO numerote a des docs thematiques legacy ;
- `3` findings provenaient d'un matching `## WHY` trop strict sur 3 docs outil/spec ;
- `15` findings provenaient d'exemples/negative lists/fences interpretes comme configuration vivante.

## 11_KEY_DECISIONS
- Les docs legacy thematiques restent scannes pour `runtime/autofix/CI/secret`, mais sortent des checks de marqueurs GO numerotes tant qu'ils n'exposent pas cette structure.
- L'equivalent WHY est borne a la famille `STATIC_VALIDATOR` citee dans le triage, pour ne pas masquer les futurs gaps WHY des autres docs structures.
- Les checks de champs interdits restent read-only/report-only et n'interpretent pas les exemples Markdown comme des bindings actifs.

## 12_INVARIANTS
- read-only
- report-only
- no auto-fix
- no target-doc remediation
- no runtime
- no CI blocking
- no global index mutation
- no scan scope expansion beyond WHY lint rule refinement

## 13_ESTABLISHED
Fichiers modifies :
- `tools/why_lint_static_validator/why_lint_static_validator.py`
- `tools/why_lint_static_validator/README.md`
- `tests/why_lint_static_validator/test_why_lint_static_validator.py`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_01/RULE_REFINEMENT_01.md`

Regles touchees :
- gating des marqueurs `WHY`, `FINAL_TARGET`, `12_INVARIANTS`, `17_RESUME_POINT` sur docs GO structures seulement ;
- assouplissement borne du check `WHY` pour les 3 docs `STATIC_VALIDATOR` structures identifies par le triage ;
- detection `AUTOFIX_ENABLED`, `RUNTIME_BINDING_ENABLED`, `CI_BLOCKING_ENABLED`, `EXECUTE_COMMAND_ENABLED`, `APPLY_PATCH_ENABLED` sur lignes actives hors code-fences.

Fixtures/corpus :
- aucune fixture Markdown canonique modifiee ;
- tests unitaires ajoutes pour la classe legacy, l'equivalent WHY `STATIC_VALIDATOR` et les exemples fenced/negative lists.

## 14_HYPOTHESIS
- Le parent WHY lint contient bien deux classes documentaires distinctes dans le scope V1 : docs GO structures et docs legacy thematiques.
- Les examples fenced ou listes negatives documentees ne doivent pas etre traites comme une configuration active du validateur.
- Si une future politique impose de migrer les docs legacy vers le squelette GO numerote, ce sera un GO documentaire separe et non un rollback implicite de ce raffinement.

## 15_REMAINING_GAP
- Aucun `TRUE_GAP` n'apparait apres absorption du bruit classe par PR #464.
- La decision de politique longue duree sur la migration eventuelle des docs legacy reste ouverte, mais elle ne bloque plus le scan V1 courant.
- Aucun `V1_BATCH_02` documentaire n'est justifie a l'issue de ce GO.

## SCAN_RESULT_POST_REFINEMENT
Commande reexecutee :

```text
python tools/why_lint_static_validator/why_lint_static_validator.py --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
```

Resultat :
- `34 scanned / 1 skipped / 0 findings / exit 0`

Delta versus `CONTROL_SCAN_01` :
- `findings: 110 -> 0` ;
- `scanned_files: 34 -> 34` ;
- `skipped_files: 1 -> 1`.

Lecture :
- `-15` absorbe les faux positifs examples/code-fences confirmes ;
- `-92` absorbe l'application abusive du squelette GO numerote aux docs legacy ;
- `-3` absorbe le matching WHY trop strict sur les docs `STATIC_VALIDATOR` structures ;
- aucun nouveau finding n'est ajoute.

## 16_TODO
1. Ouvrir `RULE_REFINEMENT_PR_01` avec ce diff minimal.
2. Ne pas ouvrir `V1_BATCH_02` tant qu'aucun nouveau `TRUE_GAP` n'est prouve sur une base rescanee.
3. Si une politique de migration des docs legacy devient necessaire plus tard, l'ouvrir comme GO documentaire dedie plutot que de re-elargir la regle V1.

## 17_RESUME_POINT
Reprendre sur :

```text
RULE_REFINEMENT_PR_01
```

Objectif immediat :
faire relire et merger le raffinement de regles WHY lint V1 maintenant que le scan read-only canonique n'expose plus de faux positifs ni de `RULE_TOO_BROAD` restants dans le scope PR #464.
