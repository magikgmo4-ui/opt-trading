# STRATEGY — INDEX

Zone documentaire dédiée aux stratégies à cadrer avant conformité et implémentation dans le moteur commun de trading.

## Rôle

Cette zone sert à :
- figer les versions documentaires des stratégies ;
- distinguer les variantes débutant et avancées ;
- préparer la conformité avec le noyau commun `frame / strategy / execution / analytics` ;
- préparer l’intégration dans le moteur utilisé aussi comme bot FVG.

## Documents

- `GO_01_STRATEGY_NAME_NEWBIE_V1.md`
- `GO_XX_STRATEGY_NAME_PRO_V2.md`

## Règles de conformité minimales

Avant implémentation, chaque stratégie doit préciser :
- `strategy_id`
- `variant_id`
- instrument cible
- session / timezone
- déclencheur d’entrée
- invalidation
- stop
- take profit / gestion
- filtres
- cas interdits
- événements et métriques à journaliser

## Alignement canonique

Cette zone complète le cadrage canonique déjà posé dans :
- `docs/ot/trading/00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md`

## Point de reprise

- partir d’abord du document de stratégie ;
- valider ensuite la conformité moteur ;
- seulement après, ouvrir l’implémentation effective.
