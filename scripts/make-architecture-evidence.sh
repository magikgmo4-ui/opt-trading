#!/usr/bin/env bash
set -euo pipefail

OUT="docs/architecture/evidence"
mkdir -p "$OUT"

echo "# Repo Identity" > "$OUT/00_repo_identity.md"
{
  echo
  echo "## Git"
  git rev-parse --show-toplevel 2>/dev/null || true
  git branch --show-current 2>/dev/null || true
  git rev-parse HEAD 2>/dev/null || true
  echo
  echo "## Date"
  date -u +"%Y-%m-%dT%H:%M:%SZ"
} >> "$OUT/00_repo_identity.md"

echo "# Tree" > "$OUT/01_tree.txt"
if command -v tree >/dev/null 2>&1; then
  tree -a -I ".git|node_modules|dist|build|coverage|__pycache__|.venv|venv|.next|target|vendor" >> "$OUT/01_tree.txt"
else
  find . \
    -path "./.git" -prune -o \
    -path "./node_modules" -prune -o \
    -path "./dist" -prune -o \
    -path "./build" -prune -o \
    -path "./coverage" -prune -o \
    -path "./__pycache__" -prune -o \
    -path "./.venv" -prune -o \
    -path "./venv" -prune -o \
    -type f -print | sort >> "$OUT/01_tree.txt"
fi

echo "# Manifests" > "$OUT/02_manifests.md"
for f in \
  package.json \
  pnpm-lock.yaml \
  yarn.lock \
  package-lock.json \
  pyproject.toml \
  requirements.txt \
  poetry.lock \
  Pipfile \
  go.mod \
  Cargo.toml \
  pom.xml \
  build.gradle \
  docker-compose.yml \
  docker-compose.yaml \
  Dockerfile \
  Makefile \
  README.md
 do
  if [ -f "$f" ]; then
    echo -e "\n## $f\n" >> "$OUT/02_manifests.md"
    sed -n '1,220p' "$f" >> "$OUT/02_manifests.md"
  fi
 done

echo "# Entrypoints" > "$OUT/03_entrypoints.md"
{
  echo "## Common entrypoint candidates"
  find . \
    -path "./.git" -prune -o \
    -path "./node_modules" -prune -o \
    -path "./dist" -prune -o \
    -path "./build" -prune -o \
    -type f \( \
      -name "main.*" -o \
      -name "index.*" -o \
      -name "app.*" -o \
      -name "server.*" -o \
      -name "cli.*" -o \
      -name "__main__.py" -o \
      -name "manage.py" \
    \) -print | sort
} >> "$OUT/03_entrypoints.md"

echo "# Imports Raw" > "$OUT/04_imports_raw.txt"
if command -v rg >/dev/null 2>&1; then
  rg -n \
    "^(import |from .* import |const .* = require\(|.*require\(|export .* from |using |#include |package |func main\(|class .*|def .*|APIRouter|FastAPI|Flask|express\(|Router\()" \
    --glob '!node_modules/**' \
    --glob '!dist/**' \
    --glob '!build/**' \
    --glob '!coverage/**' \
    --glob '!vendor/**' \
    --glob '!target/**' \
    . > "$OUT/04_imports_raw.txt" || true
else
  echo "ripgrep not installed. Install rg or use IDE search." >> "$OUT/04_imports_raw.txt"
fi

echo "# External Dependencies" > "$OUT/05_external_dependencies.md"
{
  echo "## Files likely declaring external dependencies"
  find . \
    -path "./.git" -prune -o \
    -path "./node_modules" -prune -o \
    -type f \( \
      -name "package.json" -o \
      -name "pyproject.toml" -o \
      -name "requirements.txt" -o \
      -name "go.mod" -o \
      -name "Cargo.toml" -o \
      -name "pom.xml" \
    \) -print | sort
} >> "$OUT/05_external_dependencies.md"

echo "# Tests" > "$OUT/06_tests.md"
{
  echo "## Test files"
  find . \
    -path "./.git" -prune -o \
    -path "./node_modules" -prune -o \
    -type f \( \
      -name "*test*" -o \
      -name "*spec*" -o \
      -path "*/tests/*" \
    \) -print | sort
} >> "$OUT/06_tests.md"

echo "# Infra" > "$OUT/07_infra.md"
{
  echo "## Infra files"
  find . \
    -path "./.git" -prune -o \
    -path "./node_modules" -prune -o \
    -type f \( \
      -name "Dockerfile" -o \
      -name "docker-compose*.yml" -o \
      -name "docker-compose*.yaml" -o \
      -name "*.tf" -o \
      -name "*.yaml" -o \
      -name "*.yml" -o \
      -path "*/.github/workflows/*" \
    \) -print | sort
} >> "$OUT/07_infra.md"

echo "Evidence pack generated in $OUT"
