# GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_BASELINE_V1_01

## 1_MASTER_TARGET

Etablir une baseline V1 validee des findings du scan reel WHY lint.

## WHY

Cette baseline existe pour figer l'etat accepte des findings avant toute
correction, afin de distinguer les vrais gaps du bruit V1 et de garder la
remediation dans des GO separes.

## 2_INITIAL_PROJECT_DOC

References :

- SPEC parent :
  `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md`
- scan spec :
  `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md`
- scan implementation V1 :
  `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_IMPLEMENTATION_V1_01.md`
- scan report V1 :
  `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01.md`
- triage report V1 :
  `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_TRIAGE_V1_01.md`
- commande `--scan-docs` :
  `python tools/why_lint_static_validator/why_lint_static_validator.py --scan-docs docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`

## 3_INITIAL_NEED

Le scan V1 produit des findings documentes. Il faut maintenant figer une
baseline acceptee afin de :

- distinguer les findings attendus ;
- isoler le bruit V1 ;
- identifier les vrais gaps ;
- definir les exceptions documentees ;
- preparer les GO de correction ou d'ajustement futurs.

## 4_MASTER_PROJECT_PLAN

Etapes :

1. relancer le scan V1 ;
2. confirmer les metriques courantes ;
3. comparer avec la baseline initiale ;
4. documenter l'ecart auto-referentiel ;
5. etablir la baseline acceptee ;
6. classer les findings ;
7. definir la politique d'acceptation ;
8. definir les prochains GO ;
9. ne corriger aucun document.

## 6_FINAL_TARGET

Produire une baseline V1 acceptee pour les findings du scan WHY lint, incluant :

- baseline initiale ;
- baseline courante ;
- ecart auto-referentiel ;
- classification des findings ;
- regles d'acceptation ;
- prochains GO ;

sans correction automatique ni mutation documentaire.

## 7_CANONICAL_STATE

Etat etabli :

- PR #433 mergee ;
- scan report V1 canonique ;
- triage V1 canonique ;
- validateur read-only/report-only ;
- aucun autofix ;
- aucun runtime ;
- aucun CI blocking ;
- baseline initiale : 30 / 1 / 113 ;
- baseline courante acceptee : 31 / 1 / 114 ;
- ecart initial explique par ajout du rapport V1 ;
- relance de collecte apres PR #433 : 32 / 1 / 115, expliquee par ajout du
  rapport de triage V1.

La baseline acceptee reste volontairement ancree sur les deux etats demandes :
initial V1 et current V1. La relance post-PR #433 est conservee comme preuve
que les rapports produits dans le dossier scanne generent du bruit
auto-referentiel tant qu'aucune politique d'exclusion n'est implementee.

## 8_VALIDATED_PLAN

Plan de ce GO :

- executer ou confirmer le scan ;
- comparer report V1 et triage V1 ;
- creer la baseline ;
- ne pas modifier les docs scannees ;
- ne pas modifier le validateur ;
- ne pas corriger.

## 9_SELECTED_SOLUTION

Creer un document Markdown unique de baseline V1.

La baseline devient la reference de comparaison avant :

- correction documentaire ;
- ajustement des regles ;
- extension repo-wide ;
- integration CI ;
- integration OpenClaw.

## 10_SELECTED_SETUP

Fichier :

`docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_BASELINE_V1_01.md`

## 11_KEY_DECISIONS

- Baseline initiale = 30 scanned / 1 skipped / 113 findings.
- Baseline courante acceptee = 31 scanned / 1 skipped / 114 findings.
- L'ecart +1/+1 initial est auto-referentiel : le rapport V1 est scanne apres
  son merge.
- La relance post-PR #433 observe 32 scanned / 1 skipped / 115 findings car le
  rapport de triage V1 est aussi scanne.
- La baseline ne corrige rien.
- Les findings ne sont pas des permissions.
- Les corrections futures exigent un GO dedie.
- Les regles V1 ne doivent pas etre assouplies sans preuve.
- Les rapports de scan ajoutes au dossier parent doivent etre traites comme
  source de bruit V1 jusqu'a decision explicite d'exclusion ou de baseline.

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
- baseline is not correction
- baseline precedes remediation

## 13_ESTABLISHED

Resultats etablis :

