# install_module_openclaw

Module standard pour installer les modules OpenClaw via un menu et des commandes pré-enregistrées.

## Objectif
- arrêter les séquences répétitives pénibles ;
- déployer les modules OpenClaw comme les autres modules du projet ;
- conserver `sanity`, `cmd`, `menu`, `install_shortcuts`.

## Principe
Le module lit un registre local de modules disponibles, puis copie le module choisi vers une racine cible.

## Par défaut
- source bundle : dossier parent du bundle courant
- cible : `/opt/trading`

## Commandes rapides
- `cmd-install_module_openclaw list`
- `cmd-install_module_openclaw install openclaw_config_modulaire`
- `cmd-install_module_openclaw status`
