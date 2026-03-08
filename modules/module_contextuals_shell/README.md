# Module Contextuals Shell

**Module**: `module_contextuals_shell`  
**Role**: Socle partagé pour la gestion des actions contextuelles des modules shell.  
**Target**: Tous les futurs modules shell.

## Description
Ce module fournit une bibliothèque standardisée pour :
1. Déclarer des actions via des fichiers contextuels simples (`.ctx`).
2. Lire ces fichiers de manière robuste en shell pur.
3. Afficher des menus dynamiques basés sur ces contextes.
4. Router les actions vers les scripts cibles.

Il sert de fondation pour l'architecture "MSI First" où chaque module expose ses capacités de manière déclarative.

## Structure
- `lib/`: Bibliothèques shell (reader, renderer, router).
- `contextuals/`: Fichiers de définition d'actions (exemples ou réels).
- `examples/`: Démos d'utilisation.
- `docs/`: Documentation technique.

## Usage
Pour utiliser ce socle dans votre module :
1. Créez un fichier `.ctx` dans votre dossier `contextuals/`.
2. Sourcez `lib/reader.sh`, `lib/renderer.sh`, `lib/router.sh`.
3. Utilisez `render_menu` pour afficher les options.
4. Utilisez `route_action` pour exécuter le choix utilisateur.

## Commandes
- `./cmd.sh status`: Vérifie l'état du module.
- `./cmd.sh list`: Liste les actions de l'exemple par défaut.
- `./cmd.sh validate`: Lance les tests de santé (sanity check).
- `./cmd.sh demo`: Lance la démo interactive.

## Note importante (Windows)
Ce module repose sur des scripts Bash. Sous Windows, vous devez utiliser **Git Bash** ou **WSL** pour exécuter les commandes `.sh`.
PowerShell n'est pas supporté nativement pour l'exécution directe des scripts `.sh`.

## Intégration Future
Ce socle est conçu pour être consommé par `menu-ops_super`.
Le menu global pourra scanner les dossiers `contextuals/` des modules, lire les fichiers `.ctx`, et générer dynamiquement son index sans modification de code.
