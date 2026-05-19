---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01
doc_type: chantier_child_implementation
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01
chantier_parent: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: child_implementation
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-14
topic_keys:
  - why_lint
  - static_validator
  - read_only
  - report_only
  - no_runtime
  - no_autofix
  - no_ci_blocking
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md
---

# GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01

## 1_MASTER_TARGET

Passer du cadrage documentation-only a une implementation controlee du premier
validateur statique local WHY lint.

Le validateur doit lire le corpus de fixtures Markdown existant, extraire les
blocs de regles, comparer les verdicts obtenus aux verdicts attendus et produire
un rapport deterministe.

## 2_INITIAL_PROJECT_DOC

Sources de depart :

- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_SPEC_REVIEW_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/05_WHY_LINT_WARNING_MODEL_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/06_CROSS_AXIS_GATE_BINDING_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/02_NO_DUPLICATION_BOUNDARY_MATRIX_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/04_DEPENDENCY_GRAPH_4_AXES_01.md`

## 3_INITIAL_NEED

Le corpus de fixtures est merge mais aucun outil local ne verifie encore que les
fixtures respectent leurs verdicts attendus.

Le besoin est de creer un validateur statique minimal qui prouve :

- l'extraction des fixtures ;
- la verification des champs requis ;
- la detection des familles, severites, axes et gates inconnus ;
- le respect no-runtime, no-autofix, no-CI-blocking ;
- la detection de placeholders secret-like factices ;
- la production d'un rapport deterministic read-only.

## 4_MASTER_PROJECT_PLAN

1. Creer le dossier `tools/why_lint_static_validator/`.
2. Ajouter le validateur Python standard-library.
3. Ajouter le README local de l'outil.
4. Ajouter les tests unitaires dedies.
5. Ajouter ce document chantier.
6. Executer les commandes de validation locales.
7. Verifier que seuls les fichiers de ce GO sont stagés et commites.

## 6_FINAL_TARGET

Implémenter un validateur statique local WHY lint read-only/report-only, capable
de vérifier le corpus de fixtures Markdown et de produire un rapport
déterministe, sans runtime, sans autofix, sans CI bloquante.

## 7_CANONICAL_STATE

Etat canonique vise par ce GO :

- branche dediee :
  `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01` ;
- base `sot/mainline` a jour apres merge du corpus ;
- outil cree sous `tools/why_lint_static_validator/` ;
- tests crees sous `tests/why_lint_static_validator/` ;
- aucun workflow CI cree ;
- aucun fichier YAML ou JSON actif cree ;
- aucun index global modifie.

## 8_VALIDATED_PLAN

Plan valide pour l'implementation :

1. Lire les specs parent, review, validator spec, corpus, warning model, gate
   binding, boundary matrix et dependency graph.
2. Coder un parseur Markdown limite aux fixtures.
3. Coder un parseur YAML-like limite aux fences du corpus.
4. Comparer verdict observe et verdict attendu.
5. Retourner des exit codes deterministes.
6. Couvrir les cas unitaires obligatoires.
7. Valider le corpus merge.

## 9_SELECTED_SOLUTION

Solution retenue :

- un fichier Python local executable directement ;
- aucune dependance externe nouvelle ;
- aucune config active ;
- un rapport texte par defaut ;
- un rapport JSON optionnel imprime sur stdout ;
- pas d'ecriture de rapport fichier.

## 10_SELECTED_SETUP

Fichiers crees :

```text
tools/why_lint_static_validator/README.md
tools/why_lint_static_validator/__init__.py
tools/why_lint_static_validator/why_lint_static_validator.py
tests/why_lint_static_validator/test_why_lint_static_validator.py
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01.md
```

Commande canonique :

```text
python tools/why_lint_static_validator/why_lint_static_validator.py --fixtures docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md
```

## 11_KEY_DECISIONS

- Le validateur ne lit que le fichier Markdown passe par `--fixtures`.
- Le parseur ne cree aucun fichier temporaire.
- Les valeurs `trace_required` et `eval_required` sont validees selon le modele
  de famille du corpus.
- Les placeholders secret-like factices sont detectes comme risques attendus
  dans les fixtures invalides.
- Les champs interdits `autofix_allowed: true`, `runtime_binding: true`,
  `can_fail_ci: true`, `execute_command: true` et `apply_patch: true` echouent.
- Les drifts d'autorite inter-axes echouent ou demandent plus de preuve selon la
  fixture.

## 12_INVARIANTS

- local only
- read-only
- report-only
- deterministic
- no runtime
- no MCP live
- no trade
- no secret
- no autofix
- no CI blocking
- no global index mutation
- no source mutation
- fail closed

## 13_ESTABLISHED

Le GO etablit :

- un outil local read-only/report-only ;
- un catalogue de verdicts supportes ;
- des exit codes deterministes ;
- une extraction de fixtures Markdown par `fixture_id` ;
- une verification du corpus de fixtures merge ;
- des tests unitaires locaux sans reseau.

## 14_HYPOTHESIS

Hypotheses retenues pour ce premier validateur :

- le corpus Markdown reste la source de test principale ;
- le sous-ensemble YAML-like des fences suffit pour ce GO ;
- les docs reelles hors fixtures seront traitees dans un GO ulterieur ;
- les faux placeholders secret-like restent explicitement factices.

## 15_REMAINING_GAP

- pas encore de CI future ;
- pas encore de rapport HTML ;
- pas encore d’intégration OpenClaw ;
- pas encore d’intégration MCP ;
- pas encore de validation cross-repo ;
- pas encore de lint sur docs réelles hors fixtures.

## 16_TODO

Avant merge :

1. Verifier `--help`.
2. Verifier le corpus complet.
3. Executer les tests unitaires.
4. Verifier le diff et l'absence de modification d'index global.
5. Stager uniquement les fichiers de ce GO.
6. Commit avec le message attendu.

## 17_RESUME_POINT

Après merge, prochain GO recommandé :

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01
```

Objectif futur :
spécifier le scan read-only de documents réels du repo, sans mutation, avant
toute intégration CI ou OpenClaw.

## 18_TO_DOCUMENT

TAGS :

- WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION
- WHY_LINT_READ_ONLY
- WHY_LINT_REPORT_ONLY
- WHY_LINT_NO_RUNTIME
- WHY_LINT_NO_AUTOFIX
- WHY_LINT_NO_CI_BLOCKING

Blocs a extraire :

- `6_FINAL_TARGET`
- `12_INVARIANTS`
- `15_REMAINING_GAP`
- `17_RESUME_POINT`

## 19_TO_REMEMBER

Memory Bricks candidats :

- `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01`
  cree le premier validateur statique local WHY lint.
- Le validateur reste read-only/report-only et ne scanne que les fixtures dans
  ce GO.
- Le prochain GO recommande specifie le scan read-only de documents reels avant
  toute integration CI, MCP ou OpenClaw.

## Verdict attendu

```text
PASS_READONLY_STATIC_VALIDATOR_IMPLEMENTATION
```
