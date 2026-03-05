# ops_super_menu — Step0 (Super menu per machine)

## Goal
Un "super menu" qui:
- détecte la machine (hostname) et affiche le rôle
- liste les shortcuts présents: menu-*/cmd-*/sanity-* + BROKEN symlinks
- liste les modules sous /opt/trading/modules et indique s'ils ont un menu standard/legacy/aucun
- liste les menus "scripts" existants sous /opt/trading/scripts (legacy)
- permet d'exécuter un menu (par shortcut menu-xxx ou par module)

## Install (each machine)
From /opt/trading:
- unzip ops_super_menu_step0.zip
- bash INSTALL.sh
- modules/ops_super_menu/scripts/sanity_check.sh
- sudo modules/ops_super_menu/scripts/install_shortcuts.sh
- menu-ops_super

## Notes
- Ça ne modifie PAS tes modules existants (pas de wrappers automatiques), ça fait juste un inventaire + runner.
- Option "cleanup_broken" disponible via cmd-ops_super pour supprimer les symlinks cassés.
