# GO_OT_TRADING_DUAL_STACK_V1_01 — REPRISE

Date (America/Montreal) : 2026-04-03

## 1. OBJET

Ce fichier sert de **point de reprise opératoire court** pour la suite du chantier trading dual stack.

Il ne remplace pas le cadrage ;
il permet de reprendre vite, proprement, et sans relire tout le document principal.

## 2. BASE CANONIQUE

Document source :
- `docs/ot/trading/00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md`

Index local :
- `docs/ot/trading/INDEX.md`

## 3. ÉTABLI

- architecture cible retenue : **Lab + Real-Time** ;
- un seul **noyau partagé** est exigé ;
- différence LAB vs REAL-TIME limitée à : data source, mode d’exécution, cadence, contraintes runtime ;
- progression retenue : **Observation → Validation → Autonomie ciblée** ;
- cadre V1 initial : **XAUUSD / Gold**, timezone `America/Montreal`, fenêtres `18:00` et `00:00` ;
- le système doit produire un **journal d’événements** avant un journal de trades.

## 4. À OUVRIR MAINTENANT

### Bloc 1 — schéma commun
Figer :
- `frame`
- `strategy`
- `execution`
- `analytics`

### Bloc 2 — config V1
Définir au minimum :
- sessions
- kill zones
- limites journalières
- risk
- cooldown
- règles de re-entry
- variantes activables

### Bloc 3 — schéma d’événements V1
Définir au minimum :
- `event_id`
- `strategy_id`
- `variant_id`
- `mode`
- `symbol`
- `session_name`
- `signal_ts`
- `filters_state`
- `decision_state`

### Bloc 4 — schéma trade/log V1
Définir au minimum :
- `entry`
- `sl`
- `tp_plan`
- `risk_pct`
- `rr_planned`
- `result`
- `r_realized`
- `mfe`
- `mae`
- `time_in_trade`

## 5. RÈGLES DE TRAVAIL

- ne pas ouvrir le full auto ;
- ne pas séparer artificiellement le risk engine entre lab et réel ;
- ne pas mélanger UI et logique de stratégie ;
- ne pas produire une spec sans point de comparaison lab/live ;
- ne pas sortir du focus V1 Gold/session sans décision explicite.

## 6. PREMIÈRE SUITE NATURELLE

Suite recommandée :
**figer la spec config + event schema V1 avant toute implémentation.**

## 7. TRIGGER

`GO_OT_TRADING_DUAL_STACK_V1_01`

## 8. FORMULE DE REPRISE COURTE

Reprendre depuis `docs/ot/trading/00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md` et `docs/ot/trading/01_GO_OT_TRADING_DUAL_STACK_V1_01_REPRISE.md`, puis ouvrir la spec V1 du noyau commun (frame / strategy / execution / analytics) pour XAUUSD session `18:00` et `00:00` en timezone `America/Montreal`.
