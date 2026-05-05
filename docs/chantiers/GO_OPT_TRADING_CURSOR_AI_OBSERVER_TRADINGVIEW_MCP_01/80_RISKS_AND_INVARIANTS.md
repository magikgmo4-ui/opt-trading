# 80_RISKS_AND_INVARIANTS — GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01

## Invariants (à préserver absolument)

| # | Invariant | Justification |
|---|-----------|---------------|
| I1 | Webhook admin-trading reste canonique | Ne pas casser le flux existant validé par PR #199 |
| I2 | Port CDP 9222 localhost only | Sécurité : pas d'exposition réseau du debugger |
| I3 | tradingview-mcp hors repo opt-trading | Séparation propre runtime / outillage |
| I4 | Aucun trade réel | Pas d'exécution financière depuis ce chantier |
| I5 | Toute mutation nécessite flag explicite | Éviter les modifications accidentelles d'alertes |
| I6 | Tout résultat produit une trace | Auditabilité et reprise |
| I7 | Secrets jamais commités | .env, tokens, captures sensibles exclus |

## Risques identifiés

| # | Risque | Probabilité | Impact | Mitigation |
|---|--------|-------------|--------|------------|
| R1 | TradingView Desktop non lancé ou port 9222 fermé | Haute | Blocage smoke | Vérification préalable http://127.0.0.1:9222/json/version |
| R2 | tradingview-mcp non compatible avec la version TradingView Desktop | Moyenne | Smoke PARTIAL | Tester les fonctions une par une, documenter les écarts |
| R3 | Claude Code pas configuré comme client MCP | Moyenne | Blocage phase 1 | Documenter précisément la config MCP attendue |
| R4 | Modification accidentelle d'alertes de production | Faible | Critique | Mode read-only par défaut, flag mutation explicite, audit trail |
| R5 | tradingview-mcp instable ou crash | Moyenne | Blocage smoke | Timeouts, retry, détection port absent |
| R6 | OpenClaw non disponible ou non configuré | Moyenne | Phase 4 bloquée | Phase 4 peut être préparée documentairement sans exécution |
| R7 | Conflit de port 9222 avec autre outil | Faible | Blocage smoke | Vérification préalable, changer port si nécessaire |
| R8 | Dépendance à la session ChatGPT pour reprise | Haute | Perte de continuité | Documentation exhaustive dans le repo |
