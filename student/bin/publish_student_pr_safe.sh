#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="/opt/trading"
BRANCH="student"
BASE_BRANCH="sot/mainline"
HTTPS_REMOTE="https://github.com/magikgmo4-ui/opt-trading.git"
SSH_REMOTE="git@github.com:magikgmo4-ui/opt-trading.git"
PR_BODY_FULL="/opt/trading/student/docs/PR_STUDENT_CONSOLIDATION.md"

cd "$REPO_ROOT"

echo "== student safe publish helper =="
echo "repo:   $REPO_ROOT"
echo "branch: $BRANCH"
echo "base:   $BASE_BRANCH"

current_branch="$(git branch --show-current)"
if [[ "$current_branch" != "$BRANCH" ]]; then
  echo "Switching to $BRANCH"
  git switch "$BRANCH"
fi

echo
echo "== status =="
git status --short --branch

echo
echo "== auth diagnostics =="
if ssh -o BatchMode=yes -T git@github.com >/tmp/student_github_ssh_test.log 2>&1; then
  echo "SSH auth to GitHub: OK"
  ssh_ok=1
else
  cat /tmp/student_github_ssh_test.log
  ssh_ok=0
fi

echo
echo "== push attempts =="
if git push -u origin "$BRANCH"; then
  echo "Push via configured origin succeeded"
  pushed=1
elif [[ "$ssh_ok" = "1" ]]; then
  echo "HTTPS push failed; retrying with SSH URL"
  git push -u "$SSH_REMOTE" "$BRANCH"
  pushed=1
else
  pushed=0
fi

if [[ "$pushed" != "1" ]]; then
  echo
  echo "Push could not be completed automatically."
  echo "Configured origin: $HTTPS_REMOTE"
  echo "Fallback SSH remote: $SSH_REMOTE"
  echo "PR body file: $PR_BODY_FULL"
  exit 1
fi

compare_url="https://github.com/magikgmo4-ui/opt-trading/compare/${BASE_BRANCH}...${BRANCH}?expand=1"

echo
echo "Branch pushed."
echo "Compare URL: $compare_url"

if command -v gh >/dev/null 2>&1; then
  gh pr create \
    --base "$BASE_BRANCH" \
    --head "$BRANCH" \
    --title "student: consolidate canonical workspace" \
    --body-file "$PR_BODY_FULL"
else
  echo "gh is not installed; open the compare URL above and use:"
  echo "$PR_BODY_FULL"
fi
