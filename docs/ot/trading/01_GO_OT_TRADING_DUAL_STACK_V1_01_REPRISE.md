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

## 3. ÉTABLI

- architecture cible retenue : **Lab + Real-Time** ;
- un seul **noyau partagé** est exigé ;
- différence LAB vs REAL-TIME limitée à : data source, mode d’exécution, cadence, contraintes runtime ;
- progression retenue : **Observation → Validation → Autonomie ciblée** ;
- cadre V1 initial : **XAUUSD / Gold**, timezone `America/Montreal`, fenêtres `18:00` et `00:00` ;
- le système doit produire un **journal d’événements** avant un journal de trades ;
- la **core spec V1** du noyau commun est matérialisée.

## 4. CE QUI EST MAINTENANT COUVERT

### Bloc 1 — schéma commun
Couvert dans `02_TRADING_DUAL_STACK_CORE_SPEC_V1.md` :
- `frame`
- `strategy`
- `execution`
- `analytics`

### Bloc 2 — config V1
Couvert dans `02_TRADING_DUAL_STACK_CORE_SPEC_V1.md` :
- sessions
- discipline
- risk
- constraints
- variantes
- execution policies
- analytics minimum

### Bloc 3 — schéma d’événements V1
Couvert dans `02_TRADING_DUAL_STACK_CORE_SPEC_V1.md`.

### Bloc 4 — schéma trade/log V1
Couvert dans `02_TRADING_DUAL_STACK_CORE_SPEC_V1.md`.

## 5. À OUVRIR ENSUITE

### Suite recommandée immédiate
Matérialiser les schémas machine-lisibles et/ou le squelette LAB V1.

### Ordre recommandé
1. schémas machine-lisibles V1
2. squelette LAB V1
3. seulement ensuite runner REAL-TIME observation

## 6. RÈGLES DE TRAVAIL

- ne pas ouvrir le full auto ;
- ne pas séparer artificiellement le risk engine entre lab et réel ;
- ne pas mélanger UI et logique de stratégie ;
- ne pas produire une implémentation qui contourne la spec ;
- ne pas sortir du focus V1 Gold/session sans décision explicite.

## 7. TRIGGER

`GO_OT_TRADING_DUAL_STACK_V1_01`

## 8. TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_LAB_V1_SCHEMA_MATERIALIZATION_01`

## 9. FORMULE DE REPRISE COURTE

Reprendre depuis `docs/ot/trading/00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md`, `docs/ot/trading/01_GO_OT_TRADING_DUAL_STACK_V1_01_REPRISE.md` et `docs/ot/trading/02_TRADING_DUAL_STACK_CORE_SPEC_V1.md`, puis matérialiser les schémas machine-lisibles V1 avant d’ouvrir le squelette LAB.
