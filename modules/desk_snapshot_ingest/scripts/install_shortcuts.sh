#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ln -sf "$BASE/scripts/menu.sh" /usr/local/bin/menu-desk_snapshot_ingest
ln -sf "$BASE/scripts/cmd.sh" /usr/local/bin/cmd-desk_snapshot_ingest
ln -sf "$BASE/scripts/sanity_check.sh" /usr/local/bin/sanity-desk_snapshot_ingest
echo "OK: shortcuts installed"
ls -lah /usr/local/bin/menu-desk_snapshot_ingest /usr/local/bin/cmd-desk_snapshot_ingest /usr/local/bin/sanity-desk_snapshot_ingest
