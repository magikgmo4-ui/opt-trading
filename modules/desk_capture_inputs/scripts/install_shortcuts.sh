#!/usr/bin/env bash
set -euo pipefail
sudo ln -sf /opt/trading/modules/desk_capture_inputs/scripts/menu.sh /usr/local/bin/menu-desk_capture_inputs
sudo ln -sf /opt/trading/modules/desk_capture_inputs/scripts/cmd.sh /usr/local/bin/cmd-desk_capture_inputs
sudo ln -sf /opt/trading/modules/desk_capture_inputs/scripts/sanity_check.sh /usr/local/bin/sanity-desk_capture_inputs
echo "OK: shortcuts installed"
ls -la /usr/local/bin/*desk_capture_inputs | cat
