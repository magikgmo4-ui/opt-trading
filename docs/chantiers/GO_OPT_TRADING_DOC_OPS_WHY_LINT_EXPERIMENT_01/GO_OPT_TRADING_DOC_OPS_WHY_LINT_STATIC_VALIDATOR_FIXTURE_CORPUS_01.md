---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01
doc_type: chantier_child_fixture_corpus
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01
chantier_parent: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: child_fixture
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-14
topic_keys:
  - why_lint
  - fixture_corpus
  - static_validator
  - warning_only
  - governance
  - runtime_security
  - why_runtime_graph
  - no_autofix
  - no_runtime
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_SPEC_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/05_WHY_LINT_WARNING_MODEL_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/06_CROSS_AXIS_GATE_BINDING_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/02_NO_DUPLICATION_BOUNDARY_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/04_DEPENDENCY_GRAPH_4_AXES_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md
---

# GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01

## 1_MASTER_TARGET

Creer un corpus documentaire de fixtures WHY lint pour preparer les futurs tests du validateur statique.

## 3_INITIAL_NEED

Le validateur statique est specifie, mais il manque un corpus de cas valides/invalides pour tester :
- rule schema ;
- warning families ;
- severity R0-R5 ;
- gate binding ;
- trace/eval binding ;
- no-runtime ;
- no-autofix ;
- no-CI-blocking ;
- no-secret ;
- no-duplication boundaries ;
- fail-closed behavior.

## 6_FINAL_TARGET

Produire un corpus Markdown-only de fixtures, avec verdicts attendus, error codes attendus, justification, regle validee, gate associee, trace/eval attendus, sans aucun fichier actif executable.

## 12_INVARIANTS

- Markdown-only.
- Fixtures non executables.
- YAML/JSON seulement dans des fences Markdown.
- Aucun secret reel.
- Aucun runtime.
- Aucun auto-fix.
- Aucun CI blocking.
- Aucun fichier actif YAML/JSON.
- Aucun script.
- Aucun index global.
- Toute fixture invalide doit avoir un expected_error_code.
- Toute fixture valide doit avoir un expected_verdict.
- Tout exemple secret-like doit etre factice et clairement bloque.

---

## Index des fixtures

| fixture_id | category | expected_verdict | expected_error_code | related_rule | related_gate | related_trace | related_eval |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VALID_MINIMAL_RULE_01 | A | PASS_RULE_STATIC_VALIDATION | - | rule_schema_001 | REVIEW_REQUIRED | true | false |
| VALID_WHY_GAP_RULE_01 | A | PASS_RULE_STATIC_VALIDATION | - | rule_schema_001 | REVIEW_REQUIRED | true | false |
| VALID_GOVERNANCE_DRIFT_RULE_01 | A | PASS_RULE_STATIC_VALIDATION | - | rule_schema_001 | GOVERNANCE_ALIGNMENT_REQUIRED | true | false |
| VALID_RUNTIME_SECURITY_GAP_RULE_01 | A | PASS_RULE_STATIC_VALIDATION | - | rule_schema_001 | RUNTIME_PROOF_REQUIRED | true | true |
| VALID_MACHINE_SCOPE_GAP_RULE_01 | A | PASS_RULE_STATIC_VALIDATION | - | rule_schema_001 | REVIEW_REQUIRED | true | false |
| VALID_WORKER_OWNER_GAP_RULE_01 | A | PASS_RULE_STATIC_VALIDATION | - | rule_schema_001 | REVIEW_REQUIRED | true | false |
| VALID_TRACE_EVAL_GAP_RULE_01 | A | PASS_RULE_STATIC_VALIDATION | - | rule_schema_001 | RUNTIME_PROOF_REQUIRED | true | true |
| FAIL_MISSING_RULE_ID_01 | B | FAIL_SCHEMA_MISSING_FIELD | ERR_SCHEMA_MISSING_RULE_ID | rule_schema_002 | - | - | - |
| FAIL_MISSING_FAMILY_01 | B | FAIL_SCHEMA_MISSING_FIELD | ERR_SCHEMA_MISSING_FAMILY | rule_schema_003 | - | - | - |
| FAIL_MISSING_SEVERITY_01 | B | FAIL_SCHEMA_MISSING_FIELD | ERR_SCHEMA_MISSING_SEVERITY | rule_schema_004 | - | - | - |
| FAIL_MISSING_SOURCE_AXIS_01 | B | FAIL_SCHEMA_MISSING_FIELD | ERR_SCHEMA_MISSING_SOURCE_AXIS | rule_schema_005 | - | - | - |
| FAIL_MISSING_AFFECTED_AXIS_01 | B | FAIL_SCHEMA_MISSING_FIELD | ERR_SCHEMA_MISSING_AFFECTED_AXIS | rule_schema_006 | - | - | - |
| FAIL_MISSING_EVIDENCE_REQUIRED_01 | B | FAIL_SCHEMA_MISSING_FIELD | ERR_SCHEMA_MISSING_EVIDENCE | rule_schema_007 | - | - | - |
| FAIL_UNKNOWN_WARNING_FAMILY_01 | C | FAIL_UNKNOWN_WARNING_FAMILY | ERR_UNKNOWN_FAMILY_EXECUTE_SHELL | rule_schema_008 | - | - | - |
| FAIL_UNKNOWN_SEVERITY_01 | C | FAIL_UNKNOWN_WARNING_FAMILY | ERR_UNKNOWN_SEVERITY_R9 | rule_schema_009 | - | - | - |
| FAIL_UNKNOWN_SOURCE_AXIS_01 | C | FAIL_UNKNOWN_WARNING_FAMILY | ERR_UNKNOWN_AXIS_ML_LAYER | rule_schema_010 | - | - | - |
| FAIL_EMPTY_AFFECTED_AXIS_01 | C | FAIL_SCHEMA_MISSING_FIELD | ERR_SCHEMA_EMPTY_AFFECTED_AXIS | rule_schema_011 | - | - | - |
| FAIL_MISSING_GATE_BINDING_01 | D | FAIL_GATE_BINDING | ERR_GATE_MISSING_BINDING | rule_schema_012 | - | - | - |
| FAIL_UNKNOWN_GATE_01 | D | FAIL_GATE_BINDING | ERR_GATE_UNKNOWN_START_WORKER | rule_schema_013 | - | - | - |
| FAIL_TRACE_REQUIRED_FALSE_01 | D | FAIL_TRACE_BINDING | ERR_TRACE_REQUIRED_FALSE | rule_schema_014 | - | - | - |
| FAIL_EVAL_REQUIRED_FALSE_01 | D | FAIL_EVAL_BINDING | ERR_EVAL_REQUIRED_FALSE | rule_schema_015 | - | - | - |
| FAIL_MISSING_TRACE_EVAL_METADATA_01 | D | FAIL_TRACE_BINDING | ERR_TRACE_EVAL_METADATA_MISSING | rule_schema_016 | - | - | - |
| FAIL_AUTOFIX_ENABLED_01 | E | FAIL_AUTOFIX_ENABLED | ERR_AUTOFIX_ENABLED | rule_schema_017 | - | - | - |
| FAIL_RUNTIME_BINDING_ENABLED_01 | E | FAIL_RUNTIME_BINDING_ENABLED | ERR_RUNTIME_BINDING_ENABLED | rule_schema_018 | - | - | - |
| FAIL_CI_BLOCKING_ENABLED_01 | E | FAIL_CI_BLOCKING_ENABLED | ERR_CI_BLOCKING_ENABLED | rule_schema_019 | - | - | - |
| FAIL_EXECUTE_COMMAND_ENABLED_01 | E | FAIL_RUNTIME_BINDING_ENABLED | ERR_EXECUTE_COMMAND_ENABLED | rule_schema_020 | - | - | - |
| FAIL_APPLY_PATCH_ENABLED_01 | E | FAIL_AUTOFIX_ENABLED | ERR_APPLY_PATCH_ENABLED | rule_schema_021 | - | - | - |
| FAIL_SECRET_LIKE_FIELD_01 | F | FAIL_SECRET_RISK | ERR_SECRET_LIKE_FIELD | rule_schema_022 | - | - | - |
| FAIL_TOKEN_LIKE_VALUE_01 | F | FAIL_SECRET_RISK | ERR_TOKEN_LIKE_VALUE | rule_schema_023 | - | - | - |
| FAIL_ENV_DUMP_EXAMPLE_01 | F | FAIL_SECRET_RISK | ERR_ENV_DUMP_EXAMPLE | rule_schema_024 | - | - | - |
| FAIL_PRIVATE_KEY_BLOCK_EXAMPLE_01 | F | FAIL_SECRET_RISK | ERR_PRIVATE_KEY_BLOCK | rule_schema_025 | - | - | - |
| FAIL_WHY_LINT_AUTHORIZES_RUNTIME_01 | G | FAIL_AXIS_AUTHORITY_DRIFT | ERR_AUTHORITY_DRIFT_LINT_RUNTIME | rule_schema_026 | - | - | - |
| FAIL_WHY_GRAPH_DEFINES_PERMISSION_01 | G | FAIL_AXIS_AUTHORITY_DRIFT | ERR_AUTHORITY_DRIFT_GRAPH_PERM | rule_schema_027 | - | - | - |
| FAIL_OPENCLAW_TARGET_GRANTS_EXECUTION_01 | G | FAIL_AXIS_AUTHORITY_DRIFT | ERR_AUTHORITY_DRIFT_TARGET_EXEC | rule_schema_028 | - | - | - |
| FAIL_RUNTIME_SECURITY_REPLACES_GOVERNANCE_01 | G | FAIL_AXIS_AUTHORITY_DRIFT | ERR_AUTHORITY_DRIFT_SECURITY_GOV | rule_schema_029 | - | - | - |
| FAIL_GOVERNANCE_REWRITES_PRODUCT_TARGET_01 | G | NEED_MORE_EVIDENCE | ERR_AUTHORITY_DRIFT_GOV_TARGET | rule_schema_030 | - | - | - |
| BLOCKED_UNKNOWN_RULE_01 | H | FAIL_UNKNOWN_RULE | ERR_UNKNOWN_RULE_ID_ZZ_999 | rule_schema_031 | - | - | - |
| NEED_MORE_EVIDENCE_MISSING_SOURCE_01 | H | NEED_MORE_EVIDENCE | ERR_EVIDENCE_MISSING_SOURCE_FILE | rule_schema_032 | - | - | - |
| BLOCKED_BY_POLICY_UNKNOWN_AXIS_01 | H | BLOCKED_BY_POLICY | ERR_POLICY_UNKNOWN_AXIS | rule_schema_033 | - | - | - |
| NEED_MORE_EVIDENCE_MISSING_PROOF_01 | H | NEED_MORE_EVIDENCE | ERR_EVIDENCE_MISSING_PROOF | rule_schema_034 | - | - | - |

