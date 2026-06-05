# 10 - Future Test Harness Requirements

## 1_MASTER_TARGET

OpenClaw must eventually test the MCP Policy static validator against documentary fixtures while preserving fail-closed behavior and avoiding runtime binding.

## 2_INITIAL_PROJECT_DOC

This requirement note follows the static validator specification and the fixture corpus. It defines a future implementation target only.

## 3_INITIAL_NEED

The future test harness needs clear boundaries before any code is written so that fixture extraction does not become a runtime policy loader or a permissive validator shortcut.

## 4_MASTER_PROJECT_PLAN

This GO records requirements for a later harness. It does not implement parser code, test code, scripts, CI jobs, commands, or validators.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01`

## 7_CANONICAL_STATE

The future harness is allowed to read documentary Markdown fixtures only after a dedicated implementation GO approves the executable scope.

## 8_VALIDATED_PLAN

The harness requirements are:

- parse Markdown fixture documents;
- extract fenced snippets as inert candidate inputs;
- read expected verdict metadata;
- run the future static validator in read-only mode;
- compare actual verdicts to expected verdicts;
- compare actual error codes to expected error codes;
- fail closed on missing metadata;
- fail closed on ambiguous fixture ownership;
- fail closed on active YAML or JSON files outside Markdown fences;
- fail closed on secret risk;
- emit a deterministic report.

## 9_SELECTED_SOLUTION

The future harness should be specified as a read-only fixture runner. It must not mutate policies, write active configuration, start services, inspect secrets, run trade actions, or make approval decisions.

## 12_INVARIANTS

- No implementation in this GO.
- No executable file in this GO.
- No active YAML file in this GO.
- No active JSON file in this GO.
- No validator runtime in this GO.
- No runtime binding in this GO.
- No secret value in fixtures or reports.
- No auto-fix.
- No self-approval.
- No policy promotion without eval evidence.
- Fail closed on parser uncertainty.

## 13_ESTABLISHED

### Future Parser Requirements

The future parser must:

- identify fixture sections by `fixture_id`;
- identify expected verdict and expected error code;
- extract only fenced snippets explicitly marked as fixture snippets;
- reject nested or malformed fences;
- reject snippets without matching metadata;
- reject metadata without snippets unless the fixture explicitly declares no snippet;
- preserve source filename and line evidence in the report.

### Future Validator Invocation Requirements

The future harness must:

- call only the static validator approved by a later GO;
- run in read-only mode;
- avoid runtime service checks;
- avoid network calls unless a later GO explicitly allows them;
- avoid credential stores and environment dumps;
- pass inert snippets as input, not active policy files;
- fail if the validator tries to mutate files or load runtime policy.

### Future Comparison Requirements

The future harness must compare:

- actual verdict against expected verdict;
- actual error code against expected error code;
- actual blocked action against fixture metadata when present;
- actual gate evidence against related gate when present;
- actual trace family against related trace when present;
- actual eval profile against related eval when present.

### Future Fail-Closed Conditions

The future harness must return a failure report when:

- a fixture has no expected verdict;
- an invalid fixture has no expected error code;
- a valid fixture has a non-`none` expected error code;
- two fixtures share the same identifier;
- a fixture references an unknown validator rule;
- a fixture uses an unknown gate, trace, or eval identifier;
- active `.yaml`, `.yml`, or `.json` files are introduced under the fixture corpus;
- an executable script appears under the fixture corpus;
- a snippet contains a secret-like value outside approved fake placeholders;
- a validator output is missing, malformed, or ambiguous.

### Future Output Report

The future report should include:

- overall verdict;
- per-fixture verdict comparison;
- per-fixture error code comparison;
- evidence summary;
- secret risk status;
- blocked capabilities;
- missing gate bindings;
- missing trace bindings;
- missing eval bindings;
- fail-closed reason when applicable;
- next safe action.

### Future CI Requirements

CI integration is possible only after a dedicated GO approves:

- command name;
- read-only execution contract;
- fixture directory scope;
- report format;
- failure policy;
- no-secret scan behavior;
- non-runtime guarantee.

CI must never promote policy to runtime or approve gated actions.

## 14_HYPOTHESIS

A later implementation can use a simple deterministic parser, but the parser must be conservative and reject ambiguous Markdown rather than guessing.

## 15_REMAINING_GAP

No harness implementation, static validator executable, fixture extraction command, or CI wiring exists yet.

## 16_TODO

Recommended future tasks:

- define implementation language and module layout;
- create read-only parser;
- create fixture extraction tests;
- implement validator invocation boundary;
- implement deterministic report output;
- add CI only after local behavior is proven and no runtime binding exists.

## 17_RESUME_POINT

The future harness requirements are documented and ready to inform a later implementation GO.

## 18_TO_DOCUMENT

The later GO must document every command, input path, output path, and failure mode before executable harness code is accepted.

## 19_TO_REMEMBER

The fixture corpus is not a runtime policy source. The future harness must treat it as test data only.

## RISKS

- À qualifier.
