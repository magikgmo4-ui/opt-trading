# Registry - Source de Vérité Centrale

Ce dossier `registry/` a vocation à devenir la source de vérité canonique et unique pour l'architecture du Desk Pro.

## Objectif
Centraliser les définitions statiques de l'infrastructure, des modules et des interfaces utilisateur, indépendamment de l'implémentation code.

Contrairement aux documents d'analyse (`docs/`) ou aux implémentations spécifiques (`modules/ui_registry_msi`), ce registre est structuré pour être consommé par des outils d'automatisation futurs (CI/CD, Dashboard, Orchestrateur).

## Contenu

### 1. [machines_registry.yaml](./machines_registry.yaml)
Définition des nœuds de l'infrastructure (serveurs, postes de dev, bases de données).
- Rôles
- Priorités UI
- Usages principaux

### 2. [modules_registry.yaml](./modules_registry.yaml)
Catalogue des modules fonctionnels du système.
- Domaines métier
- Visibilité opérateur
- Dépendances
- Wrappers attendus

### 3. [ui_surfaces_registry.yaml](./ui_surfaces_registry.yaml)
Inventaire des points d'entrée utilisateur (UI/UX).
- Surfaces (Menus, Dashboards, Commandes interactives)
- Cibles machines (MSI, Admin)
- Catégories d'usage

### 4. [wrappers_registry.yaml](./wrappers_registry.yaml)
Source de vérité pour les wrappers système et leurs emplacements cibles.
- Familles (menu, cmd, sanity)
- Modules cibles
- Chemins d'installation

## Statut Actuel
- **Version**: 0.1 (Initiale)
- **Consommation**: Manuelle / Consultative pour l'instant.
- **Prochaine étape**: Faire consommer ces fichiers par `ui_registry_msi` et les scripts de déploiement.

## Note Importante
Les modules existants (`ops_menu_hub`, `desk_pro_dashboard`, etc.) ne sont **pas encore** câblés sur ce registre. Ils fonctionnent avec leurs propres configurations locales. Ce registre servira de base à la future unification.
