#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading/workflow_ai"
while true; do
cat <<'MENU'
=== Workflow AI Menu ===
1) Sanity check
2) Backup before change
3) Show .cursorrules path
4) Print prompt: Agent (gated)
5) Print prompt: Chat Blueprint
6) Print prompt: Fix this
7) Print prompt: Diff review checklist
q) Quit
MENU
read -r -p "> " choice
case "$choice" in
1) bash "$BASE/scripts/workflow_ai_sanity_check.sh" ;;
2) read -r -p "Topic: " topic; bash "$BASE/scripts/backup_before_change.sh" "${topic:-change}" ;;
3) echo "$BASE/.cursorrules" ;;
4) cat "$BASE/prompts/cursor_agent_gated.md" ;;
5) cat "$BASE/prompts/cursor_chat_blueprint.md" ;;
6) cat "$BASE/prompts/fix_this.md" ;;
7) cat "$BASE/prompts/diff_review_checklist.md" ;;
q|Q) exit 0 ;;
*) echo "Invalid." ;;
esac
echo
done
