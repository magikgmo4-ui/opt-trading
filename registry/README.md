# Registry - Source de Vérité Centrale

Ce dossier `registry/` est la source de vérité **versionnée repo** pour décrire l’architecture et les points d’entrée d’`opt-trading`.

## Objectif
Centraliser les définitions statiques de l'infrastructure, des modules et des interfaces utilisateur, indépendamment de l'implémentation code.

Contrairement aux documents d'analyse (`docs/`) ou aux implémentations spécifiques (`modules/ui_registry_msi`), ce registre est structuré pour être consommé par des outils d'automatisation (readers, installateurs, menus).

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
- Familles standard (menu, cmd, sanity) + famille exceptionnelle admise (entrypoint) reservee aux surfaces canoniques operateur top-level non reductibles proprement a cmd/menu/sanity
- Modules cibles
- Chemins d'installation

### 5. [meta_index.yaml](./meta_index.yaml)
Vue d'ensemble méta des registres centraux et de leurs consommateurs.
- Cartographie des fichiers de registre
- Consommateurs principaux (readers)
- Portée et statut

## Statut Actuel
- **Version**: 0.1 (Initiale)
- **Consommation**: Manuelle / Consultative pour l'instant.
- **Prochaine étape**: Faire consommer ces fichiers par `ui_registry_msi` et les scripts de déploiement.

## Note Importante
Ce registre décrit la vérité **repo/package**. Il ne prouve pas, à lui seul, l’état réel du déploiement live (wrappers installés, unités systemd actives, etc.).
