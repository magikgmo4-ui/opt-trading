---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01_JSON_MAPPING
doc_type: policy_json_mapping_draft
status: draft_doc_only
module: governance_openclaw_mcp_policy_yaml_draft
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01
runtime_binding: false
validator_created: false
---

# 03_POLICY_JSON_MAPPING_DRAFT

## 1_MASTER_TARGET

Decrire une correspondance JSON conceptuelle pour le draft YAML, sans generer de script, de fichier `.json` actif ou de validator.

## 2_INITIAL_PROJECT_DOC

Source directe : `02_POLICY_YAML_DRAFT.md`.

## 3_INITIAL_NEED

Preparer une future traduction YAML -> JSON tout en conservant ce GO dans le perimetre doc-only.

## 4_MASTER_PROJECT_PLAN

Le mapping est exprime comme objet JSON d'exemple dans Markdown. Il est non executable et incomplet volontairement sur les tableaux tres longs, qui restent normatifs dans les fichiers de tables.

## 6_FINAL_TARGET

Mapping JSON documentaire equivalent aux sections YAML principales.

## 7_CANONICAL_STATE

Tout objet JSON futur devra conserver :

- `runtime_binding: false` tant qu'aucun GO runtime n'existe ;
- `default_status: BLOCKED_BY_DEFAULT` ;
- `unknown_capability: BLOCKED_BY_DEFAULT` ;
- `NEVER_ALLOWED.approval_path: none` ;
- absence de champs interdits.

## 8_VALIDATED_PLAN

Regles de mapping :

| YAML path | JSON path | Remarque |
| --- | --- | --- |
| `policy` | `policy` | Objet metadata principal. |
| `default_policy` | `default_policy` | Regles globales fail-closed. |
| `capability_classes` | `capability_classes` | Objet indexe par class id. |
| `gates` | `gates` | Objet indexe par gate id. |
| `traces.families` | `traces.families` | Objet indexe par trace family. |
| `evals.profiles` | `evals.profiles` | Objet indexe par eval id. |
| `strict_worker_roles` | `strict_worker_roles` | Objet indexe par role id. |
| `ollama_lab_policy.entries` | `ollama_lab_policy.entries` | Objet indexe par capability Ollama. |
| `capabilities` | `capabilities` | Objet indexe par capability id. |
| `governor_decision_rules` | `governor_decision_rules` | Tableau de regles ordonnees. |
| `never_allowed` | `never_allowed` | Objet sans approval path. |
| `blocked_by_default` | `blocked_by_default` | Objet de refus implicite. |
| `examples` | `examples` | Objet d'exemples conceptuels. |

## 9_SELECTED_SOLUTION

Exemple JSON conceptuel :