---

## A. Valid fixtures

### VALID_MINIMAL_RULE_01

- **fixture_id**: VALID_MINIMAL_RULE_01
- **category**: A — Valid fixture
- **purpose**: Tester qu'une regle minimale valide avec tous les champs requis passe la validation statique.
- **expected_verdict**: PASS_RULE_STATIC_VALIDATION
- **expected_error_code**: (none)
- **related_validator_rule**: rule_schema_001
- **related_warning_family**: WHY_GAP
- **related_gate**: REVIEW_REQUIRED
- **related_trace**: true
- **related_eval**: false
- **why_it_should_pass_or_fail**: Tous les champs du schema sont presents et valides. rule_id, family, severity, source_axis, affected_axis, gate_required, trace_required, eval_required, autofix_allowed, runtime_binding, can_fail_ci, evidence_required sont conformes.

```yaml
rule_id: "MINIMAL_RULE_001"
family: "WHY_GAP"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L42"
  - "Missing WHY section"
```

### VALID_WHY_GAP_RULE_01

- **fixture_id**: VALID_WHY_GAP_RULE_01
- **category**: A — Valid fixture
- **purpose**: Tester une regle de detection de WHY manquant dans un document canonique.
- **expected_verdict**: PASS_RULE_STATIC_VALIDATION
- **expected_error_code**: (none)
- **related_validator_rule**: rule_schema_001
- **related_warning_family**: WHY_GAP
- **related_gate**: REVIEW_REQUIRED
- **related_trace**: true
- **related_eval**: false
- **why_it_should_pass_or_fail**: La regle cible WHY_GAP, avec une severite R2 appropriee, un gate REVIEW_REQUIRED, trace active, eval desactive. autofix, runtime, CI sont tous a false.

```yaml
rule_id: "WHY_GAP_DOC_MISSING_001"
family: "WHY_GAP"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/chantiers/EXAMPLE_GO/SPEC.md"
  - "Section 4"
  - "No WHY section found"
```

### VALID_GOVERNANCE_DRIFT_RULE_01

- **fixture_id**: VALID_GOVERNANCE_DRIFT_RULE_01
- **category**: A — Valid fixture
- **purpose**: Tester une regle de detection d'ecart entre un document et la matrice maitre.
- **expected_verdict**: PASS_RULE_STATIC_VALIDATION
- **expected_error_code**: (none)
- **related_validator_rule**: rule_schema_001
- **related_warning_family**: GOVERNANCE_DRIFT
- **related_gate**: GOVERNANCE_ALIGNMENT_REQUIRED + REVIEW_REQUIRED
- **related_trace**: true
- **related_eval**: false
- **why_it_should_pass_or_fail**: La regle utilise GOVERNANCE_DRIFT avec le gate GOVERNANCE_ALIGNMENT_REQUIRED. Tous les champs invariants sont corrects.

