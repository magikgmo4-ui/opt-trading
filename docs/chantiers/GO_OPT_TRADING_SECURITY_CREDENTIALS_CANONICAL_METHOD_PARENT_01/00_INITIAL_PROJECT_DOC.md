# GO_OPT_TRADING_SECURITY_CREDENTIALS_CANONICAL_METHOD_PARENT_01

**GO_STRUCTURAL_ROLE:** GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN

## Objectif
Canoniser une méthode unique, simple et durable pour gérer tous les credentials du projet opt-trading.

## Portée
- API keys
- Bot tokens
- OAuth credentials
- Service accounts JSON
- Telegram sessions
- Webhook secrets
- DB passwords
- SSH keys
- Cookie sessions
- JWT/refresh tokens
- Chemins sensibles
- Variables sensibles

## Principe Central
Toute modification, ajout, rotation ou désactivation de credential passe par une seule fiche canonique : **CREDENTIAL_CHANGE_REQUEST**.

## Architecture Cible
- **Git Repository:** Contient uniquement contrats, registries (vides/exemples), validateurs et documentation.
- **Local Filesystem:** Les vraies valeurs résident dans `/etc/opt-trading/env.d/` ou `/etc/opt-trading/secrets/`.
- **Zéro Secret dans Git:** Aucun credential réel dans Git, `/shared`, fixtures, screenshots, logs, ou patchs.
- **Rôles & Capabilities:** Un job déclare ses besoins ; une machine déclare ses capacités.
- **Resolver & Validator:** Chargement minimaliste et validation redacted (OK/MISSING/DENIED/EXPIRED).
