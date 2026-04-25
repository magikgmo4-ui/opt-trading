# PROMPT — OPENCLAW GATEWAY

## OBJECTIF

Créer un endpoint local permettant à Botpress de déclencher des actions.

## SPEC

Endpoint:
POST /api/operator/execute

## INPUT

{
  "intent": "...",
  "payload": {},
  "meta": {}
}

## ACTION

Router vers:
- student scripts
- trading labs
- LONA

## OUTPUT

{
  "status": "success",
  "result": {},
  "safety": {}
}

## CONTRAINTES

- timeout
- gestion erreurs
- logs
