# 30_APPLICATION_REQUIREMENTS

## Ce qui manque pour l'application réelle

### Option A — Test avec endpoint local (PASS_DOC_ONLY → PASS_REAL)

1. Endpoint local mock disponible (`http://127.0.0.1:9999/tv-test`)
2. Charger le template dans TradingView via MCP ou manuellement
3. Déclencher une alerte non critique
4. Vérifier que le payload est bien formé
5. Supprimer l'alerte test
6. Aucune connexion admin-trading

### Option B — Validation sans envoi (PASS_DOC_ONLY — statut actuel)

- Le template JSON est valide
- Les flag de sécurité sont actifs
- Les placeholders TradingView sont corrects
- Aucun envoi réel

### Préconditions pour passage à l'application réelle

| Condition | Statut |
|---|---|
| Endpoint mock/test disponible | A VERIFIER |
| TradingView MCP observer opérationnel | PASS (Phase 1-6) |
| Mode mutation explicite (`-AllowMutation`) | REQUIS |
| Admin-trading non connecté | PASS |
| Validation sécurité explicite | A FAIRE |

### Risques

- Connexion accidentelle au webhook production admin-trading
- Déclenchement d'une alerte de production
- Modification d'alertes existantes
