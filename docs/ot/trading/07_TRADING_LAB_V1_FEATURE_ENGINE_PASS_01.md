# TRADING LAB V1 — FEATURE ENGINE PASS 01

Date (America/Montreal) : 2026-04-03

## 1. RÔLE

Ce document clôt la première passe **feature engine LAB**.

Le but de cette passe est de séparer plus clairement :
- l’entrée marché ;
- l’extraction de features session/open ;
- la journalisation `event` / `trade`.

## 2. MODIFICATIONS APPORTÉES

### Runner Python enrichi
- `modules/trading_lab_v1/app/trading_lab_v1.py`

### Wrapper CLI enrichi
- `modules/trading_lab_v1/scripts/cmd.sh`

## 3. CAPACITÉS AJOUTÉES

Le module sait maintenant :
- construire un **payload de features** dédié à partir des chandelles M1 ;
- écrire ce payload dans `state/trading_lab_v1/features_v1.jsonl` ;
- exposer une commande dédiée `extract-features` ;
- réutiliser ces features pour construire les journaux `event` / `trade` ;
- enrichir `journal-status` avec le compteur des features.

## 4. FEATURES POSÉES DANS CETTE PASSE

Exemples de features matérialisées :
- `open_candle.range_points`
- `open_candle.body_points`
- `open_candle.direction`
- `first5_range_points`
- `first5_body_delta`
- `first5_direction`
- `sweep_above`
- `sweep_below`
- `sweep_detected`
- `fvg_detected`
- `fvg_direction`
- `fvg_gap_points`
- `variant_id`
- `entry`
- `sl`
- `rr_planned`

## 5. COMMANDE AJOUTÉE

Commande :
- `cmd-trading_lab_v1 extract-features [csv_path] [session_id] [local_date]`

La commande lit un CSV M1, isole la session ciblée, calcule les features, et renvoie le payload calculé.

## 6. DÉCISION DE DESIGN

La passe reste volontairement simple :
- pas encore de moteur d’exécution sophistiqué ;
- pas encore de feature store externe ;
- pas encore de multi-instrument.

Mais le LAB dispose maintenant d’une vraie couche **feature engine** distincte.

## 7. LIMITES RÉELLES

- features encore centrées sur une lecture session/open simple ;
- pas de calcul HTF enrichi ;
- pas de scoring probabiliste ;
- pas de backtest exhaustif multi-journées.

## 8. SUITE NATURELLE

Suite recommandée :
- ouvrir une passe **multi-run / batch** sur plusieurs jours ou plusieurs fichiers ;
- garder le focus strict `XAUUSD`.

## 9. TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_LAB_V1_BATCH_PASS_01`

## RISKS

- À qualifier.
