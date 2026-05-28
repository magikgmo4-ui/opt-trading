---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_BAK_01_INBOX
doc_type: inbox_entry
repo: opt-trading
project: opt-trading
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_BAK_01
parent_go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: blocked
lifecycle_stage: blocked_permissions
topic_keys: [cleanup, bak, code_ops, inbox]
surface: docs/index/inbox
source_kind: canonical
updated_at: 2026-05-28
---

# GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_BAK_01 — inbox

D06 bloqué — répertoires `.bak` propriété `root:root`.
Action manuelle requise :
```bash
sudo rm -rf /opt/trading/modules/install_module_openclaw.bak_20260314
sudo rm -rf /opt/trading/modules/ops_wrappers.bak
```
Aucun commit git requis (gitignorés). Preuve d'absence de consommateur établie.
Verdict : **BLOCKED_PERMISSIONS**.
