#!/usr/bin/env bash
# Install shortcuts — smc_ict_obs_processor
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
INSTALL_DIR="/usr/local/bin"

install_wrapper() {
  local name="$1" target="$2"
  cat > "$INSTALL_DIR/$name" <<EOF
#!/usr/bin/env bash
exec bash "$REPO_ROOT/$target" "\$@"
EOF
  chmod +x "$INSTALL_DIR/$name"
  echo "[installed] $name -> $target"
}

install_wrapper "cmd-smc_ict_obs_processor"   "modules/smc_ict_obs_processor/scripts/cmd.sh"
install_wrapper "menu-smc_ict_obs_processor"  "modules/smc_ict_obs_processor/scripts/menu.sh"
install_wrapper "sanity-smc_ict_obs_processor" "modules/smc_ict_obs_processor/scripts/sanity_check.sh"

echo "[DONE] smc_ict_obs_processor shortcuts installed"
