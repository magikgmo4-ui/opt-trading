---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01
doc_type: chantier_child_report
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01
chantier_parent: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: child_report
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-14
topic_keys:
  - why_lint
  - real_docs_scan
  - scan_report
  - findings_baseline
  - read_only
  - report_only
  - no_autofix
  - no_ci_blocking
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_V1_01.md
  - tools/why_lint_static_validator/README.md
---

# GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01

## 1_MASTER_TARGET

Documenter le premier scan réel V1 du validateur WHY lint sur le dossier parent
WHY lint.

Ce rapport capture les résultats du mode `--scan-docs` sans modifier les
documents scannés.

## WHY

Ce rapport existe pour figer le premier resultat reel du scan V1 avant toute
interpretation corrective, afin de separer collecte, triage et remediation sans
mutation documentaire.

## 2_INITIAL_PROJECT_DOC

Références :

- SPEC parent :
  `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md`
- scan spec :
  `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md`
- scan implementation V1 :
  `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_V1_01.md`
- README outil :
  `tools/why_lint_static_validator/README.md`
- commande exécutée :
  `python tools/why_lint_static_validator/why_lint_static_validator.py --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`

## 3_INITIAL_NEED

Le mode `--scan-docs` existe et doit produire un rapport lisible des findings
sans modifier les documents scannés.

Le besoin de ce GO est de documenter le premier résultat V1, de conserver les
métriques comme baseline documentaire et de préparer un triage séparé.

## 4_MASTER_PROJECT_PLAN

Étapes :

1. confirmer base Git ;
2. exécuter validations outil ;
3. exécuter scan V1 ;
4. capturer résumé ;
5. documenter findings ;
6. classer les findings ;
7. définir suite sûre ;
8. ne modifier aucun document scanné.

## 6_FINAL_TARGET

Produire un rapport documentaire du scan V1 indiquant :

- fichiers scannés ;
- fichiers ignorés ;
- findings ;
- exit code ;
- interprétation ;
- limites ;
- prochain GO ;

sans mutation documentaire.

## 7_CANONICAL_STATE

État établi :

- PR #429 mergée ;
- mode `--scan-docs` V1 disponible ;
- scan borné au dossier parent WHY lint ;
- read-only/report-only ;
- pas de CI ;
- pas d’autofix ;
- pas de scan repo-wide.

## 8_VALIDATED_PLAN

Plan de ce GO :

- exécuter le scan localement ;
- ne rien corriger ;
- écrire seulement le rapport ;
- ne pas modifier le validateur ;
- ne pas modifier les tests ;
- ne pas modifier les documents scannés.

## 9_SELECTED_SOLUTION

Rapport Markdown unique, localisé dans le dossier parent WHY lint.

Le rapport documente les résultats et prépare le triage, mais ne qualifie aucune
correction comme autorisée.

## 10_SELECTED_SETUP

Fichier rapport :

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01.md
```

Le scan documenté a été exécuté avant la création de ce fichier rapport. Ce
fichier n'était donc pas dans l'entrée du scan V1 capturée ci-dessous.

## 11_KEY_DECISIONS

- exit 1 = attendu si findings présents ;
- findings ≠ crash ;
- findings ≠ autorisation de correction automatique ;
- no autofix ;
- no source mutation ;
- triage futur séparé ;
- les métriques de ce rapport forment une baseline, pas un plan de correction.

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

Résultats établis :

- fixtures corpus : 40/40 match, exit 0
- scan V1 : 30 scanned, 1 skipped, 113 findings, exit 1
- pytest : 20 passed
- worktree clean
- no mutation

Le scan a terminé normalement. L'exit code `1` signifie `FINDINGS_PRESENT`.

## 14_HYPOTHESIS

À valider plus tard :

- plusieurs findings sont probablement structurels et attendus sur des docs
  anciennes ;
- certains findings peuvent être du bruit de V1 ;
- seuils de bruit à calibrer ;
- règles de scan à raffiner ;
- triage nécessaire avant correction.

## 15_REMAINING_GAP

- findings non triés individuellement ;
- pas encore de catégorie par fichier ;
- pas encore de décision sur corrections ;
- pas encore de baseline acceptée ;
- pas encore de seuils ;
- pas encore de mode report artifact automatisé ;
- pas encore de scan repo-wide.

## 16_TODO

Suite recommandée :

1. merger ce rapport ;
2. ouvrir un GO de triage des findings ;
3. classifier findings en :
   - vrais gaps ;
   - bruit V1 ;
   - exceptions documentaires ;
   - règles à ajuster ;
4. ne corriger aucun document avant triage.

## 17_RESUME_POINT

Après merge :

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_TRIAGE_V1_01
```

Objectif futur :
classifier les 113 findings sans correction automatique.

## 18_TO_DOCUMENT

TAGS :

- WHY_LINT_REAL_DOCS_SCAN_REPORT_V1
- WHY_LINT_FINDINGS_BASELINE
- WHY_LINT_READONLY_REPORT
- WHY_LINT_NO_AUTOFIX
- WHY_LINT_TRIAGE_NEXT

Blocs à extraire :

- `Scan command`
- `Validation summary`
- `Scan summary`
- `Findings summary`
- `Findings handling policy`
- `Next GO`

## 19_TO_REMEMBER

Memory Bricks candidats :

- Le premier scan réel V1 WHY lint a scanné 30 fichiers, ignoré 1 fichier et
  produit 113 findings.
