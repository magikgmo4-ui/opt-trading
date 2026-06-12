# GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_TRIAGE_V1_01

## 1_MASTER_TARGET

Trier les findings du scan V1 WHY lint sans correction automatique.

Le rapport V1 canonique a documente le premier scan reel avec 30 fichiers
scannes, 1 fichier ignore et 113 findings. La relance obligatoire de ce GO,
faite apres merge de PR #431, scanne aussi le rapport V1 nouvellement merge dans
le dossier parent WHY lint. Le resultat courant est donc 31 fichiers scannes,
1 fichier ignore et 114 findings. L'ecart est lui-meme classe comme bruit V1
auto-referentiel a traiter dans la baseline.

## WHY

Ce triage existe pour classer les findings du premier scan reel avant toute
mutation documentaire, afin de separer vrais gaps, bruit V1, exceptions et
besoins d'ajustement du validateur.

## 2_INITIAL_PROJECT_DOC

References documentaires :

- SPEC parent :
  `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md`
- Scan spec :
  `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md`
- Scan implementation V1 :
  `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_V1_01.md`
- Scan report V1 :
  `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01.md`
- Commande `--scan-docs` :
  `python tools/why_lint_static_validator/why_lint_static_validator.py --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`

## 3_INITIAL_NEED

Le scan V1 a produit 113 findings dans le rapport canonique. Il faut distinguer :

- ce qui est un vrai gap documentaire ;
- ce qui est du bruit de regle V1 ;
- ce qui doit devenir exception documentee ;
- ce qui exige une amelioration du validateur ;
- ce qui doit etre corrige plus tard dans un GO dedie.

La relance apres PR #431 ajoute 1 finding sur le rapport V1 lui-meme. Cette
donnee confirme que la baseline doit preceder toute extension du scan.

## 4_MASTER_PROJECT_PLAN

Etapes :

1. relancer scan V1 ;
2. capturer la sortie texte et JSON ;
3. regrouper les findings par fichier ;
4. regrouper les findings par `finding_id` ;
5. classer chaque famille de findings ;
6. definir une politique de traitement ;
7. recommander les prochains GO ;
8. ne modifier aucun document scanne.

## 6_FINAL_TARGET

Produire un rapport de triage V1 classant les findings en categories
actionnables, sans correction automatique et sans mutation documentaire.

## 7_CANONICAL_STATE

Etat etabli :

- PR #431 mergee ;
- scan report V1 canonique ;
- scan V1 disponible ;
- scan V1 read-only/report-only ;
- rapport V1 canonique : 30 fichiers scannes, 1 fichier ignore, 113 findings ;
- relance courante apres PR #431 : 31 fichiers scannes, 1 fichier ignore,
  114 findings ;
- exit 1 attendu ;
- aucun crash ;
- aucun fichier modifie par le scan.

## 8_VALIDATED_PLAN

Plan de ce GO :

- executer scan ;
- analyser rapport ;
- documenter triage ;
- ne pas corriger ;
- ne pas modifier outil/tests/docs scannees.

## 9_SELECTED_SOLUTION

Rapport Markdown unique avec :

- resume ;
- regroupement par fichier ;
- regroupement par type ;
- classification ;
- decision ;
- prochain GO.

## 10_SELECTED_SETUP

Fichier :

`docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_TRIAGE_V1_01.md`

## 11_KEY_DECISIONS

- Findings != erreurs de runtime.
- Findings != autorisation de correction.
- Exit 1 = comportement attendu lorsque des findings sont presents.
- Triage avant correction.
- Aucune correction dans ce GO.
- Les regles V1 peuvent produire du bruit structurel.
- Les corrections futures doivent etre separees par categorie.
- Le finding supplementaire sur le rapport V1 apres PR #431 doit etre traite
  comme cas de baseline, pas comme permission de modifier le rapport.

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
- findings require triage before action

## 13_ESTABLISHED

Resultats reels de validation :

- help OK ;
- fixtures OK : 40/40 match, exit 0 ;
- scan report V1 canonique : 30 scanned, 1 skipped, 113 findings, exit 1 ;
- scan V1 relance apres PR #431 : 31 scanned, 1 skipped, 114 findings, exit 1 ;
- pytest : 20 passed ;
- worktree clean apres scan et avant creation de ce rapport ;
- 0 mutation par le scan.

## 14_HYPOTHESIS

A valider :

- une partie des findings vient probablement de documents volontairement
  incomplets ;
- une partie vient probablement de regles V1 trop strictes ;
- certains documents peuvent necessiter des exceptions ;
- certains gaps sont probablement reels et a corriger dans des GO dedies ;
- le seuil de bruit V1 doit etre mesure avant extension repo-wide ;
- les documents de rapport ajoutes au dossier parent peuvent creer du bruit
  auto-referentiel tant qu'aucune regle d'exclusion ou baseline n'existe.

