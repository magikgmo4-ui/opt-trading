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

Spec V1 du noyau commun :
- `docs/ot/trading/02_TRADING_DUAL_STACK_CORE_SPEC_V1.md`

Schémas machine-lisibles :
- `docs/ot/trading/schemas/xauusd_dual_stack_v1.profile.yaml`
- `docs/ot/trading/schemas/trading_event_v1.schema.json`
- `docs/ot/trading/schemas/trading_trade_v1.schema.json`

## 3. ÉTABLI

- architecture cible retenue : **Lab + Real-Time** ;
- un seul **noyau partagé** est exigé ;
- différence LAB vs REAL-TIME limitée à : data source, mode d’exécution, cadence, contraintes runtime ;
- progression retenue : **Observation → Validation → Autonomie ciblée** ;
- cadre V1 initial : **XAUUSD / Gold**, timezone `America/Montreal`, fenêtres `18:00` et `00:00` ;
- le système doit produire un **journal d’événements** avant un journal de trades ;
- la **core spec V1** du noyau commun est matérialisée ;
- les **schémas machine-lisibles V1** sont matérialisés.

## 4. CE QUI EST MAINTENANT COUVERT

### Bloc 1 — schéma commun
Couvert dans `02_TRADING_DUAL_STACK_CORE_SPEC_V1.md`.

### Bloc 2 — config V1
Couvert dans `02_TRADING_DUAL_STACK_CORE_SPEC_V1.md` et matérialisé dans `schemas/xauusd_dual_stack_v1.profile.yaml`.

### Bloc 3 — schéma d’événements V1
Couvert dans `02_TRADING_DUAL_STACK_CORE_SPEC_V1.md` et matérialisé dans `schemas/trading_event_v1.schema.json`.

### Bloc 4 — schéma trade/log V1
Couvert dans `02_TRADING_DUAL_STACK_CORE_SPEC_V1.md` et matérialisé dans `schemas/trading_trade_v1.schema.json`.

## 5. À OUVRIR ENSUITE

### Suite recommandée immédiate
Ouvrir le **squelette LAB V1** qui consomme le profil YAML et les schémas JSON.

### Ordre recommandé
1. squelette LAB V1
2. validation structurelle des journaux
3. seulement ensuite runner REAL-TIME observation

## 6. RÈGLES DE TRAVAIL

- ne pas ouvrir le full auto ;
- ne pas séparer artificiellement le risk engine entre lab et réel ;
- ne pas mélanger UI et logique de stratégie ;
- ne pas produire une implémentation qui contourne la spec ;
- ne pas sortir du focus V1 Gold/session sans décision explicite.

## 7. TRIGGER SOURCE

`GO_OT_TRADING_DUAL_STACK_V1_01`

## 8. TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_LAB_V1_SKELETON_01`

## 9. FORMULE DE REPRISE COURTE

Reprendre depuis `docs/ot/trading/00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md`, `docs/ot/trading/02_TRADING_DUAL_STACK_CORE_SPEC_V1.md` et les fichiers `schemas/`, puis ouvrir le squelette LAB V1 avant toute implémentation REAL-TIME.
