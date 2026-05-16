# GO_OPT_TRADING_DOC_OPS_WHY_LINT_FALSE_POSITIVE_TRIAGE_01

## 1_MASTER_TARGET
Qualifier les 110 findings restants du controle WHY lint post-PR #457 afin de separer faux positifs confirmes, regles V1 trop larges, vrais gaps encore non prouves et cas a ne pas corriger avant tout `V1_BATCH_02`.

## WHY
Ce triage existe pour eviter une nouvelle passe documentaire sur des signaux mal qualifies et pour justifier le prochain GO a partir du bruit reel du scan canonique `34 scanned / 1 skipped / 110 findings / exit 1`.

## 3_INITIAL_NEED
Le controle canonique merge via PR #461 a confirme l'etat post-fix V1 :
- PR #457 tient apres merge ;
- aucun nouveau gap n'apparait ;
- il ne reste plus de `MISSING_WHY_SECTION` isoles du meme type que la passe V1.

Il faut donc qualifier les 110 findings restants avant toute correction supplementaire, sinon `V1_BATCH_02` risquerait de corriger du bruit de regle ou des docs legacy hors classe documentaire stabilisee.

## 7_CANONICAL_STATE
- PR #437 mergee : remediation plan V1 canonique.
- PR #442 mergee : real gaps fix plan V1 canonique.
- PR #452 mergee : first manual WHY lint gap fix batch canonique.
- PR #457 mergee : first WHY lint V1 fix pass canonique, merge commit `da871ef2c37a7fe51b6d60e3faaae6c9be7e7423`.
- PR #461 mergee : control scan 01 canonique, merge commit `ddaac2e3`.
- `sot/mainline` contient bien PR #461.
- Le validateur WHY lint reste read-only/report-only ; aucun auto-fix ; aucun changement outil dans ce GO.

## 13_ESTABLISHED
- Rebase locale sur `origin/sot/mainline` effectue avant triage.
- Branche dediee creee : `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_FALSE_POSITIVE_TRIAGE_01`.
- Relecture des artefacts canoniques `CONTROL_SCAN_01`, baseline V1, triage V1, remediation plan V1, batch 01 et fix V1.
- Re-execution read-only du scan WHY lint sur le parent experimental : `34 scanned / 1 skipped / 110 findings / exit 1`.
- La repartition observee reste stable :
  - `MISSING_WHY_SECTION = 26`
  - `MISSING_FINAL_TARGET = 23`
  - `MISSING_INVARIANTS = 23`
  - `MISSING_RESUME_POINT = 23`
  - `APPLY_PATCH_ENABLED = 3`
  - `AUTOFIX_ENABLED = 3`
  - `CI_BLOCKING_ENABLED = 3`
  - `EXECUTE_COMMAND_ENABLED = 3`
  - `RUNTIME_BINDING_ENABLED = 3`
- Les 8 fichiers deja propres au `CONTROL_SCAN_01` le restent ; aucune regression n'est apparue.

## 14_HYPOTHESIS
- La majorite des findings restants ne decrit plus un lot de correction documentaire simple, mais un probleme de granularite des regles V1 appliquees a des docs legacy ou a des exemples interdits documentes.
- Les 15 findings sur les 3 docs outil/spec sont des faux positifs confirmes ou quasi confirmes par contexte.
- Les 95 autres findings relevent principalement d'un scope de regle trop large ou d'un matching trop strict sur des marqueurs exacts.
- Le prochain GO utile n'est pas `V1_BATCH_02`, mais un GO de refinement de regles ou de cadrage d'exceptions documentaires.

## 15_REMAINING_GAP
- 110 findings restent ouverts au niveau du scan brut.
- 0 vrai gap a haute confiance n'est confirme pour un nouveau batch documentaire immediat.
- Le validateur V1 n'est pas encore aware des classes documentaires legacy ni du contexte exemple/code-fence.
- Une decision de politique reste necessaire sur le traitement des docs thematiques du parent WHY lint qui ne suivent pas le squelette GO numerote.

