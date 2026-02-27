#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading/workflow_ai"
case "${1:-}" in
sanity) bash "$BASE/scripts/workflow_ai_sanity_check.sh" ;;
backup) shift || true; bash "$BASE/scripts/backup_before_change.sh" "${1:-change}" ;;
open-rules) echo "$BASE/.cursorrules" ;;
print-prompt)
  case "${2:-agent}" in
    agent) cat "$BASE/prompts/cursor_agent_gated.md" ;;
    blueprint) cat "$BASE/prompts/cursor_chat_blueprint.md" ;;
    fix) cat "$BASE/prompts/fix_this.md" ;;
    diffcheck) cat "$BASE/prompts/diff_review_checklist.md" ;;
    *) echo "Unknown prompt"; exit 2 ;;
  esac ;;
*) echo "Usage: cmd-workflow_ai <sanity|backup|open-rules|print-prompt>"; exit 2 ;;
esac