```yaml
rule_id: "GOV_DRIFT_MATRIX_ALIGN_001"
family: "GOVERNANCE_DRIFT"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "Document affecte"
gate_required: "GOVERNANCE_ALIGNMENT_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/example/document.md"
  - "Section 1.3"
  - "Frontmatter missing doc_id"
```

### VALID_RUNTIME_SECURITY_GAP_RULE_01

- **fixture_id**: VALID_RUNTIME_SECURITY_GAP_RULE_01
- **category**: A — Valid fixture
- **purpose**: Tester une regle de detection d'absence de garde-fou pour une action runtime.
- **expected_verdict**: PASS_RULE_STATIC_VALIDATION
- **expected_error_code**: (none)
- **related_validator_rule**: rule_schema_001
- **related_warning_family**: RUNTIME_SECURITY_GAP
- **related_gate**: RUNTIME_PROOF_REQUIRED + GATE_RUNTIME
- **related_trace**: true
- **related_eval**: true
- **why_it_should_pass_or_fail**: La regle cible RUNTIME_SECURITY_GAP avec severite R1, gate RUNTIME_PROOF_REQUIRED, trace ET eval a true. Les invariants sont respectes.

```yaml
rule_id: "RT_SEC_GAP_PERM_MISSING_001"
family: "RUNTIME_SECURITY_GAP"
severity: "R1"
source_axis: "Runtime Security"
affected_axis:
  - "OpenClaw Central"
gate_required: "RUNTIME_PROOF_REQUIRED"
trace_required: true
eval_required: true
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "configs/openclaw/security/skill_policy.yaml"
  - "worker_exec section"
  - "No permission entry for worker type"
```

### VALID_MACHINE_SCOPE_GAP_RULE_01

- **fixture_id**: VALID_MACHINE_SCOPE_GAP_RULE_01
- **category**: A — Valid fixture
- **purpose**: Tester une regle de detection de contradiction de routage machine.
- **expected_verdict**: PASS_RULE_STATIC_VALIDATION
- **expected_error_code**: (none)
- **related_validator_rule**: rule_schema_001
- **related_warning_family**: MACHINE_SCOPE_GAP
- **related_gate**: REVIEW_REQUIRED
- **related_trace**: true
- **related_eval**: false
- **why_it_should_pass_or_fail**: La regle utilise MACHINE_SCOPE_GAP, severite R3, gate REVIEW_REQUIRED. Schema valide.

```yaml
rule_id: "MACH_SCOPE_BRANCH_MISMATCH_001"
family: "MACHINE_SCOPE_GAP"
severity: "R3"
source_axis: "Governance"
affected_axis:
  - "MACHINE_WORK_SPLIT"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md"
  - "Bloc CURSOR_AI"
  - "Branch listed under wrong machine block"
```

### VALID_WORKER_OWNER_GAP_RULE_01

- **fixture_id**: VALID_WORKER_OWNER_GAP_RULE_01
- **category**: A — Valid fixture
- **purpose**: Tester une regle de detection de worker sans proprietaire documente.
- **expected_verdict**: PASS_RULE_STATIC_VALIDATION
- **expected_error_code**: (none)
- **related_validator_rule**: rule_schema_001
- **related_warning_family**: WORKER_OWNER_GAP
- **related_gate**: REVIEW_REQUIRED + RUNTIME_PROOF_REQUIRED
- **related_trace**: true
- **related_eval**: false
- **why_it_should_pass_or_fail**: La regle utilise WORKER_OWNER_GAP avec les gates appropriees. Tous les invariants sont respectes.

```yaml
rule_id: "WORKER_OWNER_UNDOCUMENTED_001"
family: "WORKER_OWNER_GAP"
severity: "R3"
source_axis: "Runtime Security"
affected_axis:
  - "OpenClaw Central"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/chantiers/EXAMPLE_WORKER/SPEC.md"
  - "Section OWNER"
  - "No owner declared for worker process"
```

### VALID_TRACE_EVAL_GAP_RULE_01

- **fixture_id**: VALID_TRACE_EVAL_GAP_RULE_01
- **category**: A — Valid fixture
- **purpose**: Tester une regle de detection d'action sans trace ni eval.
- **expected_verdict**: PASS_RULE_STATIC_VALIDATION
- **expected_error_code**: (none)
- **related_validator_rule**: rule_schema_001
- **related_warning_family**: TRACE_EVAL_GAP
- **related_gate**: RUNTIME_PROOF_REQUIRED
- **related_trace**: true
- **related_eval**: true
- **why_it_should_pass_or_fail**: La regle cible TRACE_EVAL_GAP avec trace ET eval a true, ce qui est coherent avec la famille.

```yaml
rule_id: "TRACE_EVAL_MISSING_AUDIT_001"
family: "TRACE_EVAL_GAP"
severity: "R2"
source_axis: "Runtime Security"
affected_axis:
  - "OpenClaw Central"
gate_required: "RUNTIME_PROOF_REQUIRED"
trace_required: true
eval_required: true
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "configs/openclaw/security/skill_policy.yaml"
  - "actions.worker_exec"
  - "No audit log or eval requirement declared"
```

---

## B. Schema failure fixtures

### FAIL_MISSING_RULE_ID_01

- **fixture_id**: FAIL_MISSING_RULE_ID_01
- **category**: B — Schema failure
- **purpose**: Tester que le validateur rejette une regle sans rule_id.
- **expected_verdict**: FAIL_SCHEMA_MISSING_FIELD
- **expected_error_code**: ERR_SCHEMA_MISSING_RULE_ID
- **related_validator_rule**: rule_schema_002
- **related_warning_family**: (not applicable - rule_id is absent)
- **related_gate**: (none)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: rule_id est requis par la spec. Son absence doit declencher FAIL_SCHEMA_MISSING_FIELD.

```yaml
# rule_id is MISSING — should fail
family: "WHY_GAP"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L42"
  - "Missing WHY section"
```

### FAIL_MISSING_FAMILY_01

- **fixture_id**: FAIL_MISSING_FAMILY_01
- **category**: B — Schema failure
- **purpose**: Tester que le validateur rejette une regle sans family.
- **expected_verdict**: FAIL_SCHEMA_MISSING_FIELD
- **expected_error_code**: ERR_SCHEMA_MISSING_FAMILY
- **related_validator_rule**: rule_schema_003
- **related_warning_family**: (not applicable - family is absent)
- **related_gate**: (none)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: family est un champ obligatoire du schema. Son absence doit echouer.

```yaml
rule_id: "MISSING_FAMILY_RULE_001"
# family is MISSING — should fail
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L42"
  - "Missing WHY section"
```

### FAIL_MISSING_SEVERITY_01

