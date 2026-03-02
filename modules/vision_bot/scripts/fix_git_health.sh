#!/usr/bin/env bash
set -euo pipefail

echo "=== vision_bot git health fix ==="
date -Is || true

cd /opt/trading || exit 1

# Remove stray patch note file if present
rm -f PATCH_NOTES.md || true

# Ensure local artifacts are ignored
grep -qxF "_work/" .gitignore || echo "_work/" >> .gitignore
grep -qxF "PATCH_NOTES.md" .gitignore || echo "PATCH_NOTES.md" >> .gitignore

git add .gitignore

if git diff --cached --quiet; then
  echo "OK: no gitignore changes to commit."
else
  git commit -m "repo: ignore _work and PATCH_NOTES.md"
  git push
  echo "OK: committed + pushed git health fixes."
fi

git status -sb
