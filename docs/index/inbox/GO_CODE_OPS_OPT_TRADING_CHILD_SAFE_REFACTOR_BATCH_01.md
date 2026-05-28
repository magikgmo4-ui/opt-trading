---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_SAFE_REFACTOR_BATCH_01_INBOX
doc_type: inbox_entry
repo: opt-trading
project: opt-trading
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_SAFE_REFACTOR_BATCH_01
parent_go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: closed
lifecycle_stage: done
topic_keys: [shebang, portability, github_actions, python_version, code_ops, inbox]
surface: docs/index/inbox
source_kind: canonical
updated_at: 2026-05-28
---

# GO_CODE_OPS_OPT_TRADING_CHILD_SAFE_REFACTOR_BATCH_01 — inbox

5 corrections mécaniques appliquées (bash -n PASS) :
- R01 `desk_pro_dry_run.sh` : `#!/bin/bash` → `#!/usr/bin/env bash`
- R02 `run_task.sh` : `#!/bin/bash` → `#!/usr/bin/env bash`
- R03-R05 : 3 workflows GHA `python-version: "3.x"` → `"3.11"`
Verdict : **DONE**. Aucune mutation logique.