- **fixture_id**: FAIL_MISSING_SEVERITY_01
- **category**: B — Schema failure
- **purpose**: Tester que le validateur rejette une regle sans severity.
- **expected_verdict**: FAIL_SCHEMA_MISSING_FIELD
- **expected_error_code**: ERR_SCHEMA_MISSING_SEVERITY
- **related_validator_rule**: rule_schema_004
- **related_warning_family**: (not applicable - severity is absent)
- **related_gate**: (none)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: severity est obligatoire. Son absence doit echouer.

```yaml
rule_id: "MISSING_SEVERITY_RULE_001"
family: "WHY_GAP"
# severity is MISSING — should fail
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L42"
  - "Missing WHY section"
```

### FAIL_MISSING_SOURCE_AXIS_01

- **fixture_id**: FAIL_MISSING_SOURCE_AXIS_01
- **category**: B — Schema failure
- **purpose**: Tester que le validateur rejette une regle sans source_axis.
- **expected_verdict**: FAIL_SCHEMA_MISSING_FIELD
- **expected_error_code**: ERR_SCHEMA_MISSING_SOURCE_AXIS
- **related_validator_rule**: rule_schema_005
- **related_warning_family**: (not applicable - source_axis is absent)
- **related_gate**: (none)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: source_axis est requis. Son absence doit echouer.

```yaml
rule_id: "MISSING_SOURCE_AXIS_001"
family: "WHY_GAP"
severity: "R2"
# source_axis is MISSING — should fail
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L42"
  - "Missing WHY section"
```

### FAIL_MISSING_AFFECTED_AXIS_01

- **fixture_id**: FAIL_MISSING_AFFECTED_AXIS_01
- **category**: B — Schema failure
- **purpose**: Tester que le validateur rejette une regle sans affected_axis.
- **expected_verdict**: FAIL_SCHEMA_MISSING_FIELD
- **expected_error_code**: ERR_SCHEMA_MISSING_AFFECTED_AXIS
- **related_validator_rule**: rule_schema_006
- **related_warning_family**: (not applicable - affected_axis is absent)
- **related_gate**: (none)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: affected_axis est requis et doit etre non-vide. Son absence doit echouer.

```yaml
rule_id: "MISSING_AFFECTED_AXIS_001"
family: "WHY_GAP"
severity: "R2"
source_axis: "Governance"
# affected_axis is MISSING — should fail
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L42"
  - "Missing WHY section"
```

### FAIL_MISSING_EVIDENCE_REQUIRED_01

- **fixture_id**: FAIL_MISSING_EVIDENCE_REQUIRED_01
- **category**: B — Schema failure
- **purpose**: Tester que le validateur rejette une regle sans evidence_required.
- **expected_verdict**: FAIL_SCHEMA_MISSING_FIELD
- **expected_error_code**: ERR_SCHEMA_MISSING_EVIDENCE
- **related_validator_rule**: rule_schema_007
- **related_warning_family**: (not applicable - evidence_required is absent)
- **related_gate**: (none)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: evidence_required est requis par la spec. Son absence doit echouer.

```yaml
rule_id: "MISSING_EVIDENCE_001"
family: "WHY_GAP"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
# evidence_required is MISSING — should fail
```

---

## C. Warning family failure fixtures

### FAIL_UNKNOWN_WARNING_FAMILY_01

- **fixture_id**: FAIL_UNKNOWN_WARNING_FAMILY_01
- **category**: C — Warning family failure
- **purpose**: Tester que le validateur rejette une regle avec une famille de warning inconnue.
- **expected_verdict**: FAIL_UNKNOWN_WARNING_FAMILY
- **expected_error_code**: ERR_UNKNOWN_FAMILY_EXECUTE_SHELL
- **related_validator_rule**: rule_schema_008
- **related_warning_family**: EXECUTE_SHELL (non approuvee)
- **related_gate**: (none - rejetee avant binding)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: EXECUTE_SHELL n'est pas dans la liste des 11 familles approuvees. Le validateur doit emettre FAIL_UNKNOWN_WARNING_FAMILY.

```yaml
rule_id: "UNKNOWN_FAMILY_SHELL_001"
family: "EXECUTE_SHELL"
severity: "R2"
source_axis: "Runtime Security"
affected_axis:
  - "OpenClaw Central"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L10"
  - "Shell execution required"
```

### FAIL_UNKNOWN_SEVERITY_01

- **fixture_id**: FAIL_UNKNOWN_SEVERITY_01
- **category**: C — Warning family failure
- **purpose**: Tester que le validateur rejette une severite hors de la plage R0-R5.
- **expected_verdict**: FAIL_UNKNOWN_WARNING_FAMILY
- **expected_error_code**: ERR_UNKNOWN_SEVERITY_R9
- **related_validator_rule**: rule_schema_009
- **related_warning_family**: WHY_GAP (valide, mais severite invalide)
- **related_gate**: (none - rejetee avant binding)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: R9 n'est pas une severite valide (R0-R5 seulement). Le validateur doit rejeter.

```yaml
rule_id: "UNKNOWN_SEVERITY_R9_001"
family: "WHY_GAP"
severity: "R9"
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L42"
  - "Missing WHY section"
```

### FAIL_UNKNOWN_SOURCE_AXIS_01

- **fixture_id**: FAIL_UNKNOWN_SOURCE_AXIS_01
- **category**: C — Warning family failure
- **purpose**: Tester que le validateur rejette un axe source inconnu.
- **expected_verdict**: FAIL_UNKNOWN_WARNING_FAMILY
- **expected_error_code**: ERR_UNKNOWN_AXIS_ML_LAYER
- **related_validator_rule**: rule_schema_010
- **related_warning_family**: WHY_GAP (mais source_axis invalide)
- **related_gate**: (none - rejetee avant binding)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: ML_LAYER n'est pas un axe source reconnu. Le validateur doit rejeter.

```yaml
rule_id: "UNKNOWN_AXIS_ML_001"
family: "WHY_GAP"
severity: "R2"
source_axis: "ML_LAYER"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L42"
  - "Missing WHY section"
```

### FAIL_EMPTY_AFFECTED_AXIS_01

- **fixture_id**: FAIL_EMPTY_AFFECTED_AXIS_01
- **category**: C — Warning family failure
- **purpose**: Tester que le validateur rejette un affected_axis vide.
- **expected_verdict**: FAIL_SCHEMA_MISSING_FIELD
- **expected_error_code**: ERR_SCHEMA_EMPTY_AFFECTED_AXIS
- **related_validator_rule**: rule_schema_011
- **related_warning_family**: WHY_GAP (mais affected_axis vide)
- **related_gate**: (none - rejetee avant binding)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: affected_axis doit etre non-vide. Une liste vide doit echouer.

