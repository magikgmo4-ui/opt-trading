#!/usr/bin/env bash
set -euo pipefail
SELF="$(readlink -f "${BASH_SOURCE[0]}")"
ROOT="$(cd "$(dirname "$SELF")/.." && pwd)"
exec bash "$ROOT/modules/repo_ownership_guard/sanity_check.sh" "$@"