```json
{
  "policy": {
    "id": "OPENCLAW_MCP_POLICY_DRAFT_01",
    "policy_version": "0.1-doc-only",
    "status": "draft_doc_only",
    "source_go": "GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01",
    "source_schema_go": "GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01",
    "runtime_binding": false,
    "validator_created": false,
    "active_config_mutation": false,
    "default_status": "BLOCKED_BY_DEFAULT",
    "unknown_capability": "BLOCKED_BY_DEFAULT",
    "secret_policy": "no_secret_allowed",
    "trade_policy": "no_trade_without_explicit_live_trading_go",
    "unrestricted_shell_policy": "never_exposed_by_mcp",
    "sudo_policy": "never_exposed_by_mcp",
    "forbidden_fields": [
      "secret_value",
      "token_value",
      "password",
      "api_key_value",
      "private_key",
      "credential_blob",
      "raw_env",
      "raw_runtime_log",
      "unrestricted_command",
      "sudo_password",
      "broker_order_payload",
      "approval_self_granted"
    ]
  },
  "default_policy": {
    "deny_by_default": true,
    "explicit_allow_only": true,
    "fail_closed": true,
    "missing_gate_binding": "BLOCKED_BY_POLICY",
    "missing_trace_binding": "FAIL_POLICY",
    "missing_eval_binding": "FAIL_POLICY",
    "secret_detected": "FAIL_SECRET_RISK",
    "runtime_mutation_without_gate": "FAIL_RUNTIME_TOUCH",
    "unknown_or_unclassified_action": "BLOCKED_BY_DEFAULT"
  },
  "capability_classes": {
    "READ_ONLY": {
      "default_allowed": true,
      "default_status": "ALLOWED_IF_SCOPE_MATCH",
      "gate_required": false,
      "gate_id": null,
      "trace_required": true,
      "trace_family": "TRACE_MCP_CALL",
      "eval_required": true,
      "eval_profile": "EVAL_MCP_BOUNDARY_COMPLIANCE",
      "approval_path": null
    },
    "READ_SANITIZED": {
      "default_allowed": true,
      "default_status": "ALLOWED_IF_SANITIZED",
      "gate_required": false,
      "conditional_gate_required": true,
      "gate_id": "required_if_raw_or_live",
      "trace_required": true,
      "trace_family": "TRACE_RUNTIME_READ",
      "eval_required": true,
      "eval_profile": "EVAL_NO_SECRET_LEAK",
      "approval_path": "conditional"
    },
    "WRITE_GATED": {
      "default_allowed": false,
      "default_status": "BLOCKED_UNTIL_GATE",
      "gate_required": true,
      "gate_id": "GATE_DOC_WRITE",
      "trace_required": true,
      "trace_family": "TRACE_CODEX_PATCH",
      "eval_required": true,
      "eval_profile": "EVAL_DOC_ONLY_COMPLIANCE",
      "rollback_required": true,
      "approval_path": "human_gate"
    },
    "RUNTIME_GATED": {
      "default_allowed": false,
      "default_status": "BLOCKED_UNTIL_GATE",
      "gate_required": true,
      "gate_id": "GATE_RUNTIME",
      "trace_required": true,
      "trace_family": "TRACE_RUNTIME_GATED_ACTION",
      "eval_required": true,
      "eval_profile": "EVAL_GATE_APPROVAL_VALID",
      "rollback_required": true,
      "approval_path": "human_gate"
    },
    "HUMAN_APPROVAL_REQUIRED": {
      "default_allowed": false,
      "default_status": "BLOCKED_UNTIL_HUMAN_APPROVAL",
      "gate_required": true,
      "gate_id": "gate_by_action_family",
      "trace_required": true,
      "trace_family": "TRACE_HUMAN_GATE",
      "eval_required": true,
      "eval_profile": "EVAL_GATE_APPROVAL_VALID",
      "rollback_required": true,
      "approval_path": "human_gate"
    },
    "BLOCKED_BY_DEFAULT": {
      "default_allowed": false,
      "default_status": "BLOCKED_BY_DEFAULT",
      "gate_required": false,
      "gate_id": null,
      "trace_required": true,
      "trace_family": "TRACE_MCP_CALL",
      "eval_required": true,
      "eval_profile": "EVAL_MCP_BOUNDARY_COMPLIANCE",
      "approval_path": "none_until_reclassified_by_go"
    },
    "NEVER_ALLOWED": {
      "default_allowed": false,
      "default_status": "NEVER_ALLOWED",
      "gate_required": false,
      "gate_id": null,
      "trace_required": true,
      "trace_family": "TRACE_VERDICT",
      "eval_required": true,
      "eval_profile": "EVAL_FINAL_VERDICT_VALIDITY",
      "rollback_required": "not_applicable",
      "approval_path": null
    }
  },
  "gates": {
    "GATE_DOC_WRITE": {
      "action_family": "doc_chantier_or_local_inbox_write",
      "human_approval_required": true,
      "evidence_required": ["go_id", "target_path", "diff_summary", "source_refs"],
      "rollback_required": true,
      "allowed_verdicts": ["APPROVED", "REJECTED", "NEED_MORE_EVIDENCE", "BLOCKED_BY_POLICY"]
    },
    "GATE_RUNTIME": {
      "action_family": "live_command_or_runtime_probe",
      "human_approval_required": true,
      "evidence_required": ["exact_command", "machine", "timeout", "no_secret_proof", "no_trade_proof"],
      "rollback_required": true,
      "allowed_verdicts": ["APPROVED", "REJECTED", "NEED_MORE_EVIDENCE", "BLOCKED_BY_POLICY"]
    }
  },
  "traces": {
    "required_for_all_decisions": true,
    "families": {
      "TRACE_MCP_CALL": {"eval": "EVAL_MCP_BOUNDARY_COMPLIANCE"},
      "TRACE_HUMAN_GATE": {"eval": "EVAL_GATE_APPROVAL_VALID"},
      "TRACE_RUNTIME_GATED_ACTION": {"eval": "EVAL_GATE_APPROVAL_VALID"},
      "TRACE_SECRET_BLOCK": {"eval": "EVAL_NO_SECRET_LEAK"},
      "TRACE_TRADE_BLOCK": {"eval": "EVAL_MCP_BOUNDARY_COMPLIANCE"},
      "TRACE_VERDICT": {"eval": "EVAL_FINAL_VERDICT_VALIDITY"}
    }
  },
  "evals": {
    "promotion_requires_eval": true,
    "profiles": {
      "EVAL_DOC_ONLY_COMPLIANCE": {"pass_requires": ["doc_only_scope", "no_runtime", "no_trade", "no_secret"]},
      "EVAL_NO_SECRET_LEAK": {"pass_requires": ["no_secret_values", "no_raw_env", "redaction_if_needed"]},
      "EVAL_GATE_APPROVAL_VALID": {"pass_requires": ["human_decision_present", "evidence_present", "rollback_present", "no_self_approval"]},
      "EVAL_FINAL_VERDICT_VALIDITY": {"pass_requires": ["verdict_allowed", "evidence_refs_present", "blocked_reason_if_blocked"]}
    }
  },
  "capabilities": {
    "repo_state": {
      "capability_class": "READ_ONLY",
      "default_status": "ALLOWED_IF_SCOPE_MATCH",
      "gate_required": false,
      "gate_id": null,
      "trace_required": true,
      "trace_family": "TRACE_MCP_CALL",
      "eval_required": true,
      "eval_profile": "EVAL_MCP_BOUNDARY_COMPLIANCE",
      "verdicts": ["PASS_DOC_ONLY", "FAIL_POLICY", "BLOCKED_WITH_REASON"]
    },
    "create_doc_file": {
      "capability_class": "WRITE_GATED",
      "default_status": "BLOCKED_UNTIL_GATE_OR_EXPLICIT_GO_SCOPE",
      "gate_required": true,
      "gate_id": "GATE_DOC_WRITE",
      "trace_required": true,
      "trace_family": "TRACE_CODEX_PATCH",
      "eval_required": true,
      "eval_profile": "EVAL_DOC_ONLY_COMPLIANCE",
      "rollback_required": true,
      "verdicts": ["PASS_DOC_ONLY", "FAIL_POLICY", "BLOCKED_BY_GATE"]
    },
    "secret_read": {
      "capability_class": "NEVER_ALLOWED",
      "default_status": "NEVER_ALLOWED",
      "allowed_actor": [],
      "blocked_actor": ["all"],
      "gate_required": false,
      "gate_id": null,
      "approval_path": null,
      "trace_required": true,
      "trace_family": "TRACE_SECRET_BLOCK",
      "eval_required": true,
      "eval_profile": "EVAL_NO_SECRET_LEAK",
      "verdicts": ["FAIL_SECRET_RISK", "BLOCKED_BY_POLICY", "NEVER_ALLOWED"]
    }
  },
  "governor_decision_rules": [
    "if capability_id is missing then BLOCKED_BY_DEFAULT",
    "if capability_class is NEVER_ALLOWED then NEVER_ALLOWED",
    "if forbidden_field is present then FAIL_POLICY",
    "if secret value is detected then FAIL_SECRET_RISK",
    "if runtime mutation has no gate then FAIL_RUNTIME_TOUCH",
    "if worker approves own action then BLOCKED_BY_POLICY"
  ],
  "never_allowed": {
    "approval_path": null,
    "capabilities": ["unrestricted_shell", "sudo", "secret_read", "credential_export", "trade_execution"]
  },
  "blocked_by_default": {
    "unknown_capability": true,
    "unclassified_action": true,
    "missing_required_field": true,
    "missing_gate_binding": true,
    "missing_trace_binding": true,
    "missing_eval_binding": true,
    "global_index_write_without_gate": true,
    "destructive_action_without_rollback": true
  }
}
```

