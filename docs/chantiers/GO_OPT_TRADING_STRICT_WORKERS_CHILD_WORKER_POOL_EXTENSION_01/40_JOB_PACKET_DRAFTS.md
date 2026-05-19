---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01_JOB_PACKET_DRAFTS
doc_type: job_packet_draft
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01
status: draft_canonical
lifecycle_stage: draft
topic_keys:
  - opt-trading
  - strict_workers
  - job_packets
  - json
  - drafts
surface: chantier
source_kind: canonical
updated_at: 2026-05-19
links:
  - scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json
  - scripts/ai/workers/tasks.index.json
  - docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
---

# 40_JOB_PACKET_DRAFTS

Brouillons JSON pour job packets. Ne pas écrire dans scripts/ai/workers/job_packets/ avant validation explicite.
Ces brouillons sont doc-only, stockés dans ce fichier markdown.

---

## GO_STRICT_WORKERS_READ_INVENTORY_MATRIX_01

```json
{
  "job_packet_id": "GO_STRICT_WORKERS_READ_INVENTORY_MATRIX_01",
  "go_id": "GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01",
  "task": "READ_INVENTORY",
  "status": "DRAFT_ONLY",
  "autonomy_max": "A1",
  "writes_code": false,
  "model": "opencode/qwen3.5-plus",
  "fallback_models": ["opencode/minimax-m2.5", "opencode/kimi-k2.5", "opencode/big-pickle"],
  "inputs": {
    "allowed": ["docs/**", "scripts/**", "modules/**", "config/**", "tests/**"],
    "denied": [".env", "**/.env", "**/*secret*", "**/*token*", "**/*credential*", "**/id_rsa", "**/id_ed25519", "**/*.pem", "**/*.key"]
  },
  "denied_commands": ["git add", "git commit", "git push", "git rebase", "git merge", "rm -rf", "chmod -R", "chown -R"],
  "output": {
    "path": "reports/ai/workers/read_inventory_matrix_01.md",
    "required_sections": ["13_ESTABLISHED", "14_HYPOTHESIS", "15_REMAINING_GAP", "16_TODO", "FICHIERS_LUS", "RISQUES", "VERDICT_DRAFT_ONLY"]
  },
  "validation": {
    "type": "model_fort_tests",
    "required": true
  },
  "stop_conditions": ["sensitive_file_detected", "empty_output"],
  "healthcheck": "test -x scripts/ai/workers/run_task.sh && test -f scripts/ai/workers/tasks.index.json"
}
```

---

## GO_STRICT_WORKERS_PATCH_DRAFT_MATRIX_01

```json
{
  "job_packet_id": "GO_STRICT_WORKERS_PATCH_DRAFT_MATRIX_01",
  "go_id": "GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01",
  "task": "PATCH_DRAFT",
  "status": "DRAFT_ONLY",
  "autonomy_max": "A2",
  "writes_code": false,
  "model": "opencode/glm-5.1",
  "fallback_models": ["opencode/kimi-k2.6", "opencode/glm-5", "opencode/qwen3.6-plus", "opencode/big-pickle"],
  "inputs": {
    "allowed": ["docs/**", "scripts/**", "modules/**", "tests/**"],
    "denied": [".env", "**/.env", "**/*secret*", "**/*token*", "**/*credential*", "**/id_rsa", "**/id_ed25519", "**/*.pem", "**/*.key"]
  },
  "denied_commands": ["git add", "git commit", "git push", "git rebase", "git merge", "rm -rf", "chmod -R", "chown -R"],
  "output": {
    "path": "reports/ai/workers/patch_draft_matrix_01.md",
    "required_sections": ["OBJECTIF_PATCH", "FICHIERS_TOUCHES", "DIFF_ATTENDU", "RISQUES", "TESTS_A_EXECUTER", "VERDICT_DRAFT_ONLY"]
  },
  "validation": {
    "type": "model_fort_tests_git_diff",
    "required": true
  },
  "stop_conditions": ["patch_touches_secrets", "diff_exceeds_100_lines", "git_write_command_detected"],
  "max_diff_lines": 100,
  "dry_run_required": true,
  "healthcheck": "test -x scripts/ai/workers/run_task.sh && test -f scripts/ai/workers/tasks.index.json"
}
```

---

## GO_STRICT_WORKERS_DOC_DRAFT_MATRIX_01