## SCAN_SOURCE
- Rapport canonique de controle : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_CONTROL_SCAN_01/CONTROL_SCAN_01.md`
- Merge commit canonique de PR #461 : `ddaac2e3`
- Commande de reference :

```text
python tools/why_lint_static_validator/why_lint_static_validator.py --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
```

- Re-verification locale dans ce GO : meme resultat que `CONTROL_SCAN_01`, soit `34 scanned / 1 skipped / 110 findings / exit 1`.

## TRIAGE_METHOD
1. Reprendre le comptage canonique de `CONTROL_SCAN_01`.
2. Reutiliser le triage V1 precedent comme point de depart, sans lui accorder de valeur canonique automatique.
3. Re-executer le scan read-only pour confirmer la stabilite du `34 / 1 / 110`.
4. Inspecter des docs representatives :
   - docs thematiques legacy (`00_CONSOLIDATION_MAP_01.md`, `10_LINT_SCOPE.md`) ;
   - docs outil/spec encore bruyants (`...IMPLEMENTATION_READONLY_01.md`, `...REAL_DOCS_SCAN_IMPLEMENTATION_V1_01.md`, `...STATIC_VALIDATOR_SPEC_01.md`).
5. Classer les findings par cause racine, pas seulement par `finding_id`.
6. Ne corriger aucun document, ne pas modifier le validateur, ne pas changer d'index global.

## FINDINGS_SUMMARY

| Category | Count | Current conclusion |
| --- | ---: | --- |
| TRUE_GAP | 0 | Aucun vrai gap a haute confiance n'est confirme pour un batch documentaire immediat. |
| FALSE_POSITIVE | 15 | Faux positifs confirmes sur 3 docs outil/spec a cause de champs interdits cites comme exemples ou contraintes. |
| RULE_TOO_BROAD | 95 | Regles V1 trop larges ou trop strictes sur docs legacy et sur le matching exact de `## WHY`. |
| NEEDS_HUMAN_DECISION | 0 direct finding | Une decision de politique reste necessaire, mais elle porte sur la classe documentaire, pas sur un finding isole a corriger. |
| ALREADY_FIXED_OR_OBSOLETE | 0 current | Les 6 findings corriges par PR #457 ne font deja plus partie des 110 restants. |
| DEFER_TO_BATCH_02 | 0 | Aucun finding n'est suffisamment net pour ouvrir `V1_BATCH_02` maintenant. |

Total classifie : `15 + 95 = 110`.

## FALSE_POSITIVES
Findings concernes : `15`.

Perimetre :
- `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01.md`
- `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_V1_01.md`
- `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01.md`

Finding IDs concernes :
- `APPLY_PATCH_ENABLED`
- `AUTOFIX_ENABLED`
- `CI_BLOCKING_ENABLED`
- `EXECUTE_COMMAND_ENABLED`
- `RUNTIME_BINDING_ENABLED`

Justification explicite :
- `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01.md:144-145` cite les champs interdits comme contraintes de validation, pas comme permission active.
- `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_V1_01.md:184-189` liste les checks interdits du scan V1, pas une configuration a appliquer.
- `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01.md:399-414` documente des champs invalides dans une section de spec, pas un runtime vivant.

Conclusion : ces 15 findings doivent etre traites comme faux positifs confirmes du scan V1 courant. Leur cause technique immediate est l'absence de contexte exemple/code-fence/negative-example dans la detection.

## TRUE_GAPS_REMAINING
`0` vrai gap confirme a haute confiance pour un lot `V1_BATCH_02` immediat.

Raison :
- les 23 docs legacy restants ne remontent jamais un gap unique simple ; ils remontent un paquet de 4 marqueurs ensemble ;
- les 3 docs outil/spec restants sont meles a du bruit de regle deja confirme ;
- aucun finding restant n'a le profil propre et reviewable des 6 `MISSING_WHY_SECTION` corriges par PR #457.

## RULE_TOO_BROAD_CASES
Findings concernes : `95`.

### Bloc legacy thematique : 92 findings
23 docs legacy remontent chacun le meme paquet de 4 findings :
- `MISSING_WHY_SECTION`
- `MISSING_FINAL_TARGET`
- `MISSING_INVARIANTS`
- `MISSING_RESUME_POINT`

