#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-/opt/trading}"
HOST="$(hostname)"
TS="$(TZ=America/Montreal date --iso-8601=seconds)"
OUTDIR="${OUTDIR:-/tmp/git_sync_all}"
mkdir -p "$OUTDIR"
REPORT="$OUTDIR/sync_${HOST}_$(TZ=America/Montreal date +%Y%m%d_%H%M%S).txt"

cd "$REPO" || { echo "FAIL: repo missing at $REPO"; exit 1; }
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "FAIL: not a git repo"; exit 1; }

{
  echo "ts: $TS"
  echo "host: $HOST"
  echo "repo: $REPO"
  echo
  echo "== remote -v =="; git remote -v || true
  echo
  echo "== branch =="; git branch --show-current || true
  echo
  echo "== head =="; git rev-parse --short HEAD || true
  echo
  echo "== status (porcelain) =="; git status --porcelain || true
  echo
  echo "== fetch ==";
} > "$REPORT"

git fetch --all --prune >>"$REPORT" 2>&1 || true

{
  echo
  echo "== after fetch: status =="; git status --porcelain || true
  echo
  echo "== ahead/behind (upstream) =="
  # upstream may not be set; this is best-effort
  git rev-list --left-right --count @{u}...HEAD 2>/dev/null || echo "upstream not set"
  echo
  echo "== last 15 commits =="; git --no-pager log --oneline -15 || true
} >> "$REPORT"

# Safe pull if clean and upstream exists
CLEAN_LINES="$(git status --porcelain | wc -l | tr -d ' ')"
UPSTREAM_OK=0
git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1 && UPSTREAM_OK=1 || true

if [[ "$CLEAN_LINES" == "0" && "$UPSTREAM_OK" == "1" ]]; then
  {
    echo
    echo "== pull --ff-only =="
  } >> "$REPORT"
  git pull --ff-only >>"$REPORT" 2>&1 || {
    echo "WARN: pull failed (non-ff or other). See report." >>"$REPORT"
  }
else
  {
    echo
    echo "== pull skipped =="
    echo "clean_lines=$CLEAN_LINES upstream_ok=$UPSTREAM_OK"
    echo "If dirty: commit/stash first. If no upstream: set it (git branch -u origin/<branch>)."
  } >> "$REPORT"
fi

# Quick drift hint
{
  echo
  echo "== drift hints =="
  echo "- If this machine has local commits: push branch."
  echo "- If this machine lacks commits: pull/ff-only (after clean)."
  echo "- If untracked/dirty: decide commit vs ignore vs delete."
} >> "$REPORT"

# Log to student if possible
if [[ -x "/opt/trading/scripts/log_event_to_student.sh" ]]; then
  /opt/trading/scripts/log_event_to_student.sh git_sync_all "Git sync report" "Generated sync report: $REPORT"
fi

echo "$REPORT"
