#!/usr/bin/env bash
set -euo pipefail

# Desk Pro - Global Wrapper Installer
# Installs standard wrappers (menu, cmd, sanity) for all Desk Pro modules.
# Target: /usr/local/bin (requires sudo)

# Base directories
REPO_ROOT="/opt/trading"
MODULES_DIR="$REPO_ROOT/modules"
BIN_DIR="/usr/local/bin"

# List of Desk Pro modules to cover
MODULES=(
    "derivatives_collector"
    "derivatives_analyzer"
    "probability_engine"
    "decision_engine"
    "risk_engine"
    "execution_engine"
    "position_engine"
    "portfolio_engine"
    "journal_engine"
    "market_scanner"
    "opportunity_ranker"
    "liquidation_analyzer"
    "desk_pro_dashboard"
    "desk_pro_orchestrator"
    "desk_pro_runner"
    "perf_engine"
)

echo "=== Desk Pro Wrapper Installer ==="
echo "Target: $BIN_DIR"
echo "Modules: ${#MODULES[@]}"

# Helper to install a single wrapper
install_wrapper() {
    local module=$1
    local script_name=$2
    local wrapper_prefix=$3
    
    local source_script="$MODULES_DIR/$module/scripts/$script_name"
    local target_wrapper="$BIN_DIR/${wrapper_prefix}-${module}"
    
    if [ -f "$source_script" ]; then
        # Check if wrapper already exists
        if [ -L "$target_wrapper" ] || [ -f "$target_wrapper" ]; then
            echo "  [SKIP] $target_wrapper already exists."
        else
            echo "  [LINK] Creating $target_wrapper -> $source_script"
            # Create symlink
            ln -s "$source_script" "$target_wrapper"
            # Ensure executable
            chmod +x "$source_script"
        fi
    else
        echo "  [WARN] Source script not found: $source_script"
    fi
}

# Iterate over modules
for mod in "${MODULES[@]}"; do
    echo "Processing module: $mod"
    
    if [ -d "$MODULES_DIR/$mod" ]; then
        # 1. Menu Wrapper
        install_wrapper "$mod" "menu.sh" "menu"
        
        # 2. Cmd Wrapper
        install_wrapper "$mod" "cmd.sh" "cmd"
        
        # 3. Sanity Wrapper
        install_wrapper "$mod" "sanity_check.sh" "sanity"
    else
        echo "  [ERR] Module directory not found: $MODULES_DIR/$mod"
    fi
    echo ""
done

echo "=== Installation Complete ==="
echo "You can verify installation with: ls -l $BIN_DIR | grep -E 'menu-|cmd-|sanity-'"