```json
{
  "job_packet_id": "GO_STRICT_WORKERS_DOC_DRAFT_MATRIX_01",
  "go_id": "GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01",
  "task": "DOC_DRAFT",
  "status": "DRAFT_ONLY",
  "autonomy_max": "A2",
  "writes_code": false,
  "model": "opencode/qwen3.5-plus",
  "fallback_models": ["opencode/qwen3.6-plus", "opencode/minimax-m2.5", "opencode/big-pickle", "opencode/nemotron-3-super-free"],
  "inputs": {
    "allowed": ["docs/**", "reports/**"],
    "denied": [".env", "**/.env", "**/*secret*", "**/*token*", "**/*credential*", "**/id_rsa", "**/id_ed25519", "**/*.pem", "**/*.key"]
  },
  "denied_commands": ["git add", "git commit", "git push", "git rebase", "git merge", "rm -rf", "chmod -R", "chown -R"],
  "output": {
    "path": "reports/ai/workers/doc_draft_matrix_01.md",
    "required_sections": ["CONTEXTE", "ETAT_INITIAL", "CHANGEMENTS", "VALIDATIONS", "LIMITES", "POINT_DE_REPRISE", "VERDICT_DRAFT_ONLY"]
  },
  "validation": {
    "type": "revue_externe",
    "required": true
  },
  "stop_conditions": ["draft_overwrites_existing_file", "contains_secrets"],
  "healthcheck": "test -x scripts/ai/workers/run_task.sh && test -f scripts/ai/workers/tasks.index.json"
}
```

---

## GO_STRICT_WORKERS_TESTPLAN_MATRIX_01

```json
{
  "job_packet_id": "GO_STRICT_WORKERS_TESTPLAN_MATRIX_01",
  "go_id": "GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01",
  "task": "TESTPLAN",
  "status": "DRAFT_ONLY",
  "autonomy_max": "A2",
  "writes_code": false,
  "model": "opencode/glm-5.1",
  "fallback_models": ["opencode/qwen3.6-plus", "opencode/kimi-k2.6", "opencode/glm-5", "opencode/minimax-m2.7"],
  "inputs": {
    "allowed": ["modules/**", "scripts/**", "tests/**"],
    "denied": [".env", "**/.env", "**/*secret*", "**/*token*", "**/*credential*", "**/id_rsa", "**/id_ed25519", "**/*.pem", "**/*.key"]
  },
  "denied_commands": ["git add", "git commit", "git push", "git rebase", "git merge", "rm -rf", "chmod -R", "chown -R", "pytest", "npm test", "make test"],
  "output": {
    "path": "reports/ai/workers/testplan_matrix_01.md",
    "required_sections": ["TESTS_UNITAIRES", "TESTS_SMOKE", "COMMANDES", "CRITERES_PASS_FAIL", "RISQUES_RESTANTS", "VERDICT_DRAFT_ONLY"]
  },
  "validation": {
    "type": "model_fort_tests_execution",
    "required": true
  },
  "stop_conditions": ["destructive_test_suggested", "invalid_test_commands"],
  "healthcheck": "test -x scripts/ai/workers/run_task.sh && test -f scripts/ai/workers/tasks.index.json"
}
```

---

## GO_STRICT_WORKERS_CHERRY_PICK_INVENTORY_MATRIX_01

```json
{
  "job_packet_id": "GO_STRICT_WORKERS_CHERRY_PICK_INVENTORY_MATRIX_01",
  "go_id": "GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01",
  "task": "CHERRY_PICK_INVENTORY",
  "status": "DRAFT_ONLY",
  "autonomy_max": "A2",
  "writes_code": false,
  "model": "opencode/kimi-k2.5",
  "fallback_models": ["opencode/kimi-k2.6", "opencode/glm-5.1", "opencode/qwen3.6-plus", "opencode/big-pickle"],
  "inputs": {
    "allowed": ["git log", "git diff", "git show"],
    "denied": [".env", "**/.env", "**/*secret*", "**/*token*", "**/*credential*", "**/id_rsa", "**/id_ed25519", "**/*.pem", "**/*.key"]
  },
  "denied_commands": ["git add", "git commit", "git push", "git rebase", "git merge", "git cherry-pick", "rm -rf", "chmod -R", "chown -R"],
  "output": {
    "path": "reports/ai/workers/cherry_pick_inventory_matrix_01.md",
    "required_sections": ["COMMITS_CANDIDATS", "FICHIERS_TOUCHES", "DEPENDANCES", "RISQUES_CONFLITS", "ORDRE_RECOMMANDE", "COMMANDES_NON_EXECUTEES", "VERDICT_DRAFT_ONLY"]
  },
  "validation": {
    "type": "revue_externe_stricte",
    "required": true
  },
  "stop_conditions": ["conflict_detected", "force_push_proposed", "commits_not_found"],
  "healthcheck": "test -x scripts/ai/workers/run_task.sh && git rev-parse --git-dir"
}
```

---

## GO_STRICT_WORKERS_FAST_TRIAGE_MATRIX_01