## 12_INVARIANTS

- Ce mapping ne genere aucun fichier JSON actif.
- Ce mapping ne valide aucune entree.
- Ce mapping n'est pas un schema JSON Schema.
- Les valeurs `null` expriment `none`, pas un chemin d'approbation implicite.
- Toute future conversion doit refuser les champs interdits.

## 13_ESTABLISHED

Les noms de sections YAML peuvent etre convertis en cles JSON sans changement semantique.

## 14_HYPOTHESIS

Un futur GO pourra choisir entre :

- JSON Schema ;
- parser YAML + conversion JSON ;
- policy registry statique ;
- validator CLI fail-closed.

## 15_REMAINING_GAP

- Pas de JSON Schema.
- Pas de test de round-trip YAML -> JSON.
- Pas de signature ou hash de policy.
- Pas de store de decisions.

## 16_TODO

- Reporter la generation effective dans un futur GO.
- Ne pas creer de fichier `.json` dans ce chantier.

## 17_RESUME_POINT

Le mapping JSON est un guide de forme. Le contenu normatif reste dans le draft YAML et les tables de ce chantier.

## 18_TO_DOCUMENT

Le futur validator devra documenter les conversions `none` -> `null`, les tableaux obligatoires, les champs interdits et la politique d'erreur.

## 19_TO_REMEMBER

JSON equivalent ne signifie pas runtime-ready. Sans validator et gate dedies, ce mapping reste une documentation.

## RISKS

- À qualifier.
