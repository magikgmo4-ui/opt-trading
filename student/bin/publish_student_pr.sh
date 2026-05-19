#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="/opt/trading"
BRANCH="student"
BASE_BRANCH="sot/mainline"
TITLE="student: consolidate canonical workspace"
PR_BODY_FULL="/opt/trading/student/docs/PR_STUDENT_CONSOLIDATION.md"

cd "$REPO_ROOT"

echo "== student publish helper =="
echo "repo:   $REPO_ROOT"
echo "branch: $BRANCH"
echo "base:   $BASE_BRANCH"

current_branch="$(git branch --show-current)"
if [[ "$current_branch" != "$BRANCH" ]]; then
  echo "Switching to $BRANCH"
  git switch "$BRANCH"
fi

echo
echo "== local status =="
git status --short --branch

echo
echo "== pushing branch =="
git push -u origin "$BRANCH"

echo
echo "== branch pushed =="

if command -v gh >/dev/null 2>&1; then
  echo "== creating PR with gh =="
  gh pr create \
    --base "$BASE_BRANCH" \
    --head "$BRANCH" \
    --title "$TITLE" \
    --body-file "$PR_BODY_FULL"
  exit 0
fi

compare_url="https://github.com/magikgmo4-ui/opt-trading/compare/${BASE_BRANCH}...${BRANCH}?expand=1"

echo "gh is not installed; opening compare URL instead"
echo "$compare_url"

if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$compare_url" >/dev/null 2>&1 || true
fi

echo
echo "Use this PR body file when GitHub asks for the description:"
echo "$PR_BODY_FULL"
