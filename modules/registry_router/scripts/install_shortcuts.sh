#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="/usr/local/bin"

echo "Installing Registry Router shortcuts..."

# Helper function
install_wrapper() {
    local src="$1"
    local dest="$2"
    
    if [ ! -f "$src" ]; then
        echo "Error: Source not found: $src"
        return 1
    fi
    
    echo "Installing $dest -> $src"
    # Create wrapper script that delegates to the source
    # We use a wrapper instead of a symlink to handle relative paths correctly
    cat <<EOF | sudo tee "$dest" > /dev/null
#!/usr/bin/env bash
exec bash "$src" "\$@"
EOF
    sudo chmod +x "$dest"
}

# Install shortcuts
install_wrapper "$SCRIPT_DIR/menu.sh" "$TARGET_DIR/menu-registry_router"
install_wrapper "$SCRIPT_DIR/cmd.sh" "$TARGET_DIR/cmd-registry_router"
install_wrapper "$SCRIPT_DIR/sanity_check.sh" "$TARGET_DIR/sanity-registry_router"

echo "Done."
echo "You can now use:"
echo "  menu-registry_router"
echo "  cmd-registry_router"
echo "  sanity-registry_router"
