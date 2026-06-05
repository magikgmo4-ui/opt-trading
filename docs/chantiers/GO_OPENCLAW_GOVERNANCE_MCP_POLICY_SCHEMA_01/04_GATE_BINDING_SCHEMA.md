---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01_GATE_BINDING
doc_type: gate_binding_schema
repo: opt-trading
project: opt-trading
module: governance_openclaw_mcp_policy_schema
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01
status: draft_canonical
lifecycle_stage: doc_only_spec
surface: docs/chantiers
source_kind: canonical_local
updated_at: 2026-05-13
---

# 04_GATE_BINDING_SCHEMA

## 1_MASTER_TARGET

Mapper capability classes et action families vers gates humaines.

## 2_INITIAL_PROJECT_DOC

Source directe : `GO_OPENCLAW_GOVERNANCE_HUMAN_REVIEW_GATES_01/02_GATE_TAXONOMY.md`.

## 3_INITIAL_NEED

Assurer qu'une action sensible ne puisse pas etre executee sans gate applicable.

## 4_MASTER_PROJECT_PLAN

Relier :

- capability_class -> gate_id ;
- action family -> human approval ;
- rollback required ;
- evidence required ;
- allowed verdicts.

## 6_FINAL_TARGET

Schema de binding de gate exploitable par un futur policy registry.

## 7_CANONICAL_STATE

### Binding par classe

| capability_class | gate_required | gate_id | evidence required | rollback required | allowed gate verdicts |
| --- | --- | --- | --- | --- | --- |
| `READ_ONLY` | no | `none` | source exists, bounded output | no | none |
| `READ_SANITIZED` | conditional | `GATE_SECRET` if redaction/security risk; `GATE_RUNTIME` if live probe | sanitizer rule, no-secret proof | no | `APPROVED`, `REJECTED`, `NEED_MORE_EVIDENCE`, `BLOCKED_BY_POLICY` |
| `WRITE_GATED` | yes | `GATE_DOC_WRITE` or `GATE_MCP_WRITE` | GO id, target path, diff/payload summary, sources | yes if write can be reverted; explicit `none` if no effect | same four gate verdicts |
| `RUNTIME_GATED` | yes | `GATE_RUNTIME`, `GATE_MODEL_PULL`, `GATE_OLLAMA_INSTALL`, `GATE_SERVICE_RESTART` as applicable | exact command/action, machine, timeout, no-secret/no-trade proof | yes if mutation/restart/pull/install | same four gate verdicts |
| `HUMAN_APPROVAL_REQUIRED` | yes | family-specific gate | exact action, target, risk, approver, rollback | yes for destructive/runtime/Git sensitive | same four gate verdicts |
| `BLOCKED_BY_DEFAULT` | no approval by default | `none` until reclassified by GO | policy ref, blocked reason | no action | `BLOCKED_BY_POLICY` |
| `NEVER_ALLOWED` | no | `none` | policy ref, blocked reason | no action | `BLOCKED_BY_POLICY` only |

### Binding par famille d'action

| Action family | Gate id | Human approval | Evidence | Rollback | Notes |
| --- | --- | --- | --- | --- | --- |
| chantier doc, inbox local, non-global doc update | `GATE_DOC_WRITE` | explicit GO instruction or human approval | GO id, path, diff, sources | revert patch/delete new file | valid for this GO |
| global index update | `GATE_GLOBAL_INDEX` | yes | index target, diff, source canonique, reason | revert patch | not used in this GO |
| git push / PR publication | `GATE_GIT_PUSH` | yes | branch, remote, diff, no-force proof | revert commit or close PR plan | push remains blocked here |
| branch delete | `GATE_BRANCH_DELETE` | yes strict | exact ref, merged/obsolete proof | recreate ref if hash known | cleanup forbidden in this GO |
| merge | `GATE_MERGE` | yes strict | PR/diff, tests/doc proof, reviewer status | revert merge plan | merge forbidden in this GO |
| live command / smoke / tmux status | `GATE_RUNTIME` | yes | exact command, machine, timeout, no-secret/no-trade proof | stop/restore plan | runtime forbidden in this GO |
| Ollama install | `GATE_OLLAMA_INSTALL` | yes strict | package/source/version, disk/network impact | uninstall/restore plan | install forbidden in this GO |
| model pull/download/switch | `GATE_MODEL_PULL` | yes strict | model id, source, size, license/risk, destination | remove model/restore routing | model pull gated |
| service restart | `GATE_SERVICE_RESTART` | yes strict | service, command, impact, maintenance window | restart/restore plan | restart gated |
| secret read/display/export/env dump | `GATE_SECRET` | redaction only; value display never | need statement, redaction plan, no value output | rotate/revoke plan if exposure | secret values never allowed |
| trade / broker / alert-to-trade | `GATE_TRADE` | yes strict plus trading GO | mode, risk, safeguards, no-secret proof | cancel/close/disable plan | trade execution never allowed in default MCP |
| MCP write | `GATE_MCP_WRITE` | yes | tool, target, payload summary, rollback | revert tool effect | no generic shell |
| remote command execution | `GATE_REMOTE_EXEC` | yes strict in dedicated GO | host, command, user, impact, timeout, rollback | stop/revert plan | blocked by default here |
| database mutation | `GATE_DATABASE_MUTATION` | yes strict in dedicated GO | query/migration, backup, affected rows estimate | restore backup/down migration | blocked by default here |

## 8_VALIDATED_PLAN

Gate decision record must include :

```text
gate_id
action_requested
target_surface
machine_scope
evidence
risk
rollback
approver
decision
trace_ref
```

## 9_SELECTED_SOLUTION

One gate authorizes one exact action. It does not authorize an open class of actions.

## 12_INVARIANTS

- A gate cannot approve `NEVER_ALLOWED`.
- A gate cannot approve secret value disclosure.
- A gate cannot approve generic unrestricted shell.
- A worker cannot approve its own request.
- Missing gate for sensitive action returns `BLOCKED_BY_GATE` or `BLOCKED_BY_POLICY`.

## 13_ESTABLISHED

All Human Review Gates from the prior taxonomy are represented.

## 14_HYPOTHESIS

Future policy may represent `gate_id` as list for compound actions.

## 15_REMAINING_GAP

No gate decision store exists.

## 16_TODO

Bind gates to traces and evals in `05_TRACE_EVAL_BINDING_SCHEMA.md`.

## 17_RESUME_POINT

Use this file to decide which human gate is required.

## 18_TO_DOCUMENT

Future implementation must reject sensitive actions before execution if gate decision is absent.

## 19_TO_REMEMBER

Memoire projet candidate :

```text
OpenClaw MCP gate binding is family-specific; a Git gate cannot authorize runtime, secret, trade or DB mutation.
```

## RISKS

- À qualifier.
