# Gaps and Missing Credentials

## Gaps Identifiés
1. **Telegram Sessions**: Le chemin `.session` n'est pas encore modélisé comme un credential "path".
2. **Cloud LLM Keys**: Les variables Anthropic et Gemini ne sont pas encore présentes dans les templates.
3. **DB Access**: Distinction nécessaire entre read-only et read-write pour le rôle `datacenter`.
4. **Secrets de Flotte**: SSH keys et accès VPN/WireGuard ne sont pas encore dans le registry.

## Actions à Entreprendre
- Ajouter les IDs manquants au registry `credentials.yaml`.
- Affiner les jobs dans `jobs.yaml`.
- Compléter les rôles dans `roles.yaml`.
