#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/infra-context}"

echo "Installing shortcuts for infra-context..."
sudo ln -sf "$ROOT/scripts/infra_context_menu.sh" /usr/local/bin/menu-infra_context
sudo ln -sf "$ROOT/scripts/infra_context_cmd.sh" /usr/local/bin/cmd-infra_context
echo "OK: /usr/local/bin/menu-infra_context and cmd-infra_context"
