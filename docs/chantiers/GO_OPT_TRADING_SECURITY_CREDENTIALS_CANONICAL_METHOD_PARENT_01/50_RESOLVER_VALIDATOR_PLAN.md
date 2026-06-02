# Resolver & Validator Plan

## Resolver (`scripts/env/resolve_credentials.py`)
- Prend en entrée `--machine` et `--job`.
- Identifie les rôles de la machine.
- Vérifie si le job est autorisé.
- Charge les variables d'environnement depuis `/etc/opt-trading/env.d/`.

## Validator (`scripts/env/validate_credentials.py`)
- Vérifie la présence physique des secrets requis.
- Valide le format (sans afficher la valeur).
- Rapporte l'état: `OK`, `MISSING`, `EXPIRED`.

## Redactor (`scripts/env/redact_env.py`)
- Filtre les fichiers `.env` pour supprimer les valeurs réelles avant affichage ou log.
