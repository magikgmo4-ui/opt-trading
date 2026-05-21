---
doc_id: GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01_TEMPLATE
doc_type: bridge_contract_template
go_id: GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01
status: draft
---

# 10_APP_BRIDGE_CONTRACT_TEMPLATE

```yaml
app_id: <string>
purpose: <string>
source_of_truth_rank: <1-5, 1=canonique>
allowed_reads:
  - <liste des lectures autorisées>
allowed_writes:
  - <liste des écritures autorisées>
forbidden_actions:
  - <liste des actions interdites>
required_env_vars:
  - <liste des vars d'env nécessaires>
dry_run_mode: <true/false>
approval_gate: <none | human_approve | dual_confirm>
audit_log: <true/false>
rollback_or_compensating_action: <description>
evidence_ref: <path>
```
