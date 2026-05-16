# GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_V1_01

## Scope

- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_SPEC_REVIEW_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_TRIAGE_V1_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_BASELINE_V1_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REMEDIATION_PLAN_V1_01.md`

## Base canonique

- PR #437 mergee : remediation plan V1 canonique.
- PR #442 mergee : real gaps fix plan V1 canonique, merge commit `68cdbefb588577cfc16de617cfc1d49d244c4a91`.
- PR #452 mergee : first manual WHY lint gap fix batch, merge commit `43a5ae9b24077f3f9f5b7b7ff45ce9189fec8f99`.

## Decision

- Corriger uniquement des `MISSING_WHY_SECTION` isoles sur des docs actifs de la chaine WHY lint.
- Reporter tous les fichiers qui cumulent aussi `MISSING_FINAL_TARGET`, `MISSING_INVARIANTS` ou `MISSING_RESUME_POINT`.
- Reporter les fichiers dont le finding WHY reste mele a du bruit de type `AUTOFIX_ENABLED`, `APPLY_PATCH_ENABLED`, `EXECUTE_COMMAND_ENABLED` ou `RUNTIME_BINDING_ENABLED`.

## Objectif

- Appliquer une premiere passe V1 courte, manuelle et reviewable sur des gaps WHY etablis a haute confiance.
- Renforcer la continuite canonique `scan report -> triage -> baseline -> remediation -> correction` sans toucher au validateur.

## Gap initial

- Scan read-only courant execute sur `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01` : `34 scanned / 1 skipped / 116 findings / exit 1`.
- Les six fichiers du scope remontaient chacun un `MISSING_WHY_SECTION` isole.
- Le batch 01 avait deja valide qu'un ajout de `## WHY` manuel sur un doc actif etait une correction conforme et non destructive.

## Corrections appliquees

### GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_SPEC_REVIEW_01.md

- Gap initial : `MISSING_WHY_SECTION`.
- WHY ajoute : la review existe pour verifier que la SPEC parent mergee peut ancrer la suite des child GO avant tout code validateur ou travail runtime-adjacent.
- Decision reliee : garder la correction sur un doc actif a gap isole.
- Objectif relie : clarifier l'intention documentaire sans reclasser le document.

### GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md

- Gap initial : `MISSING_WHY_SECTION`.
- WHY ajoute : la spec existe pour encadrer le passage du corpus fixtures au scan de docs reels sans derive autofix, CI ou runtime.
- Decision reliee : renforcer la lecture explicite de la contrainte read-only/report-only deja canonique.
- Objectif relie : relier le scope technique au besoin documentaire etabli.

### GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01.md

- Gap initial : `MISSING_WHY_SECTION`.
- WHY ajoute : le rapport existe pour figer la premiere collecte V1 avant toute interpretation corrective.
- Decision reliee : corriger la causalite documentaire sans toucher au traitement de self-reference.
- Objectif relie : separer collecte, triage et remediation.

### GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_TRIAGE_V1_01.md

- Gap initial : `MISSING_WHY_SECTION`.
- WHY ajoute : le triage existe pour classer les findings avant mutation documentaire.
- Decision reliee : expliciter la frontiere entre triage, correction, exception et ajustement de regle.
- Objectif relie : rendre la decision de suite reviewable.

### GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_BASELINE_V1_01.md

- Gap initial : `MISSING_WHY_SECTION`.
- WHY ajoute : la baseline existe pour figer l'etat accepte avant correction et distinguer vrais gaps et bruit V1.
- Decision reliee : clarifier l'usage canonique de la baseline.
- Objectif relie : garder la remediation dans des GO separes.

### GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REMEDIATION_PLAN_V1_01.md

- Gap initial : `MISSING_WHY_SECTION`.
- WHY ajoute : le plan existe pour transformer la baseline en lots d'action sans corriger trop tot.
- Decision reliee : separer corrections documentaires, exceptions et ajustements de regles.
- Objectif relie : relier le plan V1 a son role de pivot avant correction.

## Validation

- `git diff --check` : OK.
- `git diff` : borne a des corrections documentaires plus cette trace chantier.
- Scan read-only WHY lint relance apres correction : `34 scanned / 1 skipped / 110 findings / exit 1`.
- Effet observe : `-6 findings`, correspondant aux six `MISSING_WHY_SECTION` corriges dans le scope.
- Validateur inchange ; aucune mutation source par le scan.

## Risques restants

- Les docs legacy a 4 gaps restent hors lot car leur classe documentaire reste ambigue.
- Les docs `..._SPEC_01.md` et `..._IMPLEMENTATION_...` qui cumulent bruit runtime/autofix restent a traiter separement.
- Les rapports scannes dans le dossier parent gardent un sujet de self-reference qui n'est pas resolu ici.

## Gaps reportes

- Tous les fichiers legacy remontant `MISSING_WHY_SECTION`, `MISSING_FINAL_TARGET`, `MISSING_INVARIANTS` et `MISSING_RESUME_POINT` ensemble.
- `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01.md`.
- `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01.md`.

## Reprise

- Si le diff passe en review : `V1_PR_01`.
- Si la passe doit rester fragmentee : `V1_BATCH_02` pour d'autres WHY isoles a haute confiance.
- Si un recontage canonique est prefere avant suite : `CONTROL_SCAN_01`.

## Statut

- PASS local: passe V1 courte, manuelle, sans auto-fix, sans changement validateur.