```yaml
rule_id: "EMPTY_AFFECTED_AXIS_001"
family: "WHY_GAP"
severity: "R2"
source_axis: "Governance"
affected_axis: []
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L42"
  - "Missing WHY section"
```

---

## D. Gate / trace / eval failure fixtures

### FAIL_MISSING_GATE_BINDING_01

- **fixture_id**: FAIL_MISSING_GATE_BINDING_01
- **category**: D — Gate / trace / eval failure
- **purpose**: Tester que le validateur rejette une regle sans gate_required.
- **expected_verdict**: FAIL_GATE_BINDING
- **expected_error_code**: ERR_GATE_MISSING_BINDING
- **related_validator_rule**: rule_schema_012
- **related_warning_family**: WHY_GAP
- **related_gate**: (none - absent)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: gate_required est obligatoire. Son absence doit declencher FAIL_GATE_BINDING.

```yaml
rule_id: "MISSING_GATE_BINDING_001"
family: "WHY_GAP"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
# gate_required is MISSING — should fail
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L42"
  - "Missing WHY section"
```

### FAIL_UNKNOWN_GATE_01

- **fixture_id**: FAIL_UNKNOWN_GATE_01
- **category**: D — Gate / trace / eval failure
- **purpose**: Tester que le validateur rejette un nom de gate inconnu.
- **expected_verdict**: FAIL_GATE_BINDING
- **expected_error_code**: ERR_GATE_UNKNOWN_START_WORKER
- **related_validator_rule**: rule_schema_013
- **related_warning_family**: WHY_GAP
- **related_gate**: START_WORKER (inconnu)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: START_WORKER n'est pas dans la liste des gates approuvees. Le validateur doit emettre FAIL_GATE_BINDING.

```yaml
rule_id: "UNKNOWN_GATE_WORKER_START_001"
family: "WHY_GAP"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "START_WORKER"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L42"
  - "Missing WHY section"
```

### FAIL_TRACE_REQUIRED_FALSE_01

- **fixture_id**: FAIL_TRACE_REQUIRED_FALSE_01
- **category**: D — Gate / trace / eval failure
- **purpose**: Tester que le validateur rejette une regle avec trace_required a false alors que la famille exige true.
- **expected_verdict**: FAIL_TRACE_BINDING
- **expected_error_code**: ERR_TRACE_REQUIRED_FALSE
- **related_validator_rule**: rule_schema_014
- **related_warning_family**: RUNTIME_SECURITY_GAP (exige trace=true)
- **related_gate**: RUNTIME_PROOF_REQUIRED
- **related_trace**: false (invalide)
- **related_eval**: true
- **why_it_should_pass_or_fail**: RUNTIME_SECURITY_GAP exige trace_required=true dans la spec. Un false doit echouer.

```yaml
rule_id: "TRACE_FALSE_RT_GAP_001"
family: "RUNTIME_SECURITY_GAP"
severity: "R1"
source_axis: "Runtime Security"
affected_axis:
  - "OpenClaw Central"
gate_required: "RUNTIME_PROOF_REQUIRED"
trace_required: false
eval_required: true
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "configs/openclaw/security/skill_policy.yaml"
  - "actions.worker_exec"
  - "No permission entry"
```

### FAIL_EVAL_REQUIRED_FALSE_01

- **fixture_id**: FAIL_EVAL_REQUIRED_FALSE_01
- **category**: D — Gate / trace / eval failure
- **purpose**: Tester que le validateur rejette une regle avec eval_required a false alors que la famille exige true.
- **expected_verdict**: FAIL_EVAL_BINDING
- **expected_error_code**: ERR_EVAL_REQUIRED_FALSE
- **related_validator_rule**: rule_schema_015
- **related_warning_family**: RUNTIME_SECURITY_GAP (exige eval=true)
- **related_gate**: RUNTIME_PROOF_REQUIRED
- **related_trace**: true
- **related_eval**: false (invalide)
- **why_it_should_pass_or_fail**: RUNTIME_SECURITY_GAP exige eval_required=true. Un false doit echouer.

```yaml
rule_id: "EVAL_FALSE_RT_GAP_001"
family: "RUNTIME_SECURITY_GAP"
severity: "R1"
source_axis: "Runtime Security"
affected_axis:
  - "OpenClaw Central"
gate_required: "RUNTIME_PROOF_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "configs/openclaw/security/skill_policy.yaml"
  - "actions.worker_exec"
  - "No permission entry"
```

### FAIL_MISSING_TRACE_EVAL_METADATA_01

- **fixture_id**: FAIL_MISSING_TRACE_EVAL_METADATA_01
- **category**: D — Gate / trace / eval failure
- **purpose**: Tester que le validateur rejette une regle ou trace_required et eval_required sont absents.
- **expected_verdict**: FAIL_TRACE_BINDING
- **expected_error_code**: ERR_TRACE_EVAL_METADATA_MISSING
- **related_validator_rule**: rule_schema_016
- **related_warning_family**: GOVERNANCE_DRIFT
- **related_gate**: GOVERNANCE_ALIGNMENT_REQUIRED
- **related_trace**: (none - absent)
- **related_eval**: (none - absent)
- **why_it_should_pass_or_fail**: trace_required et eval_required doivent etre explicitement declares. Leur absence doit echouer.

```yaml
rule_id: "MISSING_TRACE_EVAL_META_001"
family: "GOVERNANCE_DRIFT"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "Document affecte"
gate_required: "GOVERNANCE_ALIGNMENT_REQUIRED"
# trace_required and eval_required are MISSING — should fail
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L15"
  - "Frontmatter mismatch"
```

---

## E. Runtime / autofix / CI failure fixtures

### FAIL_AUTOFIX_ENABLED_01

- **fixture_id**: FAIL_AUTOFIX_ENABLED_01
- **category**: E — Runtime / autofix / CI failure
- **purpose**: Tester que le validateur rejette une regle avec autofix_allowed a true.
- **expected_verdict**: FAIL_AUTOFIX_ENABLED
- **expected_error_code**: ERR_AUTOFIX_ENABLED
- **related_validator_rule**: rule_schema_017
- **related_warning_family**: WHY_GAP
- **related_gate**: REVIEW_REQUIRED
- **related_trace**: true
- **related_eval**: false
- **why_it_should_pass_or_fail**: autofix_allowed doit toujours etre false pour WHY lint. Un true doit echouer.

```yaml
rule_id: "AUTOFIX_ENABLED_RULE_001"
family: "WHY_GAP"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: true
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L42"
  - "Missing WHY section"
```

### FAIL_RUNTIME_BINDING_ENABLED_01