```json
{
  "job_packet_id": "GO_STRICT_WORKERS_FAST_TRIAGE_MATRIX_01",
  "go_id": "GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01",
  "task": "FAST_TRIAGE",
  "status": "DRAFT_ONLY",
  "autonomy_max": "A1",
  "writes_code": false,
  "model": "opencode/qwen3.5-plus",
  "fallback_models": ["opencode/minimax-m2.5", "opencode/gpt-5-nano", "opencode/deepseek-v4-flash-free"],
  "inputs": {
    "allowed": ["docs/**", "scripts/**", "modules/**"],
    "denied": [".env", "**/.env", "**/*secret*", "**/*token*", "**/*credential*", "**/id_rsa", "**/id_ed25519", "**/*.pem", "**/*.key"]
  },
  "denied_commands": ["git add", "git commit", "git push", "git rebase", "git merge", "rm -rf", "chmod -R", "chown -R"],
  "output": {
    "path": "reports/ai/workers/fast_triage_matrix_01.md",
    "required_sections": ["RESUME", "CLASSEMENT", "RISQUES", "TODO", "VERDICT_DRAFT_ONLY"]
  },
  "validation": {
    "type": "revue_echantillon",
    "required": true
  },
  "stop_conditions": ["incoherent_classification", "empty_todo"],
  "healthcheck": "test -x scripts/ai/workers/run_task.sh"
}
```

---

## GO_STRICT_WORKERS_ENDPOINT_AUDIT_MATRIX_01

```json
{
  "job_packet_id": "GO_STRICT_WORKERS_ENDPOINT_AUDIT_MATRIX_01",
  "go_id": "GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01",
  "task": "ENDPOINT_AUDIT",
  "status": "DRAFT_ONLY",
  "autonomy_max": "A1",
  "writes_code": false,
  "model": "opencode/qwen3.5-plus",
  "fallback_models": ["opencode/minimax-m2.5", "opencode/big-pickle"],
  "inputs": {
    "allowed": ["https://opencode.ai/zen/v1/models", "scripts/ai/workers/models.registry.json"],
    "denied": [".env", "**/.env", "**/*secret*", "**/*token*", "**/*credential*", "**/id_rsa", "**/id_ed25519", "**/*.pem", "**/*.key"]
  },
  "denied_commands": ["git add", "git commit", "git push", "git rebase", "git merge", "rm -rf", "chmod -R", "chown -R"],
  "output": {
    "path": "reports/ai/workers/endpoint_audit_matrix_01.md",
    "required_sections": ["ENDPOINT_CONSULTE", "MODELES_TROUVES", "COMPARAISON_REGISTRY", "AJOUTS", "RETRAITS", "RECOMMANDATIONS", "VERDICT_DRAFT_ONLY"]
  },
  "validation": {
    "type": "test_read_only",
    "required": true
  },
  "stop_conditions": ["endpoint_unreachable", "auto_registry_update_attempted"],
  "healthcheck": "curl -s -o /dev/null -w '%{http_code}' https://opencode.ai/zen/v1/models"
}
```

---

## GO_STRICT_WORKERS_WRITE_GATED_DRYRUN_MATRIX_01

```json
{
  "job_packet_id": "GO_STRICT_WORKERS_WRITE_GATED_DRYRUN_MATRIX_01",
  "go_id": "GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01",
  "task": "WRITE_GATED",
  "status": "DRAFT_ONLY",
  "autonomy_max": "A4",
  "writes_code": true,
  "dry_run_required": true,
  "model": "opencode/glm-5.1",
  "fallback_models": ["opencode/qwen3.6-plus", "opencode/kimi-k2.6", "opencode/big-pickle"],
  "inputs": {
    "allowed": ["docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_*/**", "reports/ai/workers/**", "scripts/ai/workers/job_packets/**"],
    "denied": [".env", "**/.env", "**/*secret*", "**/*token*", "**/*credential*", "**/id_rsa", "**/id_ed25519", "**/*.pem", "**/*.key"]
  },
  "write_allowlist": ["docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_**/*.md", "docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_**/BRANCH_STATE.md", "reports/ai/workers/*.md", "scripts/ai/workers/job_packets/*.json"],
  "forbidden_targets": ["docs/index/GO_INDEX.md", "docs/index/BRANCH_STATE.md", "scripts/ai/workers/run_task.sh", "scripts/ai/workers/_validate_job.py", "scripts/ai/workers/models.registry.json", "scripts/ai/workers/tasks.index.json"],
  "max_lines_per_write": 50,
  "denied_commands": ["git add", "git commit", "git push", "git rebase", "git merge", "rm -rf", "chmod -R", "chown -R"],
  "output": {
    "path": "reports/ai/workers/write_gated_dryrun_matrix_01.md",
    "required_sections": ["13_ESTABLISHED", "14_HYPOTHESIS", "WRITE_PLAN", "WRITE_DIFF_ATTENDU", "VALIDATION_EXTERNE", "DRY_RUN_RESULT", "RISQUES", "VERDICT_WRITE_GATED"]
  },
  "validation": {
    "type": "approbation_ecrite_explicite_dry_run",
    "required": true
  },
  "stop_conditions": ["dry_run_fail", "write_outside_allowlist", "exceeds_50_lines", "forbidden_target_detected"],
  "healthcheck": "test -x scripts/ai/workers/run_task.sh && test -f scripts/ai/workers/tasks.index.json"
}
```
