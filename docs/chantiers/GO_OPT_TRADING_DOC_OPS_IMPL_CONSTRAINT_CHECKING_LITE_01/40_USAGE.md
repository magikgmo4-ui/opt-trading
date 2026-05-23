# 40_USAGE

## Installation
Le script est disponible dans `scripts/ai/workers/doc_ops_constraint_check.py`.
Il ne nécessite pas d'installation particulière.

## Utilisation manuelle
```bash
# Vérifier les contraintes (détecte ./00_INITIAL_PROJECT_DOC.md par défaut)
python scripts/ai/workers/doc_ops_constraint_check.py

# Utiliser un GO_ID spécifique
python scripts/ai/workers/doc_ops_constraint_check.py --go-id GO_ID_EXEMPLE

# Forcer le mode DOC_ONLY
python scripts/ai/workers/doc_ops_constraint_check.py --mode DOC_ONLY
```

## Intégration recommandée
Il est recommandé de lancer ce script avant chaque commit ou lors de la préparation d'une PR si le chantier est marqué `DOC_ONLY`.