- **fixture_id**: FAIL_RUNTIME_BINDING_ENABLED_01
- **category**: E — Runtime / autofix / CI failure
- **purpose**: Tester que le validateur rejette une regle avec runtime_binding a true.
- **expected_verdict**: FAIL_RUNTIME_BINDING_ENABLED
- **expected_error_code**: ERR_RUNTIME_BINDING_ENABLED
- **related_validator_rule**: rule_schema_018
- **related_warning_family**: RUNTIME_SECURITY_GAP
- **related_gate**: RUNTIME_PROOF_REQUIRED
- **related_trace**: true
- **related_eval**: true
- **why_it_should_pass_or_fail**: runtime_binding doit toujours etre false pour WHY lint. Un true doit echouer.

```yaml
rule_id: "RUNTIME_BINDING_TRUE_001"
family: "RUNTIME_SECURITY_GAP"
severity: "R1"
source_axis: "Runtime Security"
affected_axis:
  - "OpenClaw Central"
gate_required: "RUNTIME_PROOF_REQUIRED"
trace_required: true
eval_required: true
autofix_allowed: false
runtime_binding: true
can_fail_ci: false
evidence_required:
  - "configs/openclaw/security/skill_policy.yaml"
  - "actions.worker_exec"
  - "No permission entry"
```

### FAIL_CI_BLOCKING_ENABLED_01

- **fixture_id**: FAIL_CI_BLOCKING_ENABLED_01
- **category**: E — Runtime / autofix / CI failure
- **purpose**: Tester que le validateur rejette une regle avec can_fail_ci a true.
- **expected_verdict**: FAIL_CI_BLOCKING_ENABLED
- **expected_error_code**: ERR_CI_BLOCKING_ENABLED
- **related_validator_rule**: rule_schema_019
- **related_warning_family**: WHY_GAP
- **related_gate**: REVIEW_REQUIRED
- **related_trace**: true
- **related_eval**: false
- **why_it_should_pass_or_fail**: can_fail_ci doit etre false pour WHY lint. Un true doit echouer.

```yaml
rule_id: "CI_BLOCKING_ENABLED_001"
family: "WHY_GAP"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: true
evidence_required:
  - "docs/source/example.md"
  - "L42"
  - "Missing WHY section"
```

### FAIL_EXECUTE_COMMAND_ENABLED_01

- **fixture_id**: FAIL_EXECUTE_COMMAND_ENABLED_01
- **category**: E — Runtime / autofix / CI failure
- **purpose**: Tester que le validateur rejette une regle avec execute_command a true.
- **expected_verdict**: FAIL_RUNTIME_BINDING_ENABLED
- **expected_error_code**: ERR_EXECUTE_COMMAND_ENABLED
- **related_validator_rule**: rule_schema_020
- **related_warning_family**: CONTROL_PLANE_GAP
- **related_gate**: MULTI_MACHINE_REVIEW_REQUIRED
- **related_trace**: true
- **related_eval**: true
- **why_it_should_pass_or_fail**: execute_command est un champ interdit pour WHY lint. Sa presence a true doit echouer comme runtime binding.

```yaml
rule_id: "EXECUTE_CMD_ENABLED_001"
family: "CONTROL_PLANE_GAP"
severity: "R1"
source_axis: "Governance"
affected_axis:
  - "OpenClaw Central"
gate_required: "MULTI_MACHINE_REVIEW_REQUIRED"
trace_required: true
eval_required: true
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
execute_command: true
evidence_required:
  - "docs/source/example.md"
  - "L30"
  - "Control plane not documented"
```

### FAIL_APPLY_PATCH_ENABLED_01

- **fixture_id**: FAIL_APPLY_PATCH_ENABLED_01
- **category**: E — Runtime / autofix / CI failure
- **purpose**: Tester que le validateur rejette une regle avec apply_patch a true.
- **expected_verdict**: FAIL_AUTOFIX_ENABLED
- **expected_error_code**: ERR_APPLY_PATCH_ENABLED
- **related_validator_rule**: rule_schema_021
- **related_warning_family**: GOVERNANCE_DRIFT
- **related_gate**: GOVERNANCE_ALIGNMENT_REQUIRED
- **related_trace**: true
- **related_eval**: false
- **why_it_should_pass_or_fail**: apply_patch est un champ interdit. Sa presence a true doit echouer comme autofix.

```yaml
rule_id: "APPLY_PATCH_ENABLED_001"
family: "GOVERNANCE_DRIFT"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "Document affecte"
gate_required: "GOVERNANCE_ALIGNMENT_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
apply_patch: true
evidence_required:
  - "docs/source/example.md"
  - "L15"
  - "Frontmatter mismatch"
```

---

## F. No-secret failure fixtures

### FAIL_SECRET_LIKE_FIELD_01

- **fixture_id**: FAIL_SECRET_LIKE_FIELD_01
- **category**: F — No-secret failure
- **purpose**: Tester que le validateur rejette un champ contenant une valeur ressemblant a un secret.
- **expected_verdict**: FAIL_SECRET_RISK
- **expected_error_code**: ERR_SECRET_LIKE_FIELD
- **related_validator_rule**: rule_schema_022
- **related_warning_family**: (not applicable - detected before classification)
- **related_gate**: (none)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: Le champ evidence_required contient une valeur qui ressemble a un secret (FAKE_SECRET_DO_NOT_USE). Meme si le placeholder est factice, le validateur doit detecter le motif secret-like et bloquer.

```yaml
rule_id: "SECRET_LIKE_EVIDENCE_001"
family: "WHY_GAP"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "FAKE_SECRET_DO_NOT_USE"
  - "L42"
  - "Secret-like value in evidence"
```

### FAIL_TOKEN_LIKE_VALUE_01

- **fixture_id**: FAIL_TOKEN_LIKE_VALUE_01
- **category**: F — No-secret failure
- **purpose**: Tester que le validateur rejette une valeur ressemblant a un token d'API.
- **expected_verdict**: FAIL_SECRET_RISK
- **expected_error_code**: ERR_TOKEN_LIKE_VALUE
- **related_validator_rule**: rule_schema_023
- **related_warning_family**: (not applicable - detected before classification)
- **related_gate**: (none)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: Le champ evidence contient EXAMPLE_TOKEN_REDACTED qui ressemble a un token d'API, meme si c'est un placeholder factice. Le validateur doit bloquer.

```yaml
rule_id: "TOKEN_LIKE_VALUE_001"
family: "RUNTIME_SECURITY_GAP"
severity: "R1"
source_axis: "Runtime Security"
affected_axis:
  - "OpenClaw Central"
gate_required: "RUNTIME_PROOF_REQUIRED"
trace_required: true
eval_required: true
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "EXAMPLE_TOKEN_REDACTED"
  - "config_token"
  - "Token-like value in rule"
```

### FAIL_ENV_DUMP_EXAMPLE_01