Docs concernes :
- `00_CONSOLIDATION_MAP_01.md`
- `01_IMPLEMENTATION_MASTER_PLAN_4_AXES_01.md`
- `02_NO_DUPLICATION_BOUNDARY_MATRIX_01.md`
- `03_EXISTING_SOURCE_MANIFEST_01.md`
- `04_DEPENDENCY_GRAPH_4_AXES_01.md`
- `05_WHY_LINT_WARNING_MODEL_01.md`
- `06_CROSS_AXIS_GATE_BINDING_01.md`
- `07_AXIS_IMPLEMENTATION_ROADMAP_01.md`
- `10_LINT_SCOPE.md`
- `20_LINT_WARNING_LEVELS.md`
- `30_LINT_DOCUMENT_TARGETS.md`
- `40_LINT_GAP_DETECTION_RULES.md`
- `50_LINT_RUNTIME_GOVERNANCE_RULES.md`
- `60_LINT_HUMAN_REVIEW_RULES.md`
- `70_LINT_OBSERVABILITY_RULES.md`
- `80_LINT_RUNTIME_CLASS_ALIGNMENT.md`
- `90_CLOSEOUT_OPENING_01.md`
- `90_LINT_AUTONOMY_LIMITS.md`
- `100_LINT_REPORTING_ARCHITECTURE.md`
- `110_LINT_CI_EXPERIMENT_PREPARATION.md`
- `120_LINT_WORKER_INTEGRATION_ROADMAP.md`
- `130_LINT_ARCHITECTURE_SYNTHESIS.md`
- `140_CLOSEOUT.md`

Justification explicite :
- `00_CONSOLIDATION_MAP_01.md:28-87` est une carte thematique avec `## Objet` et des invariants explicites en prose, pas un child GO numerote complet.
- `10_LINT_SCOPE.md:3-45` utilise `## Objectif`, `## Scope`, `## Hors scope`, `## Invariant`, ce qui exprime l'intention documentaire sans respecter les marqueurs exacts `WHY`, `FINAL_TARGET`, `12_INVARIANTS`, `17_RESUME_POINT`.

Conclusion : sur ces 23 docs, le validateur V1 applique trop largement le squelette GO numerote a des docs thematiques legacy du parent WHY lint.

### Bloc exact-heading WHY : 3 findings
Findings concernes : `3 x MISSING_WHY_SECTION` sur :
- `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01.md`
- `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_V1_01.md`
- `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01.md`

Justification explicite :
- ces trois docs exposent deja leur fonction via `## 1_MASTER_TARGET` et `## 3_INITIAL_NEED` ;
- la regle V1 ne reconnait qu'un heading exact `## WHY` ;
- apres PR #457, ce sont les seuls `MISSING_WHY_SECTION` restants hors bloc legacy et ils ne sont pas isoles du bruit de regle sur les memes fichiers.

Conclusion : ces 3 findings relevent d'une regle trop stricte sur le marquage WHY exact, pas d'un nouveau gap documentaire simple a corriger en batch.

## HUMAN_DECISION_NEEDED
Decision de politique restante :
- faut-il traiter les 23 docs thematiques du parent WHY lint comme une classe documentaire legitime avec exceptions documentees ;
- ou bien les migrer volontairement vers le squelette GO numerote complet.

Cette decision est reelle, mais elle ne justifie pas de corriger les 23 docs maintenant. Le triage courant montre d'abord un probleme de scope de regle, pas un lot de correction reviewable.

## DEFERRED_TO_BATCH_02
`0` finding est deferre vers `V1_BATCH_02` a ce stade.

Justification :
- aucun finding restant n'est un `MISSING_WHY_SECTION` isole a haute confiance ;
- ouvrir `V1_BATCH_02` maintenant reviendrait a corriger avant d'avoir stabilise les regles ou les exceptions documentaires ;
- le prochain GO doit d'abord traiter le bruit de regle majoritaire.

## DO_NOT_FIX
Dans ce GO : `110 / 110` findings sont `DO_NOT_FIX`.

Sens operationnel :
- ne pas corriger les 15 faux positifs confirmes ;
- ne pas corriger les 95 cas de regle trop large ou trop stricte avant refinement ;
- ne pas transformer le triage en remediation implicite ;
- ne pas modifier le validateur dans ce GO ;
- ne pas ouvrir de batch documentaire tant que la classification n'est pas absorbee par un GO dedie.

## 16_TODO
1. Ouvrir `GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_01` en priorite.
2. Y cadrer au minimum :
   - awareness des examples/code-fences/negative lists pour les champs interdits ;
   - scope explicite des marqueurs GO numerotes versus docs thematiques legacy ;
   - regle WHY moins stricte qu'un heading exact `## WHY` ou exceptions documentees equivalentes.
3. Refaire ensuite un control scan read-only canonique apres refinement.
4. Reevaluer seulement apres cela s'il reste un lot `V1_BATCH_02` reellement documentaire.

## 17_RESUME_POINT
Reprendre sur :

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_01
```

Objectif immediat :
reduire les 110 findings residuels en traitant d'abord les 15 faux positifs confirmes et les 95 cas de regle trop large, avant toute nouvelle correction documentaire.
