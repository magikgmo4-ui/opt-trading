#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading/workflow_ai"
echo "=== WORKFLOW_AI Sanity Check ==="
echo "base=$BASE"
req=(
".cursorrules"
"WORKFLOW.md"
"templates/specs.md"
"templates/tasks.md"
"templates/db_schema.md"
"templates/api_contract.md"
"prompts/cursor_agent_gated.md"
"prompts/cursor_chat_blueprint.md"
"prompts/fix_this.md"
"prompts/diff_review_checklist.md"
"scripts/backup_before_change.sh"
"scripts/workflow_ai_cmd.sh"
"scripts/workflow_ai_menu.sh"
"scripts/workflow_ai_sanity_check.sh"
"scripts/install_workflow_ai_shortcuts.sh"
)
ok=1
for f in "${req[@]}"; do
  if [[ -f "$BASE/$f" ]]; then echo "OK file: $f"; else echo "MISSING: $f"; ok=0; fi
done
if [[ "$ok" -ne 1 ]]; then echo "FAIL: sanity missing files"; exit 1; fi
echo "PASS: workflow_ai sanity OK"
