# TRADING LAB V1 — SCHEMA MATERIALIZATION 01

Date (America/Montreal) : 2026-04-03

## 1. RÔLE

Ce document clôt la passe de **matérialisation des schémas V1** pour le chantier trading dual stack.

Il sert à rendre visible ce qui est désormais produit en fichiers machine-lisibles.

## 2. FICHIERS MATÉRIALISÉS

### Profil V1
- `docs/ot/trading/schemas/xauusd_dual_stack_v1.profile.yaml`

### Schéma d’événements V1
- `docs/ot/trading/schemas/trading_event_v1.schema.json`

### Schéma de trades V1
- `docs/ot/trading/schemas/trading_trade_v1.schema.json`

## 3. CE QUI EST MAINTENANT ÉTABLI

- un **profil YAML V1** existe pour le focus `XAUUSD` ;
- un **JSON Schema d’événements V1** existe ;
- un **JSON Schema de trades V1** existe ;
- la structure `frame / strategy / execution / analytics` est maintenant présente à la fois :
  - en cadrage humain (`00_...`),
  - en spec opératoire (`02_...`),
  - et en fichiers machine-lisibles (`schemas/`).

## 4. LIMITES ACTUELLES

- il ne s’agit pas encore d’un runner LAB ;
- aucune exécution réelle n’est ouverte ;
- les schémas ne prouvent pas encore une validation runtime ;
- les champs de friction réaliste sont prévus, mais pas encore testés en exécution.

## 5. DÉCISION

La phase **schema materialization** peut être considérée comme **faite au niveau documentation + structures machine-lisibles**.

## 6. SUITE NATURELLE

Suite recommandée :
- ouvrir le **squelette LAB V1** qui consomme :
  - le profil YAML,
  - le schéma d’événements,
  - le schéma de trades.

## 7. TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_LAB_V1_SKELETON_01`
