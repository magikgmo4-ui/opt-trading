# 30_TEST_PROCEDURE

## Procedure de test safe recommandee

### Pre-requis

- TradingView MCP observer operationnel (Phase 1-6).
- Mode mutation explicite (`-AllowMutation`).
- Aucun endpoint webhook production connecte.

### Option A — Test avec endpoint local mock

1. Ne pas utiliser l'URL webhook production.
2. Utiliser un endpoint local ou mock : `http://127.0.0.1:9999/tv-test`
3. Charger le template JSON dans TradingView via MCP (ou manuellement).
4. Declencher une alerte non critique (symbol fictif).
5. Verifier que le payload est bien forme.
6. Ne pas connecter admin-trading.
7. Supprimer ou desactiver l'alerte test manuellement apres verification.

### Option B — Validation JSON sans envoi

1. Verifier que le template JSON est syntaxiquement valide.
2. Verifier que les placeholders TradingView sont corrects.
3. Verifier que les flags de securite sont actifs (`trade_allowed: false`, etc.).
4. Ne pas envoyer d'alerte reelle.

### Etat actuel

- **PASS_DOC_ONLY** : Le template est pret et documente. Aucun envoi reel n'a ete effectue (Option B appliquee).

### Verification JSON

Le fichier `alert_webhook_template_v1.json` est un JSON valide. Tous les flags de securite sont actifs. Aucun endpoint webhook reel n'est documente dans le template.
