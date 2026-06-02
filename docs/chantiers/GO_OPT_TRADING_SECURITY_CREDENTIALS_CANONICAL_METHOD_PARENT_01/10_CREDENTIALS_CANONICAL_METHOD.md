# Credentials Canonical Method

## Définition
La méthode canonique définit comment les secrets sont identifiés, stockés et accédés au sein de l'écosystème opt-trading.

## Naming Convention
Chaque credential possède un `credential_id` unique (ex: `telegram_bot_token_main`).

## Storage Backend Strategy
1. **Environment Variables:** Pour les secrets simples (API keys).
2. **Secret Files:** Pour les structures complexes (JSON, RSA keys).
3. **Local Store:** `/etc/opt-trading/env.d/` pour les fichiers `.env` par rôle.

## Accès aux Secrets
Les applications ne doivent jamais lire directement des fichiers `.env` arbitraires. Elles doivent utiliser le `resolver` qui injecte uniquement ce qui est nécessaire selon le job et le rôle de la machine.
