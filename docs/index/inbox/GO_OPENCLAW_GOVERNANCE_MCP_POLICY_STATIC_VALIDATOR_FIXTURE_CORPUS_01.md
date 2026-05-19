# Inbox - GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01

## 1_MASTER_TARGET

Prepare a documentary fixture corpus for the future OpenClaw MCP Policy static validator.

## 2_INITIAL_PROJECT_DOC

This inbox entry points to:

`docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01/`

## 3_INITIAL_NEED

The validator specification needs inert examples with expected verdicts and expected error codes before any executable implementation exists.

## 4_MASTER_PROJECT_PLAN

Create Markdown-only fixtures and keep all YAML-like and JSON-like snippets inside Markdown fences.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_FIXTURE_CORPUS_01`

## 7_CANONICAL_STATE

The corpus is local chantier documentation. It is not an active policy source and must not be loaded by runtime.

## 8_VALIDATED_PLAN

Expected deliverables:

- 12 chantier Markdown files;
- 1 local inbox Markdown file;
- no global index updates;
- no active YAML or JSON files;
- no executable files.

## 9_SELECTED_SOLUTION

Use fenced Markdown snippets with explicit fixture metadata:

- fixture identifier;
- expected verdict;
- expected error code;
- related rule;
- related gate;
- related trace;
- related eval.

## 12_INVARIANTS

- Documentation only.
- No executable validator.
- No active YAML.
- No active JSON.
- No runtime.
- No trade.
- No sudo.
- No real secret.
- No unrestricted shell.
- No merge.
- No force push.
- No branch cleanup.
- Do not modify global indexes.
- Do not use `git add -A`.

## 13_ESTABLISHED

Target corpus categories:

- valid policy fixtures;
- schema failure fixtures;
- capability class failure fixtures;
- gate, trace, and eval failure fixtures;
- never-allowed failure fixtures;
- no-secret failure fixtures;
- strict worker failure fixtures;
- fixture index and future harness requirements.

## 14_HYPOTHESIS

The fixture corpus will be sufficient to bootstrap a later read-only static validator implementation and test harness.

## 15_REMAINING_GAP

No validator, parser, harness, runtime binding, CI job, or policy loader exists in this GO.

## 16_TODO

Review the chantier files, verify Markdown-only constraints, stage only the chantier and inbox paths, and commit on the dedicated branch.

## 17_RESUME_POINT

Static Validator Spec passed doc-only review at commit `248b6c38`; this GO creates the fixture corpus that follows it.

## 18_TO_DOCUMENT

Document the force-add exception if the no-secret fixture file is ignored because `SECRET` appears in the path.

## 19_TO_REMEMBER

NEXT_GO recommended after this corpus:

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_IMPLEMENTATION_01`
