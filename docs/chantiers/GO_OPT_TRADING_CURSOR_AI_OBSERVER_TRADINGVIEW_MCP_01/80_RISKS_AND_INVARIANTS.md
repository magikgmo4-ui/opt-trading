# 80_RISKS_AND_INVARIANTS — GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01

## Invariants (a preserver absolument)

| # | Invariant | Justification | Verifie |
|---|-----------|---------------|---------|
| I1 | Webhook admin-trading reste canonique | Ne pas casser le flux existant valide par PR #199 | PASS |
| I2 | Port CDP 9222 localhost only | Securite : pas d'exposition reseau du debugger | PASS |
| I3 | tradingview-mcp hors repo opt-trading | Separation propre runtime / outillage | PASS |
| I4 | Aucun trade reel | Pas d'execution financiere depuis ce chantier | PASS |
| I5 | Toute mutation necessite flag explicite | Eviter les modifications accidentelles d'alertes | PASS |
| I6 | Tout resultat produit une trace | Auditabilite et reprise | PASS |
| I7 | Secrets jamais commites | .env, tokens, captures sensibles exclus | PASS |
| I8 | Aucun output live committe | output/.gitignore ignore *.json | PASS |
| I9 | Pas de pont admin-trading actif | Phase 5 = Option A (local manuel) | PASS |
| I10 | Pas d'appel direct CDP depuis OpenClaw | OpenClaw passe par cmd.ps1 → observer_runner.ps1 | PASS |

## Risques identifies (mis a jour Phase 6)

| # | Risque | Probabilite | Impact | Mitigation |
|---|--------|-------------|--------|------------|
| R1 | TradingView Desktop non lance | Haute | Blocage | Verification prealable CDP, message clair |
| R2 | tradingview-mcp non compatible | Moyenne | PARTIAL | Test par fonction, documenter ecarts (Phase 2) |
| R3 | Alertes de production mutees accidentellement | Faible | Critique | `-AllowMutation` gate, audit trail, forbidden liste |
| R4 | tradingview-mcp instable | Moyenne | Blocage | Timeouts, retry implicite via runner |
| R5 | Output JSON corrompu | Faible | Moyen | UTF8 sans BOM, atomic writes |
| R6 | Bridge packet active par erreur | Faible | Faible | Dry-run only, pas de transfert, pas de SSH |
| R7 | Changement upstream tradingview-mcp | Moyenne | Blocage | Scripts verificatifs (check CLI avant appel) |
| R8 | Sorties live commites par erreur | Faible | Critique | output/.gitignore ignore *.json, product_sanity check 11 |

## Etat des risques apres hardening

Tous les risques sont mitiges. Les risques residuels (R1, R2, R7) dependent de l'environnement externe (TradingView Desktop, tradingview-mcp upstream) et ne sont pas controlables par le hardening local.

## Verdict securite

**PASS** — Tous les invariants respectes. Produit local secure et verrouille.
