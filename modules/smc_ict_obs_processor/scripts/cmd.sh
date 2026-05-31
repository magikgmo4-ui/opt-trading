#!/usr/bin/env bash
# CLI entry point — smc_ict_obs_processor
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$REPO_ROOT"
exec python3 -m modules.smc_ict_obs_processor.app.smc_ict_obs_processor "$@"