- **fixture_id**: FAIL_ENV_DUMP_EXAMPLE_01
- **category**: F — No-secret failure
- **purpose**: Tester que le validateur rejette un exemple contenant un dump d'environnement.
- **expected_verdict**: FAIL_SECRET_RISK
- **expected_error_code**: ERR_ENV_DUMP_EXAMPLE
- **related_validator_rule**: rule_schema_024
- **related_warning_family**: (not applicable - detected before classification)
- **related_gate**: (none)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: Le contenu de la fixture contient une section env_dump avec des entrees de type PATH et DUMMY_CREDENTIAL_BLOCKED. Les dumps d'environnement sont interdits.

```yaml
rule_id: "ENV_DUMP_EXAMPLE_001"
family: "WHY_GAP"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/env_dump.txt"
  - "L1"
  - "Environment dump in example"
env_dump:
  PATH: "/usr/bin:/bin"
  API_KEY: "DUMMY_CREDENTIAL_BLOCKED"
  SECRET: "FAKE_SECRET_DO_NOT_USE"
```

### FAIL_PRIVATE_KEY_BLOCK_EXAMPLE_01

- **fixture_id**: FAIL_PRIVATE_KEY_BLOCK_EXAMPLE_01
- **category**: F — No-secret failure
- **purpose**: Tester que le validateur rejette un bloc de cle privee factice.
- **expected_verdict**: FAIL_SECRET_RISK
- **expected_error_code**: ERR_PRIVATE_KEY_BLOCK
- **related_validator_rule**: rule_schema_025
- **related_warning_family**: (not applicable - detected before classification)
- **related_gate**: (none)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: Meme avec un marqueur FAKE_PRIVATE_KEY_BLOCKED, la presence d'un bloc de cle privee factice dans une fixture doit etre detectee et bloquee.

```yaml
rule_id: "PRIVATE_KEY_BLOCK_001"
family: "WHY_GAP"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "configs/example/key.pem"
  - "L1"
  - "Private key block detected"
private_key_block: |
  -----BEGIN RSA PRIVATE KEY-----
  FAKE_PRIVATE_KEY_BLOCKED
  FAKE_PRIVATE_KEY_BLOCKED
  -----END RSA PRIVATE KEY-----
```

---

## G. Axis authority drift fixtures

### FAIL_WHY_LINT_AUTHORIZES_RUNTIME_01

- **fixture_id**: FAIL_WHY_LINT_AUTHORIZES_RUNTIME_01
- **category**: G — Axis authority drift
- **purpose**: Tester que le validateur detecte une regle WHY lint qui autorise une action runtime.
- **expected_verdict**: FAIL_AXIS_AUTHORITY_DRIFT
- **expected_error_code**: ERR_AUTHORITY_DRIFT_LINT_RUNTIME
- **related_validator_rule**: rule_schema_026
- **related_warning_family**: (attempting to define RUNTIME_PERMISSION)
- **related_gate**: GATE_RUNTIME
- **related_trace**: true
- **related_eval**: true
- **why_it_should_pass_or_fail**: WHY lint ne doit jamais autoriser d'action runtime. Si une regle lint pretend definir une permission d'execution, c'est un authority drift.

```yaml
rule_id: "LINT_AUTHORIZES_RUNTIME_001"
family: "RUNTIME_SECURITY_GAP"
severity: "R1"
source_axis: "WHY Lint"
affected_axis:
  - "OpenClaw Central"
gate_required: "GATE_RUNTIME"
trace_required: true
eval_required: true
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/why_lint/rule_drift.md"
  - "L5"
  - "Lint rule attempts to grant execution permission"
lint_action: "GRANT_EXECUTION_PERMISSION"
```

### FAIL_WHY_GRAPH_DEFINES_PERMISSION_01

- **fixture_id**: FAIL_WHY_GRAPH_DEFINES_PERMISSION_01
- **category**: G — Axis authority drift
- **purpose**: Tester que le validateur detecte le WHY graph qui definit des permissions.
- **expected_verdict**: FAIL_AXIS_AUTHORITY_DRIFT
- **expected_error_code**: ERR_AUTHORITY_DRIFT_GRAPH_PERM
- **related_validator_rule**: rule_schema_027
- **related_warning_family**: (attempting to define permissions from graph layer)
- **related_gate**: (none - rejected as drift)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: Le WHY graph represente, il ne definit pas de permissions. Toute regle qui fait du graph une source de permission est un drift.

```yaml
rule_id: "GRAPH_DEFINES_PERMISSION_001"
family: "RUNTIME_SECURITY_GAP"
severity: "R1"
source_axis: "WHY Runtime Graph"
affected_axis:
  - "Runtime Security"
gate_required: "RUNTIME_PROOF_REQUIRED"
trace_required: true
eval_required: true
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/why_graph/permission_overlay.md"
  - "L12"
  - "Graph layer attempts to define runtime permission"
graph_action: "DEFINE_PERMISSION_LEVEL"
```

### FAIL_OPENCLAW_TARGET_GRANTS_EXECUTION_01

- **fixture_id**: FAIL_OPENCLAW_TARGET_GRANTS_EXECUTION_01
- **category**: G — Axis authority drift
- **purpose**: Tester que le validateur detecte la cible OpenClaw qui s'auto-autorise l'execution.
- **expected_verdict**: FAIL_AXIS_AUTHORITY_DRIFT
- **expected_error_code**: ERR_AUTHORITY_DRIFT_TARGET_EXEC
- **related_validator_rule**: rule_schema_028
- **related_warning_family**: (attempting to self-grant execution)
- **related_gate**: (none - rejected as drift)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: OpenClaw central est la cible produit. Elle ne peut pas s'auto-autoriser l'execution sans passer par la gouvernance et la securite runtime.

```yaml
rule_id: "TARGET_GRANTS_EXECUTION_001"
family: "RUNTIME_SECURITY_GAP"
severity: "R1"
source_axis: "OpenClaw Central"
affected_axis:
  - "OpenClaw Central"
gate_required: "GATE_RUNTIME"
trace_required: true
eval_required: true
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/openclaw_target/self_grant.md"
  - "L8"
  - "Target product self-grants execution without governance"
target_action: "SELF_GRANT_EXECUTION"
```

### FAIL_RUNTIME_SECURITY_REPLACES_GOVERNANCE_01

- **fixture_id**: FAIL_RUNTIME_SECURITY_REPLACES_GOVERNANCE_01
- **category**: G — Axis authority drift
- **purpose**: Tester que le validateur detecte la securite runtime qui remplace la gouvernance.
- **expected_verdict**: FAIL_AXIS_AUTHORITY_DRIFT
- **expected_error_code**: ERR_AUTHORITY_DRIFT_SECURITY_GOV
- **related_validator_rule**: rule_schema_029
- **related_warning_family**: (attempting to override governance)
- **related_gate**: (none - rejected as drift)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: Runtime Security derive de la gouvernance. Elle ne peut pas remplacer ou ignorer les regles de gouvernance.

