# GO_OPT_TRADING_SECURITY_CREDENTIALS_DESKPRO_ROLE_SETUP_CHILD_01

**GO_STRUCTURAL_ROLE:** GO_CHILD_ATTACHED_TO_PARENT
**PARENT:** GO_OPT_TRADING_SECURITY_CREDENTIALS_CANONICAL_METHOD_PARENT_01
**DEPENDS_ON:** GO_OPT_TRADING_SECURITY_CREDENTIALS_REQUIREMENTS_INVENTORY_CHILD_01

## Objectif
Opérationnaliser le setup DeskPro credentials pour le rôle `deskpro_user`.

## Portée
- Définition du scope des configurations DeskPro (API URL, API Key, chemins locaux).
- Validation des autorisations par rôle et profil machine.
- Procédure de setup local sécurisé (hors Git).
- Vérification via les scripts canoniques `validate` et `resolve`.

## Livrables
- Documentation de setup et de validation.
- Registres et templates à jour.
- Patch d'initialisation du rôle.