- help OK ;
- fixtures OK : 40/40 match, exit 0 ;
- scan V1 connu dans le report canonique : 30 scanned, 1 skipped, 113 findings,
  exit 1 ;
- scan V1 connu dans le triage canonique : 31 scanned, 1 skipped, 114 findings,
  exit 1 ;
- scan relance dans ce GO apres PR #433 : 32 scanned, 1 skipped, 115 findings,
  exit 1 ;
- pytest OK : 20 passed ;
- worktree clean apres scan et avant creation de cette baseline ;
- 0 mutation par les validations ;
- PR #433 mergee ;
- triage V1 valide.

## 14_HYPOTHESIS

A valider :

- certains findings sont probablement des vrais gaps ;
- certains findings sont probablement du bruit structurel V1 ;
- certains findings devraient devenir exceptions documentees ;
- certains findings devraient guider l'ajustement futur du validateur ;
- le seuil de bruit V1 doit etre valide avant extension ;
- les rapports generes dans le dossier scanne devraient probablement etre
  exclus, classes en exception, ou pris en charge par une regle d'artifact.

## 15_REMAINING_GAP

- pas encore de corrections ;
- pas encore de baseline automatisee ;
- pas encore de seuils formels ;
- pas encore de regles d'exception codifiees ;
- pas encore de correction des vrais gaps ;
- pas encore d'ajustement du validateur ;
- pas encore de scan repo-wide ;
- pas encore de CI.

## 16_TODO

Suite recommandee :

1. merger cette baseline ;
2. ouvrir un GO de correction ciblee pour vrais gaps ;
3. ouvrir un GO separe pour ajustement regles V1 si bruit confirme ;
4. ouvrir un GO d'exceptions documentees si necessaire ;
5. ne pas etendre repo-wide avant stabilisation.

## 17_RESUME_POINT

Apres merge :

`GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REMEDIATION_PLAN_V1_01`

Objectif :

Creer un plan de remediation documentaire cible, base sur la baseline V1, sans
correction automatique.

## 18_TO_DOCUMENT

TAGS :

- WHY_LINT_BASELINE_V1
- WHY_LINT_FINDINGS_BASELINE
- WHY_LINT_REAL_DOCS_SCAN
- WHY_LINT_NO_AUTOFIX
- WHY_LINT_REMEDIATION_PLAN_NEXT

## 19_TO_REMEMBER

Memory Bricks candidats :

- Baseline initiale WHY lint V1 : 30 scanned / 1 skipped / 113 findings.
- Baseline courante acceptee apres ajout du rapport V1 : 31 scanned /
  1 skipped / 114 findings.
- L'ecart +1/+1 initial est auto-referentiel et classe bruit V1 attendu.
- La relance apres PR #433 observe 32 scanned / 1 skipped / 115 findings car le
  triage V1 est lui aussi scanne.
- La baseline precede toute correction documentaire.

## Baseline summary

| Metric | Initial V1 | Current V1 | Interpretation |
| --- | ---: | ---: | --- |
| scanned_files | 30 | 31 | Current V1 ajoute le rapport V1 au dossier scanne. |
| skipped_files | 1 | 1 | Le corpus de fixtures reste le seul fichier ignore. |
| findings | 113 | 114 | L'ecart +1 est le finding auto-referentiel du rapport V1. |
| exit_code | 1 | 1 | `FINDINGS_PRESENT`, comportement attendu. |
| status | FINDINGS_PRESENT | FINDINGS_PRESENT | Scan termine avec findings, sans crash. |

Observation de collecte post-PR #433 :

| Metric | Observed after PR #433 | Interpretation |
| --- | ---: | --- |
| scanned_files | 32 | Le triage V1 merge est maintenant scanne. |
| skipped_files | 1 | Le corpus de fixtures reste ignore. |
| findings | 115 | +1 `MISSING_WHY_SECTION` sur le triage V1. |
| exit_code | 1 | `FINDINGS_PRESENT`, attendu. |
| status | FINDINGS_PRESENT | Pas un crash, pas une permission de correction. |

## Baseline decision

