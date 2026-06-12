---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01_INBOX
doc_type: local_inbox_entry
status: pass_doc_only
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01
runtime_binding: false
validator_created: false
---

# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01

## 1_MASTER_TARGET

Maintenir la continuite locale du GO MCP Policy YAML Draft sans modifier les index globaux.

## 2_INITIAL_PROJECT_DOC

Chantier local :

`docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01/`

## 3_INITIAL_NEED

Creer une entree inbox courte pour signaler que le draft YAML/JSON documentaire est pose.

## 4_MASTER_PROJECT_PLAN

Lire la chaine MCP Boundary -> Human Gates -> Trace/Evals -> Policy Schema, puis documenter le draft YAML/JSON.

## 6_FINAL_TARGET

`GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01`

## 7_CANONICAL_STATE

Etat local attendu :

```text
Livrables:
12 fichiers chantier + 1 inbox locale

Index globaux:
non modifies

Runtime / trade / sudo / secret / shell libre / merge / push force / cleanup:
aucune action
```

## 8_VALIDATED_PLAN

Le chantier contient :

- cadrage ;
- principes YAML ;
- draft YAML ;
- mapping JSON ;
- capabilities ;
- bindings gate/trace/eval ;
- strict workers ;
- Ollama Lab ;
- deny-by-default ;
- checklist ;
- futur validator requirements ;
- closeout.

## 9_SELECTED_SOLUTION

Draft documentaire en Markdown, pas de fichier runtime `.yaml` ou `.json`.

## 12_INVARIANTS

- Ne pas modifier les index globaux.
- Ne pas utiliser `git add -A`.
- Laisser intacts les chemins admin-trading hors scope.
- Toute capability inconnue est `BLOCKED_BY_DEFAULT`.
- `NEVER_ALLOWED` n'a aucun approval path.

## 13_ESTABLISHED

Le draft relie :

```text
capability_class
-> gate_id
-> trace_family
-> eval_profile
-> governor_decision
```

## 14_HYPOTHESIS

Un futur GO pourra specifier un validator statique a partir de ce draft.

## 15_REMAINING_GAP

- Pas de validator.
- Pas de policy runtime.
- Pas de JSON Schema.

## 16_TODO

NEXT_GO recommande :

```text
GO_OPENCLAW_GOVERNANCE_MCP_POLICY_STATIC_VALIDATOR_SPEC_01
```

## 17_RESUME_POINT

Reprendre depuis :

`docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01/90_CLOSEOUT.md`

## 18_TO_DOCUMENT

Future documentation : validator statique, fixtures, fail-closed rules, no-secret checks.

## 19_TO_REMEMBER

Ce GO est `PASS_DOC_ONLY`. Le YAML/JSON reste documentaire, non charge et non executable.

## RISKS

- À qualifier.
