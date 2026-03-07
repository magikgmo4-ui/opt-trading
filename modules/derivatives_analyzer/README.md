# Derivatives Analyzer

**Module**: `derivatives_analyzer`  
**Type**: Desk Pro Module (Analytical)  
**Status**: V1 (Local/Paper)

## Description
Le module `derivatives_analyzer` est un moteur d'analyse quantitatif conçu pour transformer les données brutes de marchés dérivés (Open Interest, Funding Rates, Ratios) en signaux actionnables pour le trading.

Il agit comme un filtre intermédiaire entre le `derivatives_collector` (qui collecte la donnée brute) et le `probability_engine` (qui calcule les probabilités de succès).

## Objectifs V1
- Analyser la structure du marché (Crowding, Leverage).
- Détecter les risques de Squeeze (Long/Short).
- Identifier le biais directionnel des dérivés.
- Produire une sortie standardisée JSON.

## Architecture
Le module est autonome et fonctionne sur fichiers JSON locaux.

```
modules/derivatives_analyzer/
├── app/
│   └── derivatives_analyzer.py  # Logique métier principale (CLI argparse)
├── config/
│   └── sample_input.json        # Données de test
├── output/                      # Dossier de sortie par défaut
├── scripts/
│   ├── cmd.sh                   # Wrapper CLI
│   ├── menu.sh                  # Interface opérateur
│   └── sanity_check.sh          # Tests de santé
└── README.md
```

## Logique d'Analyse (V1)

### 1. États Dérivés
| Indicateur | Condition | État |
|---|---|---|
| **Funding** | > 0.01% | POSITIVE |
| | > 0.03% | EXTREME_POSITIVE |
| | < -0.01% | NEGATIVE |
| | < -0.03% | EXTREME_NEGATIVE |
| **Open Interest** | Change > 2% | RISING |
| | Change < -2% | FALLING |

### 2. Risques & Biais
- **Squeeze Risk**: Déclenché si Funding Extrême + OI Rising/Flat.
- **Crowding**: Basé sur le Long/Short Ratio et l'accumulation d'OI.
- **Bias**: Synthèse du Funding et de l'OI (ex: Funding Positif + OI Rising = Bullish Leverage).

## Commandes Principales

Le module s'utilise via son wrapper `cmd.sh` ou directement via Python.

### Via Wrapper (Recommandé)

```bash
# Statut du module
bash modules/derivatives_analyzer/scripts/cmd.sh status

# Voir le sample input
bash modules/derivatives_analyzer/scripts/cmd.sh sample

# Analyse (utilise sample_input.json par défaut)
bash modules/derivatives_analyzer/scripts/cmd.sh analyze

# Analyse d'un fichier spécifique
bash modules/derivatives_analyzer/scripts/cmd.sh analyze data/my_derivatives.json

# Explication de la logique
bash modules/derivatives_analyzer/scripts/cmd.sh explain

# Export vers fichier (utilise sample_input.json par défaut vers output/derivatives_analysis.json)
bash modules/derivatives_analyzer/scripts/cmd.sh export
```

### Via Python (Direct)

```bash
# Statut
python -m modules.derivatives_analyzer.app.derivatives_analyzer status

# Analyse
python -m modules.derivatives_analyzer.app.derivatives_analyzer analyze --input modules/derivatives_analyzer/config/sample_input.json

# Export
python -m modules.derivatives_analyzer.app.derivatives_analyzer export --input modules/derivatives_analyzer/config/sample_input.json --output modules/derivatives_analyzer/output/my_analysis.json
```

## Intégration Future
Ce module fournira les métriques `squeeze_risk` et `crowding_score` au `probability_engine` pour ajuster la taille des positions et les stop-loss.