- Baseline acceptee : `ACCEPTED_BASELINE_V1`.
- Baseline initiale : 30 scanned / 1 skipped / 113 findings.
- Baseline courante : 31 scanned / 1 skipped / 114 findings.
- Ecart auto-referentiel accepte : +1 scanned / +1 finding.
- Statut : `ACCEPTED_BASELINE_V1`.
- Corrections : interdites dans ce GO.

La relance post-PR #433 est conservee comme observation additionnelle :
32 scanned / 1 skipped / 115 findings. Elle ne remplace pas la baseline
acceptee ; elle prouve que chaque rapport documentaire ajoute au dossier parent
peut creer un nouveau bruit de scan jusqu'a decision d'exclusion ou de regle
d'artifact.

## Findings classification baseline

| classification | count | meaning | next_action |
| --- | --- | --- | --- |
| REAL_GAP | TBD_FROM_TRIAGE | Gap documentaire probablement reel, a confirmer par fichier. | Conserver dans baseline jusqu'au GO de remediation. |
| V1_NOISE | TBD_FROM_TRIAGE | Bruit produit par detection simple, exemples interdits ou auto-reference. | Conserver dans baseline ; ne pas assouplir les regles sans preuve. |
| DOCUMENTED_EXCEPTION | TBD_FROM_TRIAGE | Document legitime qui ne suit pas le squelette attendu. | Definir les exceptions dans un GO dedie avant tout codage. |
| RULE_REFINEMENT_NEEDED | TBD_FROM_TRIAGE | Regle V1 trop large ou trop stricte pour certains formats. | Ouvrir un GO d'ajustement seulement apres preuve de bruit. |
| NEED_MORE_EVIDENCE | TBD_FROM_TRIAGE | Finding insuffisamment qualifie pour correction immediate. | Maintenir dans la baseline jusqu'a classification fichier par fichier. |

Comptage technique de la relance post-PR #433 :

| finding_id | observed_count | baseline_note |
| --- | ---: | --- |
| APPLY_PATCH_ENABLED | 3 | Candidat V1_NOISE, exemples ou champs interdits documentes. |
| AUTOFIX_ENABLED | 3 | Candidat V1_NOISE, exemples ou contraintes documentees. |
| CI_BLOCKING_ENABLED | 3 | Candidat V1_NOISE, ne pas transformer en CI blocking. |
| EXECUTE_COMMAND_ENABLED | 3 | Candidat V1_NOISE, implication runtime documentee. |
| MISSING_FINAL_TARGET | 23 | NEED_MORE_EVIDENCE avant decision de remediation. |
| MISSING_INVARIANTS | 23 | NEED_MORE_EVIDENCE avant decision d'exception ou correction. |
| MISSING_RESUME_POINT | 23 | NEED_MORE_EVIDENCE avant decision par classe documentaire. |
| MISSING_WHY_SECTION | 31 | Melange probable de vrais gaps, bruit V1 et auto-reference. |
| RUNTIME_BINDING_ENABLED | 3 | Candidat V1_NOISE, garder invariant no-runtime. |

## Baseline policy

- Ne pas corriger automatiquement.
- Ne pas modifier les docs scannees.
- Ne pas reduire les regles sans preuve.
- Ne pas etendre repo-wide avant stabilisation.
- Ne pas rendre CI bloquante.
- Ne pas traiter un finding comme permission.
- Ne pas convertir une baseline en remediation implicite.
- Les rapports V1 dans le dossier scanne doivent etre geres explicitement avant
  toute comparaison automatique future.

## Accepted baseline

```text
ACCEPTED_BASELINE_V1_INITIAL = 30 scanned / 1 skipped / 113 findings
ACCEPTED_BASELINE_V1_CURRENT = 31 scanned / 1 skipped / 114 findings
AUTO_REFERENCE_DELTA = +1 scanned / +1 finding
OBSERVED_POST_PR433_COLLECTION = 32 scanned / 1 skipped / 115 findings
POST_PR433_COLLECTION_DELTA = +1 scanned / +1 finding versus accepted current
```

## Recommended next GO

`GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REMEDIATION_PLAN_V1_01`

Objectif :

Planifier les corrections documentaires ciblees et/ou ajustements de regles a
partir de la baseline, sans correction automatique.

## Verdict

`PASS_REAL_DOCS_SCAN_BASELINE_V1_DOC_ONLY`

## RISKS

- À qualifier.
