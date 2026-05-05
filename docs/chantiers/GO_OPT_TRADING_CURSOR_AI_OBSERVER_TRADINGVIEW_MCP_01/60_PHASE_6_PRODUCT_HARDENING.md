# 60_PHASE_6 — Hardening produit

## Objectif

Transformer l'intégration en outil stable, documenté, sécurisé et testable.

## Axes de hardening

- **Logs propres** : tracer chaque opération avec timestamp et statut
- **Timeouts** : chaque appel MCP doit avoir un timeout, défaut 10s
- **Détection TradingView fermé** : précondition obligatoire avant tout appel
- **Détection port 9222 absent** : vérification préalable `http://127.0.0.1:9222/json/version`
- **Vérification localhost** : le port ne doit répondre que sur `127.0.0.1`
- **Mode read-only par défaut** : toute commande mutation nécessite un flag explicite
- **Mode mutation verrouillé** : flag `--allow-mutation` obligatoire pour créer/supprimer
- **Suppression automatique des alertes test** : cleanup après chaque session de test
- **Documentation opérateur** : README.md dans modules/tradingview_observer
- **Sanity command** : `sanity_check.ps1` doit retourner OK/KO
- **Closeout complet** : checklist de vérification finale

## Critère PASS

Un opérateur peut relancer le système sans dépendre d'une session ChatGPT.
Toutes les commandes de sanity et smoke retournent OK.

## Résultat

**Statut** : [PASS / PARTIAL / FAIL]

**Checklist** :

| Axe | Statut |
|-----|--------|
| Logs propres | |
| Timeouts | |
| Détection TV fermé | |
| Détection port absent | |
| Vérification localhost | |
| Mode read-only défaut | |
| Flag mutation explicite | |
| Cleanup alertes test | |
| Documentation opérateur | |
| Sanity command | |
| Closeout complet | |