## 15_REMAINING_GAP

- findings non corriges ;
- pas encore de baseline acceptee ;
- pas encore de seuils ;
- pas encore de regles d'exception ;
- pas encore de rapport par fichier automatise ;
- pas encore de scan repo-wide ;
- pas encore de correction documentaire ;
- pas encore de CI.

## 16_TODO

Suite recommandee :

1. merger ce rapport de triage ;
2. ouvrir un GO de baseline V1 ;
3. isoler bruit V1 vs vrais gaps ;
4. ouvrir ensuite des GO de correction documentaire ciblee ;
5. ajuster les regles seulement apres preuve de bruit.

## 17_RESUME_POINT

Apres merge :

`GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_BASELINE_V1_01`

Objectif :

Creer une baseline V1 acceptee des findings, avec classification des vrais gaps,
bruit, exceptions et regles a ajuster.

## 18_TO_DOCUMENT

TAGS :

- WHY_LINT_REAL_DOCS_SCAN_TRIAGE_V1
- WHY_LINT_FINDINGS_TRIAGE
- WHY_LINT_BASELINE_NEXT
- WHY_LINT_NO_AUTOFIX
- WHY_LINT_READONLY_REPORT

## 19_TO_REMEMBER

Memory Bricks candidats :

- Le premier scan reel WHY lint a produit 113 findings, exit 1 attendu.
- La relance apres PR #431 produit 114 findings car le rapport V1 est desormais
  inclus dans le dossier scanne.
- Les findings ne doivent pas etre corriges automatiquement.
- La prochaine etape est une baseline V1, pas une correction directe.

## Scan command

```bash
python tools/why_lint_static_validator/why_lint_static_validator.py \
  --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
```

## Validation summary

| Check | Resultat | Interpretation |
| --- | --- | --- |
| `--help` | OK, exit 0 | CLI disponible. |
| Fixture corpus | 40/40 match, exit 0 | Le mode fixtures reste conforme. |
| Scan V1 text | 31 scanned, 1 skipped, 114 findings, exit 1 | Findings presents ; pas un crash. L'ecart vs 113 vient du rapport V1 merge. |
| Scan V1 JSON | 31 scanned, 1 skipped, 114 findings, exit 1 | JSON exploite pour les regroupements par type et par fichier. |
| `pytest` | 20 passed, exit 0 | Tests outil OK. |
| Worktree | Clean apres scan, avant creation du rapport | Le scan n'a modifie aucun fichier. |

## Scan summary

| Metric | Value |
| --- | --- |
| scanned_files | 31 |
| skipped_files | 1 |
| findings | 114 |
| exit_code | 1 |
| status | FINDINGS_PRESENT |
| canonical_report_v1_scanned_files | 30 |
| canonical_report_v1_findings | 113 |
| current_delta | +1 scanned file, +1 finding after PR #431 |

## Findings by type

| finding_id | count | preliminary_classification | suggested_action |
| --- | ---: | --- | --- |
| APPLY_PATCH_ENABLED | 3 | V1_NOISE | Treat as example/code-fence noise until a parser can distinguish forbidden active config from documented invalid examples. |
| AUTOFIX_ENABLED | 3 | V1_NOISE | Keep no-autofix invariant ; refine detection before changing docs. |
| CI_BLOCKING_ENABLED | 3 | V1_NOISE | Preserve no-CI-blocking invariant ; baseline examples separately from active policy. |
| EXECUTE_COMMAND_ENABLED | 3 | V1_NOISE | Treat as documented forbidden runtime example unless baseline proves active permission text. |
| MISSING_FINAL_TARGET | 23 | NEED_MORE_EVIDENCE | Determine whether legacy thematic docs must adopt GO skeleton markers or become documented exceptions. |
| MISSING_INVARIANTS | 23 | NEED_MORE_EVIDENCE | Review document class before requiring `12_INVARIANTS` everywhere. |
| MISSING_RESUME_POINT | 23 | NEED_MORE_EVIDENCE | Decide if resume points apply to legacy architecture docs or only GO reports/specs. |
| MISSING_WHY_SECTION | 30 | NEED_MORE_EVIDENCE | Split true WHY gaps from rule strictness around exact `## WHY` headings and generated reports. |
| RUNTIME_BINDING_ENABLED | 3 | V1_NOISE | Preserve no-runtime invariant ; refine scanner to ignore explicit negative-test examples. |

## Findings by file

