# GO_OPT_TRADING_SECURITY_CREDENTIALS_TELEGRAM_COLLECTOR_ROLE_SETUP_CHILD_01

**GO_STRUCTURAL_ROLE:** GO_CHILD_ATTACHED_TO_PARENT
**PARENT:** GO_OPT_TRADING_SECURITY_CREDENTIALS_CANONICAL_METHOD_PARENT_01
**DEPENDS_ON:** GO_OPT_TRADING_SECURITY_CREDENTIALS_REQUIREMENTS_INVENTORY_CHILD_01

## Objectif
Opérationnaliser le setup Telegram credentials pour le rôle `telegram_collector`, sans cibler une machine exclusivement.

## Portée
- Définition du scope précis des credentials Telegram.
- Validation des autorisations par rôle et profil machine.
- Procédure de setup local sécurisé (hors Git).
- Vérification via les scripts canoniques `validate` et `resolve`.
- Plan de test smoke sans exposition de secrets.

## Livrables
- Documentation de setup et de validation.
- Registres et templates à jour.
- Patch d'initialisation du rôle.
