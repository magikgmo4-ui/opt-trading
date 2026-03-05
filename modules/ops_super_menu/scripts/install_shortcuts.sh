#!/usr/bin/env bash
set -euo pipefail
cd /opt/trading || exit 1
ln -sf /opt/trading/modules/ops_super_menu/scripts/menu.sh /usr/local/bin/menu-ops_super
ln -sf /opt/trading/modules/ops_super_menu/scripts/cmd.sh /usr/local/bin/cmd-ops_super
ln -sf /opt/trading/modules/ops_super_menu/scripts/sanity_check.sh /usr/local/bin/sanity-ops_super
echo "OK: installed shortcuts:"
ls -lah /usr/local/bin/menu-ops_super /usr/local/bin/cmd-ops_super /usr/local/bin/sanity-ops_super
