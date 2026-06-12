#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"

errors=0

echo "--- SPCX V2 sanity check ---"

# Check Python files exist
for f in config.py setup_detector.py paper_logger.py perf_calculator.py runner.py; do
  if [ -f "$MODULE_DIR/$f" ]; then
    echo "  OK  $MODULE_DIR/$f"
  else
    echo "  FAIL  $MODULE_DIR/$f missing"
    errors=$((errors + 1))
  fi
done

# Check scripts exist
for s in cmd.sh menu.sh sanity_check.sh install_shortcuts.sh; do
  if [ -f "$MODULE_DIR/scripts/$s" ]; then
    echo "  OK  scripts/$s"
  else
    echo "  FAIL  scripts/$s missing"
    errors=$((errors + 1))
  fi
done

# Check Python syntax
echo "--- Python syntax ---"
cd "$ROOT_DIR"
for f in config.py setup_detector.py paper_logger.py perf_calculator.py runner.py; do
  if python3 -m py_compile "$MODULE_DIR/$f" 2>/dev/null; then
    echo "  OK  syntax: $f"
  else
    echo "  FAIL  syntax: $f"
    errors=$((errors + 1))
  fi
done

# Verify shared.logger available
if python3 -c "from shared.logger import setup_logger" 2>/dev/null; then
  echo "  OK  shared.logger importable"
else
  echo "  FAIL  shared.logger not importable"
  errors=$((errors + 1))
fi

echo ""
if [ "$errors" -eq 0 ]; then
  echo "SPCX V2 sanity: PASSED"
else
  echo "SPCX V2 sanity: $errors error(s)"
  exit 1
fi
