---
doc_id: GO_AUTOMATION_SECURITY_SECRETS_PERMISSIONS_01_STEPS
doc_type: steps
go_id: GO_AUTOMATION_SECURITY_SECRETS_PERMISSIONS_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: passed_with_evidence
---

# 10_STEPS

1. Inventorier tous les secrets (tokens, clés API, credentials) dans le périmètre
2. Définir la politique de stockage (env vars vs fichiers vs vault)
3. Définir les scopes OAuth par app externe
4. Définir la politique de rotation (fréquence, procédure)
5. Concevoir le kill switch (déclencheur, périmètre, procédure)
6. Formaliser le principe deny-by-default
7. Écrire les tests anti-secret (détection de patterns .env, token, key dans les outputs)
8. Documenter le verdict

## Critères de succès

- Tout secret est inventorié avec son usage et son scope
- Aucun secret n'est stocké dans le repo (hors env vars template)
- Le kill switch peut couper toutes les écritures automatisées
- Les tests anti-secret détectent une fuite volontaire
