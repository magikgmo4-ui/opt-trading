# Trae Module Validator V1

## Objectif
Outil de validation structurelle minimale pour les modules durables.

## Fonctionnalités
- Vérifie la présence des scripts standards (`cmd.sh`, `menu.sh`, `sanity.sh`).
- Tolère les scripts dans `scripts/` (legacy) mais encourage la racine (nouveau standard).
- Vérifie la structure minimale (`app/`, `lib/`, `scripts/`).
- Vérifie la présence de `README.md`.

## Utilisation

```bash
# Valider un module spécifique
bash modules/trae_module_validator/cmd.sh validate validated_prompt_factory

# Valider tous les modules
bash modules/trae_module_validator/cmd.sh validate-all
```

## Standards V1
- **Scripts** : `cmd.sh`, `menu.sh`, `sanity.sh` à la racine du module.
- **Legacy supporté** : Scripts dans `scripts/` (déclenche un WARN).
- **Sanity** : `sanity.sh` (préféré) ou `sanity_check.sh` (legacy accepté).