| file | findings_count | dominant_finding_type | preliminary_action |
| --- | ---: | --- | --- |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/00_CONSOLIDATION_MAP_01.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: classify as legacy map vs GO skeleton requirement. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/00_INITIAL_PROJECT_DOC.md` | 1 | MISSING_WHY_SECTION | NEED_MORE_EVIDENCE: decide whether initial project docs need exact `## WHY`. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/01_IMPLEMENTATION_MASTER_PLAN_4_AXES_01.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: likely legacy plan template gap or exception. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/02_NO_DUPLICATION_BOUNDARY_MATRIX_01.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: structural governance doc may need exception. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/03_EXISTING_SOURCE_MANIFEST_01.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: manifest type should be classified before correction. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/04_DEPENDENCY_GRAPH_4_AXES_01.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: graph doc may require exception or template update. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/05_WHY_LINT_WARNING_MODEL_01.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: warning model may be a real gap or V1 marker overreach. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/06_CROSS_AXIS_GATE_BINDING_01.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: gate binding doc should be reviewed as canonical source. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/07_AXIS_IMPLEMENTATION_ROADMAP_01.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: roadmap class needs baseline decision. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/10_LINT_SCOPE.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: legacy lint scope doc likely predates GO skeleton. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/100_LINT_REPORTING_ARCHITECTURE.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: architecture doc may need documented exception. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/110_LINT_CI_EXPERIMENT_PREPARATION.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: CI preparation doc requires careful no-CI-blocking review. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/120_LINT_WORKER_INTEGRATION_ROADMAP.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: roadmap doc needs class decision. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/130_LINT_ARCHITECTURE_SYNTHESIS.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: synthesis doc may be exception. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/140_CLOSEOUT.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: closeout format should be checked before edits. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/20_LINT_WARNING_LEVELS.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: legacy rule doc may require exception. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/30_LINT_DOCUMENT_TARGETS.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: target doc class not yet baselined. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/40_LINT_GAP_DETECTION_RULES.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: rule doc should not be edited before baseline. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/50_LINT_RUNTIME_GOVERNANCE_RULES.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: runtime governance wording requires triage, not autofix. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/60_LINT_HUMAN_REVIEW_RULES.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: review-rule doc may need exception or template. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/70_LINT_OBSERVABILITY_RULES.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: observability doc class needs baseline. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/80_LINT_RUNTIME_CLASS_ALIGNMENT.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: runtime alignment doc should be reviewed separately. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/90_CLOSEOUT_OPENING_01.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: closeout/opening hybrid needs class decision. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/90_LINT_AUTONOMY_LIMITS.md` | 4 | MISSING_FINAL_TARGET | NEED_MORE_EVIDENCE: autonomy-limit doc may need exception. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_SPEC_REVIEW_01.md` | 1 | MISSING_WHY_SECTION | RULE_REFINEMENT_NEEDED: GO-style docs may express WHY without exact heading. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01.md` | 6 | APPLY_PATCH_ENABLED | V1_NOISE: negative examples and field names need code-fence/example awareness. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_V1_01.md` | 6 | APPLY_PATCH_ENABLED | V1_NOISE: implementation report contains forbidden terms as documented constraints. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01.md` | 1 | MISSING_WHY_SECTION | V1_NOISE: self-scan artifact introduced after PR #431. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md` | 1 | MISSING_WHY_SECTION | RULE_REFINEMENT_NEEDED: exact heading rule may be too narrow for numbered specs. |
| `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01.md` | 6 | APPLY_PATCH_ENABLED | V1_NOISE: spec contains invalid examples, not active permissions. |

Scanned file with no finding in the current run :

- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md`

Skipped file :

- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md`

## Triage policy

- Ne pas corriger dans ce GO.
- Ne pas modifier les documents scannes.
- Chaque correction doit avoir un GO dedie.
- Les regles V1 ne doivent pas etre assouplies sans preuve.
- Les exceptions doivent etre documentees.
- La baseline doit preceder toute extension repo-wide.
- Les findings de type runtime/autofix/CI dans des exemples doivent etre
  traites comme bruit V1 candidat, pas comme autorisation active.
- Les findings de marqueur manquant doivent etre baselines par type de document
  avant toute correction.

## Recommended next GO

`GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_BASELINE_V1_01`

Objectif :

Etablir une baseline validee des findings, en distinguant :

- la baseline canonique du rapport V1 initial : 113 findings ;
- la relance post-PR #431 : 114 findings ;
- les vrais gaps ;
- le bruit V1 ;
- les exceptions documentaires ;
- les regles a ajuster.

## Verdict

`PASS_REAL_DOCS_SCAN_TRIAGE_V1_DOC_ONLY`

## RISKS

- À qualifier.
