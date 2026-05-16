---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01_PRINCIPLES
doc_type: policy_schema_principles
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

# 01_POLICY_SCHEMA_PRINCIPLES

## 1_MASTER_TARGET

Definir les principes non negociables du schema de policy MCP OpenClaw.

## 2_INITIAL_PROJECT_DOC

Sources directes :

- MCP Boundary principles.
- Human Review Gate principles.
- Trace principles.
- Evals profile.

## 3_INITIAL_NEED

Eviter qu'une capacite technique MCP, Codex, strict worker ou Ollama Lab soit interpretee comme une permission operationnelle.

## 4_MASTER_PROJECT_PLAN

Chaque principe est formule comme regle de schema et doit etre verifiable par un futur validateur statique.

## 6_FINAL_TARGET

Un socle de policy utilisable avant YAML/JSON runtime.

## 7_CANONICAL_STATE

### Deny-by-default

Toute capability absente, incomplete, inconnue ou non classee est refusee.

```text
unclassified_capability -> BLOCKED_BY_POLICY
unknown_action -> BLOCKED_BY_DEFAULT
missing_required_field -> FAIL_POLICY
```

### Explicit allow only

Une autorisation existe seulement si :

- `capability_id` est defini ;
- `capability_class` est valide ;
- `default_status` est explicite ;
- les actors autorises et bloques sont explicites ;
- gates, traces et evals sont binds quand requis.

### Gate before sensitive action

Toute action write, runtime, Git sensible, index global, secret, trade, remote exec, install, restart ou DB mutation doit avoir un `gate_id` applicable avant execution.

### Trace before verdict

Aucun verdict final ne peut etre rendu sans trace referencee. Les refus sont traces comme resultats normaux.

### Eval before promotion

Toute promotion vers manifest, middleware, runtime policy ou allowlist executable exige evals statiques minimales :

- no secret leak ;
- no runtime touch ;
- gate required ;
- MCP boundary compliance ;
- trace completeness ;
- final verdict validity.

### No secret in input/output/trace

Les valeurs secretes sont interdites dans :

- input ;
- output ;
- evidence ;
- trace ;
- exemples ;
- closeout.

Les sorties peuvent indiquer `present=true` ou `REDACTED`, jamais la valeur.

### No auto-approval

Aucun agent, worker, Governor, tool MCP ou orchestrateur ne peut approuver sa propre action sensible.

### No runtime mutation without GO dedie

Une mutation runtime exige un GO dedie, un gate humain, un rollback, une trace et une eval.

### No trade without explicit live-trading GO

Tout trade paper/live, broker API, alert-to-trade ou ordre financier est bloque par defaut et `NEVER_ALLOWED` dans la frontiere MCP par defaut sans GO live-trading explicite.

## 8_VALIDATED_PLAN

Le schema doit rendre ces principes visibles dans les champs et dans les validations.

## 9_SELECTED_SOLUTION

Les principes sont appliques par composition :

```text
capability_class -> gate_binding -> trace_binding -> eval_binding -> verdict
```

## 12_INVARIANTS

- Pas de shell libre.
- Pas de sudo.
- Pas de secret.
- Pas de trade.
- Pas de bypass gate.
- Pas de trace supprimee.
- Pas de PASS sans preuve.

## 13_ESTABLISHED

MCP Boundary, Human Gates et Trace/Evals convergent sur la meme sequence :

```text
classify -> trace -> gate if sensitive -> action or block -> eval -> verdict
```

## 14_HYPOTHESIS

Le futur validateur pourra executer ces checks sans charger de runtime OpenClaw.

## 15_REMAINING_GAP

Pas encore de representation YAML/JSON normative.

## 16_TODO

Deriver les champs dans `02_POLICY_SCHEMA_FIELDS.md`.

## 17_RESUME_POINT

Reprendre ici si un futur schema semble autoriser implicitement une action.

## 18_TO_DOCUMENT

Documenter toute exception comme GO dedie, jamais comme permission implicite.

## 19_TO_REMEMBER

Memoire projet candidate :

```text
OpenClaw MCP policy est deny-by-default : seul un allow explicite, trace, gate et evalue peut devenir actionnable.
```
