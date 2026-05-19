#!/usr/bin/env bash
set -euo pipefail

# Desk Pro - Global Wrapper Installer (Robust V2)
# Installs robust shell wrappers (cd + exec) for all Desk Pro modules.
# Target: /usr/local/bin (requires sudo)
# Backups: /opt/trading/_work/operator_surface_standardization/backups/<timestamp>

# Base directories
REPO_ROOT="/opt/trading"
MODULES_DIR="$REPO_ROOT/modules"
BIN_DIR="/usr/local/bin"
WORK_DIR="$REPO_ROOT/_work/operator_surface_standardization"
BACKUP_DIR="$WORK_DIR/backups/$(date +%Y%m%d_%H%M%S)"

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

echo "=== Desk Pro Wrapper Installer (Robust) ==="
echo "Target: $BIN_DIR"
echo "Backup: $BACKUP_DIR"
echo "Modules: ${#MODULES[@]}"

mkdir -p "$BACKUP_DIR"

# Helper to create a robust wrapper content
generate_wrapper_content() {
    local module=$1
    local script_name=$2
    
    cat <<EOF
#!/usr/bin/env bash
# Desk Pro Wrapper: $module / $script_name
set -e

# Jump to module directory to resolve relative paths
cd "$MODULES_DIR/$module" || {
    echo "Error: Module directory not found at $MODULES_DIR/$module"
    exit 1
}

# Execute target script with all arguments
if [ -f "scripts/$script_name" ]; then
    exec bash "scripts/$script_name" "\$@"
else
    echo "Error: Target script 'scripts/$script_name' not found in $module"
    exit 1
fi
EOF
}

# Helper to install a single wrapper
install_wrapper() {
    local module=$1
    local script_name=$2
    local wrapper_prefix=$3
    
    local source_script="$MODULES_DIR/$module/scripts/$script_name"
    local target_wrapper="$BIN_DIR/${wrapper_prefix}-${module}"
    
    if [ -f "$source_script" ]; then
        # 1. Backup if exists
        if [ -f "$target_wrapper" ] || [ -L "$target_wrapper" ]; then
            echo "  [BACKUP] $target_wrapper -> $BACKUP_DIR/"
            mv "$target_wrapper" "$BACKUP_DIR/"
        fi
        
        # 2. Create Robust Wrapper
        echo "  [CREATE] $target_wrapper (Pointing to $module/scripts/$script_name)"
        generate_wrapper_content "$module" "$script_name" > "$target_wrapper"
        chmod +x "$target_wrapper"
        
        # 3. Ensure source is executable too
        chmod +x "$source_script"
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
echo "Backups stored in: $BACKUP_DIR"
echo "Verify with: ./scripts/check_desk_pro_wrappers.sh"
