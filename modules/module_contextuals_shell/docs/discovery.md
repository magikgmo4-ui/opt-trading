# Module Contextuals Shell - V2 Discovery Layer

## Vue d'ensemble
Ce document décrit l'évolution du module vers la V2, qui ajoute une capacité de découverte automatique des modules et de leurs assets (scripts, commandes, contextuels).

## V1 (État Actuel)
La V1 fournit un socle stable pour :
- Lire un fichier contextuel (`.ctx`).
- Afficher un menu interactif.
- Router une sélection vers une cible exécutable.
- Valider son propre fonctionnement via `sanity.sh`.

## V2 (Nouvelle Couche Discovery)
La V2 étend le module sans casser la V1 pour permettre :
1. **Découverte des modules** : Lister les modules "découvrables" présents dans le dossier `modules/`.
2. **Inspection des modules** : Détecter la présence des fichiers standards (`sanity.sh`, `cmd.sh`, `menu.sh`) et des dossiers d'assets.
3. **Inventaire des assets** :
   - `scripts/*.sh` : Scripts exécutables autonomes.
   - `contextuals/*.ctx` : Fichiers de définition de menus contextuels.
   - `commands/*.txt` : Fichiers déclaratifs de commandes utiles (un fichier par commande).
4. **Vue structurée** : Produire une sortie simple (clé: valeur) facile à parser.

### Critères de Découverte
Un dossier dans `modules/` est considéré comme un "module découvrable" s'il :
- Ne commence pas par `.` (caché) ou `__` (technique).
- N'est pas un dossier technique global explicite (ex: `scripts`).
- Contient **au moins un** des éléments suivants :
  - `sanity.sh`
  - `cmd.sh`
  - `menu.sh`
  - dossier `scripts/`
  - dossier `contextuals/`
  - dossier `commands/`

Les dossiers purement techniques (comme `__pycache__`, `scripts` à la racine modules, ou des dossiers vides) sont ignorés.

### Ce que V2 ne fait pas encore
- Intégration complète avec `menu-ops_super` (c'est une étape ultérieure).
- Migration ou refactoring des anciens modules (ils restent tels quels).
- Création d'un registry global persisté (l'indexation est faite à la volée pour l'instant).

## Doctrine "1 Action = 1 Cible"
Pour garantir la fiabilité et la simplicité, la découverte repose sur des règles strictes :

1. **1 Script = 1 Action** : Un script dans `scripts/` doit être autonome et exécuter une seule tâche précise. Pas de script "couteau suisse" avec des arguments complexes cachés.
2. **1 Commande Utile = 1 Action** : Les fichiers dans `commands/` listent des commandes prêtes à l'emploi.
   - Convention : **1 Fichier = 1 Action**.
   - Nom du fichier : Explicite (ex: `show_status.txt`, `deploy_prod.txt`).
   - Contenu : La commande exacte à exécuter (ex: `python3 main.py --status`).
   - **Note** : Ces fichiers servent de documentation exécutable. Si un fichier est un exemple illustratif non jouable directement, son nom doit être explicite (ex: `example_usage.txt`).
3. **1 Contextuel = 1 Cible** : Une entrée de menu contextuel pointe vers un exécutable unique.

## Intégration future avec `menu-ops_super`
Cette couche de découverte servira de backend pour `menu-ops_super`.
- `menu-ops_super` utilisera `cmd.sh discover` pour obtenir la liste des modules.
- Il pourra ensuite interroger chaque module pour afficher ses actions disponibles dynamiquement, sans configuration manuelle centralisée.

## Utilisation
Le script `cmd.sh` expose désormais les commandes de découverte :

```bash
# Lister tous les modules découvrables
./cmd.sh list-modules

# Afficher les détails d'un module
./cmd.sh show-module <nom_module>

# Lister les scripts d'un module
./cmd.sh show-scripts <nom_module>

# Lister les contextuels d'un module
./cmd.sh show-contextuals <nom_module>

# Lister les commandes utiles d'un module
./cmd.sh show-commands <nom_module>

# Lancer une découverte complète avec détails
./cmd.sh discover
```
