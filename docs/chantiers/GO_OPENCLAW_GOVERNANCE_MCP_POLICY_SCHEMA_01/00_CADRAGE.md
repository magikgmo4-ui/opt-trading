---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01_CADRAGE
doc_type: cadrage
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

# 00_CADRAGE

## 1_MASTER_TARGET

Construire le schema canonique de policy MCP OpenClaw a partir des chantiers governance deja valides.

## 2_INITIAL_PROJECT_DOC

Sources imposees lues :

- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
- `docs/index/BRANCH_STATE.md`
- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/REPRISE.md`
- `go/GO_OPENCLAW_GOVERNANCE_CHATGPT_ORCHESTRATION_RECONCILIATION_01:docs/chantiers/GO_OPENCLAW_GOVERNANCE_CHATGPT_ORCHESTRATION_RECONCILIATION_01/`
- `go/GO_OPENCLAW_GOVERNANCE_MCP_BOUNDARY_SPEC_01:docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_BOUNDARY_SPEC_01/`
- `go/GO_OPENCLAW_GOVERNANCE_HUMAN_REVIEW_GATES_01:docs/chantiers/GO_OPENCLAW_GOVERNANCE_HUMAN_REVIEW_GATES_01/`
- `go/GO_OPENCLAW_GOVERNANCE_AGENT_TRACE_EVALS_PROFILE_01:docs/chantiers/GO_OPENCLAW_GOVERNANCE_AGENT_TRACE_EVALS_PROFILE_01/`

Note de lecture : les quatre chantiers governance precedents existent comme branches locales et ont ete lus via `git ls-tree` / `git show`, sans merge et sans checkout de ces branches.

## 3_INITIAL_NEED

Transformer la frontiere MCP, les gates humaines et le profil trace/evals en schema de policy exploitable par OpenClaw, Codex, strict workers et Ollama Lab, sans charger ni executer de runtime policy.

## 4_MASTER_PROJECT_PLAN

1. Verifier l'etat Git reel.
2. Creer la branche dediee.
3. Lire les socles MCP Boundary, Human Review Gates, Agent Trace/Evals et reconciliation ChatGPT/OpenClaw.
4. Definir les principes de policy MCP.
5. Definir les champs conceptuels du schema.
6. Relier capability classes, gates, traces, evals, verdicts et roles strict workers.
7. Produire des exemples draft compatibles YAML/JSON, non executables.
8. Fermer en closeout doc-only.

## 6_FINAL_TARGET

Schema policy MCP canonique couvrant :

- `capability_id`
- `capability_class`
- `default_status`
- `allowed_actor`
- `blocked_actor`
- `machine_scope`
- `tool_scope`
- `input_policy`
- `output_policy`
- `secret_policy`
- `gate_required`
- `gate_id`
- `trace_required`
- `eval_required`
- `rollback_required`
- `verdicts`
- `escalation_path`
- `forbidden_fields`

## 7_CANONICAL_STATE

Etat Git reel au demarrage :

```text
git status --short --branch
## sot/mainline...origin/sot/mainline

git branch --show-current
sot/mainline

git log --oneline -5
e34b9952 Merge pull request #343 from magikgmo4-ui/go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01
b21a6cd1 Merge pull request #344 from magikgmo4-ui/go/GO_OPT_TRADING_SESSION_CLOSEOUT_MULTI_CHAIN_01
7b70b223 docs: global session closeout - 4 chains closed
f6bd872b fix: guard admin-trading paper test runtime
b7a032bd Merge pull request #342 from magikgmo4-ui/go/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_03

git remote -v
origin https://github.com/magikgmo4-ui/opt-trading.git (fetch)
origin https://github.com/magikgmo4-ui/opt-trading.git (push)
```

Branche dediee creee :

```text
go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01
```

## 8_VALIDATED_PLAN

Le chantier reste strictement documentaire :

- dossier local de chantier ;
- inbox locale ;
- aucun index global modifie ;
- aucune execution runtime ;
- aucun trade ;
- aucun sudo ;
- aucun secret ;
- aucun shell libre ;
- aucun merge ;
- aucun push ;
- aucun cleanup de branche.

## 9_SELECTED_SOLUTION

Le schema est une specification conceptuelle translateable plus tard en YAML/JSON. Il n'est pas une policy chargeable, pas un middleware et pas un runtime.

## 12_INVARIANTS

- Toute action non explicitement autorisee dans le schema est `BLOCKED_BY_DEFAULT`.
- Une capability inconnue produit `BLOCKED_BY_POLICY`.
- `NEVER_ALLOWED` n'a pas de chemin d'approbation dans OpenClaw MCP.
- Gate avant action sensible.
- Trace avant verdict.
- Eval avant promotion.
- Aucun secret dans input, output, preuve, trace ou exemple.
- Aucun auto-approval.
- Aucune mutation runtime sans GO dedie.
- Aucun trade sans GO live-trading explicite.

## 13_ESTABLISHED

Les socles precedents etablissent :

- MCP Boundary : classes `READ_ONLY`, `READ_SANITIZED`, `WRITE_GATED`, `RUNTIME_GATED`, `HUMAN_APPROVAL_REQUIRED`, `BLOCKED_BY_DEFAULT`, `NEVER_ALLOWED`.
- Human Review Gates : gates `GATE_DOC_WRITE`, `GATE_GLOBAL_INDEX`, `GATE_GIT_PUSH`, `GATE_BRANCH_DELETE`, `GATE_MERGE`, `GATE_RUNTIME`, `GATE_OLLAMA_INSTALL`, `GATE_MODEL_PULL`, `GATE_SERVICE_RESTART`, `GATE_SECRET`, `GATE_TRADE`, `GATE_MCP_WRITE`, `GATE_REMOTE_EXEC`, `GATE_DATABASE_MUTATION`.
- Trace/Evals : familles `TRACE_*`, profils `EVAL_*`, verdicts PASS/FAIL/BLOCKED/NEED_MORE_EVIDENCE.

## 14_HYPOTHESIS

- La future traduction YAML/JSON reprendra les noms de champs de ce chantier.
- Les ids de trace et gate decision pourront devenir des artefacts files ou records.
- Les strict worker roles pourront etre extraits dans un registry dedie.

## 15_REMAINING_GAP

- Pas de policy runtime.
- Pas de validateur automatique.
- Pas de runner eval.
- Pas de trace store central.
- Pas de manifest MCP chargeable.

## 16_TODO

Produire les fichiers 01 a 10, l'inbox locale et le closeout.

## 17_RESUME_POINT

Reprendre par `01_POLICY_SCHEMA_PRINCIPLES.md`, puis verifier les bindings classes -> gates -> traces -> evals.

## 18_TO_DOCUMENT

- Principes.
- Champs.
- Classes.
- Gates.
- Traces/evals.
- Strict workers.
- Ollama Lab.
- Deny-by-default.
- Validation.
- Exemples draft.

## 19_TO_REMEMBER

Memoire projet candidate :

```text
GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01 convertit MCP Boundary + Human Gates + Trace/Evals en schema policy canonique doc-only, sans runtime ni index global.
```

## RISKS

- À qualifier.