```yaml
rule_id: "SECURITY_REPLACES_GOV_001"
family: "CONTROL_PLANE_GAP"
severity: "R1"
source_axis: "Runtime Security"
affected_axis:
  - "Governance"
gate_required: "GOVERNANCE_ALIGNMENT_REQUIRED"
trace_required: true
eval_required: true
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/runtime_security/override_gov.md"
  - "L3"
  - "Security policy attempts to override governance rules"
security_action: "OVERRIDE_GOVERNANCE_RULE"
```

### FAIL_GOVERNANCE_REWRITES_PRODUCT_TARGET_01

- **fixture_id**: FAIL_GOVERNANCE_REWRITES_PRODUCT_TARGET_01
- **category**: G — Axis authority drift
- **purpose**: Tester que le validateur emet NEED_MORE_EVIDENCE quand la gouvernance reecrit la cible produit.
- **expected_verdict**: NEED_MORE_EVIDENCE
- **expected_error_code**: ERR_AUTHORITY_DRIFT_GOV_TARGET
- **related_validator_rule**: rule_schema_030
- **related_warning_family**: (governance overriding product target)
- **related_gate**: (none - insufficient evidence)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: Selon la spec, "Governance rewrites product target" retourne NEED_MORE_EVIDENCE car il n'est pas clair si la gouvernance etend ou remplace la cible produit sans preuve supplementaire.

```yaml
rule_id: "GOV_REWRITES_TARGET_001"
family: "CONTROL_PLANE_GAP"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "OpenClaw Central"
gate_required: "MULTI_MACHINE_REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/governance/target_override.md"
  - "L10"
  - "Governance doc rewrites product target scope"
governance_action: "REWRITE_PRODUCT_TARGET"
```

---

## H. Fail-closed fixtures

### BLOCKED_UNKNOWN_RULE_01

- **fixture_id**: BLOCKED_UNKNOWN_RULE_01
- **category**: H — Fail-closed
- **purpose**: Tester que le validateur bloque une regle avec un rule_id inconnu du catalogue.
- **expected_verdict**: FAIL_UNKNOWN_RULE
- **expected_error_code**: ERR_UNKNOWN_RULE_ID_ZZ_999
- **related_validator_rule**: rule_schema_031
- **related_warning_family**: (unknown - cannot classify)
- **related_gate**: (none)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: Le rule_id ZZ_999 n'existe dans aucun catalogue connu. Le validateur doit fail-closed avec FAIL_UNKNOWN_RULE.

```yaml
rule_id: "ZZ_999"
family: "WHY_GAP"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "WHY Runtime Graph"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/unknown.md"
  - "L1"
  - "Rule id not in any known catalog"
```

### NEED_MORE_EVIDENCE_MISSING_SOURCE_01

- **fixture_id**: NEED_MORE_EVIDENCE_MISSING_SOURCE_01
- **category**: H — Fail-closed
- **purpose**: Tester que le validateur demande plus de preuves quand la source est manquante.
- **expected_verdict**: NEED_MORE_EVIDENCE
- **expected_error_code**: ERR_EVIDENCE_MISSING_SOURCE_FILE
- **related_validator_rule**: rule_schema_032
- **related_warning_family**: GOVERNANCE_DRIFT (cannot verify)
- **related_gate**: (none - evidence insufficient)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: Le fichier source reference dans evidence_required n'existe pas. Le validateur ne peut pas confirmer ni infirmer le drift. Il demande plus de preuves.

```yaml
rule_id: "EVIDENCE_SOURCE_MISSING_001"
family: "GOVERNANCE_DRIFT"
severity: "R2"
source_axis: "Governance"
affected_axis:
  - "Document affecte"
gate_required: "GOVERNANCE_ALIGNMENT_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/non_existent_file.md"
  - "L1"
  - "Referenced source file does not exist on disk"
```

### BLOCKED_BY_POLICY_UNKNOWN_AXIS_01

- **fixture_id**: BLOCKED_BY_POLICY_UNKNOWN_AXIS_01
- **category**: H — Fail-closed
- **purpose**: Tester que le validateur bloque une regle avec un axe inconnu de la matrice de non-duplication.
- **expected_verdict**: BLOCKED_BY_POLICY
- **expected_error_code**: ERR_POLICY_UNKNOWN_AXIS
- **related_validator_rule**: rule_schema_033
- **related_warning_family**: (cannot classify - unknown axis)
- **related_gate**: (none)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: L'axe DATA_LAYER n'est pas reconnu par la matrice de non-duplication. Aucune politique ne peut etre appliquee. Le validateur doit bloquer avec BLOCKED_BY_POLICY.

```yaml
rule_id: "UNKNOWN_AXIS_POLICY_001"
family: "WHY_GAP"
severity: "R2"
source_axis: "DATA_LAYER"
affected_axis:
  - "OpenClaw Central"
gate_required: "REVIEW_REQUIRED"
trace_required: true
eval_required: false
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "docs/source/example.md"
  - "L42"
  - "Axis not recognized in any policy"
```

### NEED_MORE_EVIDENCE_MISSING_PROOF_01

- **fixture_id**: NEED_MORE_EVIDENCE_MISSING_PROOF_01
- **category**: H — Fail-closed
- **purpose**: Tester que le validateur demande plus de preuves quand la preuve est absente ou insuffisante.
- **expected_verdict**: NEED_MORE_EVIDENCE
- **expected_error_code**: ERR_EVIDENCE_MISSING_PROOF
- **related_validator_rule**: rule_schema_034
- **related_warning_family**: RUNTIME_SECURITY_GAP (cannot verify)
- **related_gate**: (none - evidence insufficient)
- **related_trace**: (none)
- **related_eval**: (none)
- **why_it_should_pass_or_fail**: La regle allegue un RUNTIME_SECURITY_GAP mais la preuve fournie est insuffisante (evidence_required avec des valeurs generiques). Le validateur demande plus de preuves.

```yaml
rule_id: "PROOF_INSUFFICIENT_001"
family: "RUNTIME_SECURITY_GAP"
severity: "R1"
source_axis: "Runtime Security"
affected_axis:
  - "OpenClaw Central"
gate_required: "RUNTIME_PROOF_REQUIRED"
trace_required: true
eval_required: true
autofix_allowed: false
runtime_binding: false
can_fail_ci: false
evidence_required:
  - "TODO: add source file"
  - "TODO: add line number"
  - "Proof not yet provided"
```

---

## 17_RESUME_POINT

Apres merge de ce GO, reprendre avec :

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01
```

Objectif futur :
implementer un validateur statique local, read-only, report-only, sans runtime, sans autofix, sans CI bloquante.

Mais ne pas implementer dans ce GO.

Suite immediate recommandee :
1. Revue humaine du fixture corpus.
2. Validation de la couverture des 40 fixtures.
3. Ouverture du GO d'implementation read-only.
