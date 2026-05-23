# 40_USAGE

## Installation
Le script est disponible dans `scripts/ai/workers/doc_ops_constraint_check.py`.
Il ne nécessite pas d'installation particulière.

## Utilisation manuelle
```bash
# Vérifier les contraintes pour le chantier actuel (déduit du 00_INITIAL_PROJECT_DOC.md local)
python scripts/ai/workers/doc_ops_constraint_check.py

# Forcer le mode DOC_ONLY
python scripts/ai/workers/doc_ops_constraint_check.py --mode DOC_ONLY

# Sortie JSON pour intégration CI/CD
python scripts/ai/workers/doc_ops_constraint_check.py --json
```

## Intégration recommandée
Il est recommandé de lancer ce script avant chaque commit ou lors de la préparation d'une PR si le chantier est marqué `DOC_ONLY`.
