# ops_wrappers — Step 0
Auto-generate minimal wrapper menus for modules that have:
- no standard scripts/menu.sh
- AND no existing /usr/local/bin/menu-<module> shortcut.

These wrappers are **inspect-only** (README / file list / grep entrypoints / git status).

## Commands
- sanity: `modules/ops_wrappers/scripts/sanity_check.sh`
- scan: `modules/ops_wrappers/scripts/cmd.sh scan`
- generate: `modules/ops_wrappers/scripts/cmd.sh generate`
- install shortcuts: `sudo modules/ops_wrappers/scripts/cmd.sh install_shortcuts`
- generate+install: `sudo modules/ops_wrappers/scripts/cmd.sh generate_and_install`
