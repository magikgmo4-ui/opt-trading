#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${1:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODULE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

bash "$MODULE_ROOT/cmd.sh" audit "$REPO_ROOT" --output-dir "$MODULE_ROOT/output"
