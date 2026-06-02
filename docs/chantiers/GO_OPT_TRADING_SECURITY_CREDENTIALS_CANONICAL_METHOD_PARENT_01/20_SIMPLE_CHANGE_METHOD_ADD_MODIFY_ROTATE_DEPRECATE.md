# Simple Change Method: ADD / MODIFY / ROTATE / DEPRECATE

Toute action sur un secret doit suivre ce workflow via une `CREDENTIAL_CHANGE_REQUEST`.

## ADD
1. Création de l'entrée dans le registry `credentials.yaml`.
2. Définition des rôles autorisés.
3. Mise à jour des templates `.env.example`.
4. Validation locale via `scripts/env/validate_credentials.py`.

## MODIFY
Modification des méta-données (expiration, description, scope) dans le registry.

## ROTATE
Procédure de remplacement de la valeur réelle sur le filesystem local sans modification du code (si l'ID reste identique).

## DEPRECATE
1. Marquage comme `deprecated` dans le registry.
2. Alerting lors de la validation.
3. Suppression après migration complète des jobs dépendants.
