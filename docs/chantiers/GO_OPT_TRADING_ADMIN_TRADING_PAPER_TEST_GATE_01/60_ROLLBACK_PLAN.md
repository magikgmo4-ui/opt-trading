# 60_ROLLBACK_PLAN

1. En cas d'anomalie : Arrêter immédiatement le processus (`CTRL+C` ou `kill`).
2. Vérifier si un fichier `ledger_live.json` a été créé (ne devrait pas).
3. Analyser les logs pour identifier la cause de l'anomalie.
4. Nettoyer les fichiers de preuves temporaires avant relance.
