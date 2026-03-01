# ui_debug_pack_v1 — Debug Desk Pro UI / Toolbox UI / Perf UI

Objectif: collecter un diagnostic reproductible (services, ports, logs, tests curl) et fournir un menu/commandes standardisées.

## Installation (sur admin-trading)
1) Copier le zip sur la machine (ex: /tmp)
2) Dézipper:
   unzip ui_debug_pack_v1.zip -d /tmp/ui_debug_pack_v1
3) Installer:
   sudo bash /tmp/ui_debug_pack_v1/ui_debug/install.sh

Après install, vous aurez:
- menu-ui_debug
- cmd-ui_debug
- sanity-ui_debug

## Usage rapide
1) sanity:
   sanity-ui_debug
2) diagnostic complet (génère un .tgz dans /tmp):
   cmd-ui_debug diag

Le script imprime le chemin du .tgz à récupérer (scp) ou à ouvrir (cat) partiellement.
