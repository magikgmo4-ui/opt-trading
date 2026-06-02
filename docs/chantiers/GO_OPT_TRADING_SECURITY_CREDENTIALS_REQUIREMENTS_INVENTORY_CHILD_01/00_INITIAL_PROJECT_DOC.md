# GO_OPT_TRADING_SECURITY_CREDENTIALS_REQUIREMENTS_INVENTORY_CHILD_01

**GO_STRUCTURAL_ROLE:** GO_CHILD_ATTACHED_TO_PARENT
**PARENT:** GO_OPT_TRADING_SECURITY_CREDENTIALS_CANONICAL_METHOD_PARENT_01

## Objectif
Fixer l’inventaire complet des credentials actuellement nécessaires au projet opt-trading, sans viser une machine en particulier.

## Portée
- Identification de toutes les applications et services nécessitant des secrets.
- Mapping des jobs vers les credentials requis.
- Définition des rôles autorisés à accéder à ces credentials.
- Assignation des rôles aux profils de machines.
- Identification des manques et gaps actuels.

## Livrables
- Documentation de l'inventaire complet.
- Mise à jour des registres YAML (`credentials`, `jobs`, `roles`, `machines`).
- Templates `.env.example` complétés pour chaque rôle.
- Validation via les scripts canoniques.
