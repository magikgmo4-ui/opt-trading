# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01 -- 07_CI_WORKFLOW_DRAFT_MARKDOWN_ONLY

## 1_MASTER_TARGET

Provide a Markdown-only future workflow draft for the MCP Policy static validator and fixture harness.

## 2_INITIAL_PROJECT_DOC

This file contains an inert workflow sketch. It is not a `.github/workflows` file and is not active CI.

## 3_INITIAL_NEED

Future activation needs a concrete workflow shape, but this GO must not create a real workflow or trigger GitHub Actions.

## 4_MASTER_PROJECT_PLAN

Keep the example inside a fenced Markdown block only. Do not create `.yml` or `.yaml` files.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_CI_DRAFT_01`

## 7_CANONICAL_STATE

No active workflow is created by this GO. The following block is documentary only.

## 8_VALIDATED_PLAN

Draft workflow, inert Markdown fence only:

```yaml
# DRAFT ONLY - DO NOT COPY INTO .github/workflows WITHOUT GATE_CI_ACTIVATION.
name: OpenClaw MCP Policy Static Validator

on:
  pull_request:
    paths:
      - "modules/governance/openclaw_mcp_policy_validator/**"
      - "tests/test_openclaw_mcp_policy_validator.py"
      - "tests/test_openclaw_mcp_policy_fixture_harness.py"
      - "docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/**"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  static-validator:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Install test dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install pytest

      - name: Run validator tests
        run: python -m pytest tests/test_openclaw_mcp_policy_validator.py -q

      - name: Run fixture harness tests
        run: python -m pytest tests/test_openclaw_mcp_policy_fixture_harness.py -q

      - name: Run fixture corpus harness
        run: python -m modules.governance.openclaw_mcp_policy_validator.fixture_harness docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01

      - name: Diff check
        run: git diff --check
```

## 9_SELECTED_SOLUTION

The draft intentionally excludes:

- secrets;
- environment dumps;
- service containers;
- MCP server calls;
- Ollama calls;
- OpenClaw runtime calls;
- broker or trade commands;
- sudo;
- workflow artifact upload until a later report policy exists.

## 12_INVARIANTS

- This file is Markdown.
- The workflow text is fenced.
- No `.github/workflows` file is created.
- No active YAML CI file is added.
- No active JSON CI file is added.
- No runtime binding is enabled.
- No CI action is triggered by this GO.

## 13_ESTABLISHED

The future workflow draft includes:

- checkout;
- setup python;
- install test dependencies;
- run validator tests;
- run harness tests;
- run corpus harness;
- run diff check;
- read-only permissions.

## 14_HYPOTHESIS

Checkout and dependency installation may require platform network access in future CI. That does not authorize validator or harness network behavior.

## 15_REMAINING_GAP

Activation is blocked until:

- warning policy is resolved or accepted;
- human approval is recorded;
- active workflow path is approved;
- rollback path is documented.

## 16_TODO

Future activation GO must review this draft and adjust exact Python version, dependency method, path filters, and report behavior.

## 17_RESUME_POINT

This Markdown fence is the only workflow-shaped artifact created in this GO.

## 18_TO_DOCUMENT

Future workflow activation must cite this draft and record every deviation.

## 19_TO_REMEMBER

Do not create `.github/workflows` from this draft without `GATE_CI_ACTIVATION`.

## RISKS

- À qualifier.