- Exit 1 signifie findings présents, pas crash.
- Le scan V1 n’a modifié aucun fichier.
- Prochaine étape : triage V1, pas correction.

## Scan command

Commande exacte :

```text
python tools/why_lint_static_validator/why_lint_static_validator.py --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
```

## Validation summary

| Check | Résultat | Interprétation |
| --- | --- | --- |
| `--help` | OK | CLI disponible ; `--fixtures` et `--scan-docs` exposés. |
| fixture corpus | 40/40 match, exit 0 | Le contrat fixtures reste valide. |
| `--scan-docs` | exit 1 | Scan terminé avec findings présents. |
| pytest | 20 passed | Tests unitaires V1 OK. |
| worktree | clean après scan | Le scan n'a modifié aucun fichier. |

## Scan summary

| Metric | Value |
| --- | --- |
| scanned_files | 30 |
| skipped_files | 1 |
| findings | 113 |
| exit_code | 1 |
| status | FINDINGS_PRESENT |

## Scanned files

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/00_CONSOLIDATION_MAP_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/00_INITIAL_PROJECT_DOC.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/01_IMPLEMENTATION_MASTER_PLAN_4_AXES_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/02_NO_DUPLICATION_BOUNDARY_MATRIX_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/03_EXISTING_SOURCE_MANIFEST_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/04_DEPENDENCY_GRAPH_4_AXES_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/05_WHY_LINT_WARNING_MODEL_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/06_CROSS_AXIS_GATE_BINDING_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/07_AXIS_IMPLEMENTATION_ROADMAP_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/100_LINT_REPORTING_ARCHITECTURE.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/10_LINT_SCOPE.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/110_LINT_CI_EXPERIMENT_PREPARATION.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/120_LINT_WORKER_INTEGRATION_ROADMAP.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/130_LINT_ARCHITECTURE_SYNTHESIS.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/140_CLOSEOUT.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/20_LINT_WARNING_LEVELS.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/30_LINT_DOCUMENT_TARGETS.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/40_LINT_GAP_DETECTION_RULES.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/50_LINT_RUNTIME_GOVERNANCE_RULES.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/60_LINT_HUMAN_REVIEW_RULES.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/70_LINT_OBSERVABILITY_RULES.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/80_LINT_RUNTIME_CLASS_ALIGNMENT.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/90_CLOSEOUT_OPENING_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/90_LINT_AUTONOMY_LIMITS.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_SPEC_REVIEW_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_V1_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md
```

## Skipped files

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md
```

## Findings summary

| Finding ID | Count | Report verdict |
| --- | ---: | --- |
| MISSING_WHY_SECTION | 29 | NEED_MORE_EVIDENCE |
| MISSING_FINAL_TARGET | 23 | NEED_MORE_EVIDENCE |
| MISSING_INVARIANTS | 23 | NEED_MORE_EVIDENCE |
| MISSING_RESUME_POINT | 23 | NEED_MORE_EVIDENCE |
| AUTOFIX_ENABLED | 3 | FAIL_AUTOFIX_ENABLED |
| APPLY_PATCH_ENABLED | 3 | FAIL_AUTOFIX_ENABLED |
| RUNTIME_BINDING_ENABLED | 3 | FAIL_RUNTIME_BINDING_ENABLED |
| EXECUTE_COMMAND_ENABLED | 3 | FAIL_RUNTIME_BINDING_ENABLED |
| CI_BLOCKING_ENABLED | 3 | FAIL_CI_BLOCKING_ENABLED |

Summary by verdict:

| Verdict | Count |
| --- | ---: |
| NEED_MORE_EVIDENCE | 98 |
| FAIL_AUTOFIX_ENABLED | 6 |
| FAIL_RUNTIME_BINDING_ENABLED | 6 |
| FAIL_CI_BLOCKING_ENABLED | 3 |

## Interpretation

Exit `1` est attendu pour ce scan V1, car des findings sont présents.

Ce n'est pas un crash :

- le scan a produit un rapport déterministe ;
- les fixtures restent valides ;
- les tests unitaires passent ;
- aucun fichier source n'a été modifié ;
- aucune correction automatique n'a été appliquée.

Les 113 findings constituent une première baseline brute. Ils doivent être
triés avant toute action, car V1 est volontairement simple et peut inclure du
bruit documentaire sur des fichiers anciens ou hors structure GO complète.

## Findings handling policy

- ne pas corriger automatiquement ;
- ne pas modifier les docs scannées dans ce GO ;
- chaque correction future exige GO dédié ou triage explicite ;
- findings ne sont pas des permissions ;
- findings ne bloquent pas la CI ;
- les corrections futures doivent remonter au document ou à l'axe source, jamais
  à un autofix WHY lint ;
- le triage doit distinguer vrais gaps, bruit V1, exceptions documentaires et
  règles à ajuster.

## Limits

- Le rapport ne contient pas de décision de correction fichier par fichier.
- Le rapport ne transforme pas `FAIL_*` en blocage CI.
- Le scan est limité au parent WHY lint.
- Le fichier de rapport lui-même a été créé après le scan documenté.
- Aucun rapport JSON ou artifact automatisé n'est créé dans ce GO.

## Next GO

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_TRIAGE_V1_01
```

Objectif :

```text
Trier les 113 findings en catégories actionnables sans correction automatique.
```

## Verdict

```text
PASS_REAL_DOCS_SCAN_REPORT_V1_DOC_ONLY
```
