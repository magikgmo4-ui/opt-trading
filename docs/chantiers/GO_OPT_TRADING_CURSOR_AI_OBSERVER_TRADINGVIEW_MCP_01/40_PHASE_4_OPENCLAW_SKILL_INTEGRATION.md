# 40_PHASE_4 — Intégration OpenClaw Skill

## Objectif

Faire d'OpenClaw l'orchestrateur du wrapper opt-trading, sans accès libre au port 9222.

## Rôle d'OpenClaw

- Lancer les commandes validées du wrapper opt-trading.
- Lire les exports JSON produits par le wrapper.
- Résumer l'état graphique (symbole, timeframe, indicateurs).
- Proposer des alertes (configuration assistée).
- Demander validation humaine avant toute modification.

## OpenClaw ne doit pas

- Trader.
- Modifier des alertes de production sans GO explicite.
- Accéder directement au port CDP (9222).
- Contourner le wrapper opt-trading.

## Skill cible

Le skill doit être défini dans la structure standard OpenClaw du repo.
Emplacement cible : `openclaw_skills/tradingview_observer_skill.md` ou équivalent existant.

## Critère PASS

OpenClaw peut demander un état TradingView et recevoir une sortie structurée sans mutation dangereuse.

## Résultat

**Statut** : [PASS / PARTIAL / FAIL]

**Détail** :
