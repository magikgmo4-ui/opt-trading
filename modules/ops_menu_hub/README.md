# Ops Menu Hub (MSI Toolbox)

**Module**: `ops_menu_hub`  
**Role**: Central Operator Toolbox (MSI V1)  
**Target**: `admin-trading`, `student`

## Objectif
Ce module sert de point d'entrée unifié (MSI) pour l'opérateur. Il regroupe les wrappers existants en catégories logiques pour faciliter la navigation et l'exécution des tâches courantes.

Il ne remplace pas les wrappers individuels (ex: `cmd-probability_engine`) mais offre une vue d'ensemble structurée.

## Structure du Hub (MSI)

Le hub organise les outils en 4 groupes fonctionnels :

### 1. Operator
Outils de pilotage quotidien du Desk Pro.
- `cmd-desk_pro_runner`: Exécution principale
- `cmd-desk_capture_inputs`: Saisie manuelle
- `cmd-desk_analyze`: Analyse à la demande
- `cmd-desk_pro_dashboard`: Vue d'ensemble

### 2. Analysis
Moteurs de calcul et d'analyse quantitative.
- `cmd-derivatives_collector`: Collecte de données
- `cmd-derivatives_analyzer`: Analyse structurelle
- `cmd-probability_engine`: Scoring directionnel
- `cmd-market_scanner`: Scan d'opportunités
- `cmd-decision_engine`: Prise de décision
- `cmd-risk_engine`: Gestion des risques

### 3. Monitoring
Surveillance de la santé et de la performance.
- `menu-perf`: Performance système
- `cmd-desk_state`: État du desk
- `menu-vision_bot`: Logs visuels
- `cmd-desk_retention`: Nettoyage

### 4. Maintenance
Outils de diagnostic et de gestion des wrappers.
- `sanity-*`: Checks de santé par module
- `cmd-ops_wrappers`: Gestion des wrappers
- `cmd-ops_super`: Super-admin tools

## Usage

### Mode Menu Interactif
Lancez le menu principal pour naviguer :
```bash
menu-ops_menu_hub
```

### Mode Commande (CLI)
Affichez la structure du hub sans interaction :
```bash
cmd-ops_menu_hub msi
# ou
cmd-ops_menu_hub show-msi
```

## Installation
Ce module est déployé via `scripts/install_desk_pro_wrappers.sh` qui crée les liens globaux :
- `menu-ops_menu_hub`
- `cmd-ops_menu_hub`
- `sanity-ops_menu_hub`
