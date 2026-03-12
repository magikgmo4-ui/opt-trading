#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="/usr/local/bin"

echo "Installing Validated Prompt Factory shortcuts..."

install_wrapper() {
    local src="$1"
    local dest="$2"
    if [ ! -f "$src" ]; then
        echo "Error: Source not found: $src"
        return 1
    fi
    echo "Installing $dest -> $src"
    cat <<EOF | sudo tee "$dest" > /dev/null
#!/usr/bin/env bash
exec bash "$src" "\$@"
EOF
    sudo chmod +x "$dest"
}

# Standard shortcuts pointing to root scripts
install_wrapper "$SCRIPT_DIR/../cmd.sh" "$TARGET_DIR/validated_prompt_factory_cmd"
install_wrapper "$SCRIPT_DIR/../menu.sh" "$TARGET_DIR/validated_prompt_factory_menu"

# Hub-compliant shortcuts (menu-*, cmd-*, sanity-*) for ops_super_menu integration
echo "Installing Hub-compliant symlinks..."
sudo ln -sf "$SCRIPT_DIR/../menu.sh" "$TARGET_DIR/menu-validated_prompt_factory"
sudo ln -sf "$SCRIPT_DIR/../cmd.sh" "$TARGET_DIR/cmd-validated_prompt_factory"
sudo ln -sf "$SCRIPT_DIR/../sanity.sh" "$TARGET_DIR/sanity-validated_prompt_factory"

echo "Done."
