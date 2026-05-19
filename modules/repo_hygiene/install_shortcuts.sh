#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS="$ROOT/scripts"

echo "[repo_hygiene] ROOT=$ROOT"

# Create scripts (thin wrappers) if missing (kept in repo for versioning)
chmod +x "$ROOT/modules/repo_hygiene/sanity_check.sh" || true
chmod +x "$ROOT/modules/repo_hygiene/repo_hygiene_lib.sh" || true

# Ensure wrapper scripts are executable
chmod +x "$SCRIPTS/repo_hygiene_cmd.sh" "$SCRIPTS/repo_hygiene_menu.sh" "$SCRIPTS/repo_hygiene_sanity.sh" || true

# Install global shortcuts
for name in menu-repo_hygiene cmd-repo_hygiene sanity-repo_hygiene; do
  sudo rm -f "/usr/local/bin/$name"
done

sudo ln -s "$SCRIPTS/repo_hygiene_menu.sh" /usr/local/bin/menu-repo_hygiene
sudo ln -s "$SCRIPTS/repo_hygiene_cmd.sh"  /usr/local/bin/cmd-repo_hygiene
sudo ln -s "$SCRIPTS/repo_hygiene_sanity.sh" /usr/local/bin/sanity-repo_hygiene

echo "OK: installed /usr/local/bin/menu-repo_hygiene, cmd-repo_hygiene, sanity-repo_hygiene"
