# TRADING LAB V1 — BATCH PASS 01

Date (America/Montreal) : 2026-04-03

## 1. RÔLE

Ce document clôt la première passe **batch LAB**.

Le but de cette passe est de permettre plusieurs runs LAB successifs sur plusieurs dates disponibles dans un même CSV M1, tout en gardant le focus strict `XAUUSD`.

## 2. MODIFICATIONS APPORTÉES

### Runner Python enrichi
- `modules/trading_lab_v1/app/trading_lab_v1.py`

### Wrapper CLI enrichi
- `modules/trading_lab_v1/scripts/cmd.sh`

## 3. CAPACITÉS AJOUTÉES

Le module sait maintenant :
- lister les dates disponibles pour une session donnée ;
- exécuter plusieurs runs sur plusieurs dates ;
- produire un résumé batch ;
- écrire ce résumé dans `state/trading_lab_v1/batch_runs_v1.jsonl`.

## 4. COMMANDES AJOUTÉES

### Voir les dates disponibles
- `cmd-trading_lab_v1 show-batch-dates [csv_path] [session_id]`

### Lancer un batch
- `cmd-trading_lab_v1 batch-run [csv_path] [session_id] [start_date] [end_date]`

## 5. SORTIES BATCH

Le batch résume au minimum :
- les dates traitées ;
- le nombre de runs ;
- le nombre de séquences complètes ;
- le nombre de trades virtuels générés ;
- la distribution des variantes mécaniques observées.

## 6. DÉCISION DE DESIGN

Cette passe reste volontairement simple :
- batch sur un seul profil V1 ;
- batch sur un seul instrument ;
- batch sans moteur d’agrégation statistique avancé.

Mais elle pose la couche minimale pour enchaîner sur des runs multi-jours de façon propre.

## 7. LIMITES RÉELLES

- pas encore de rapport statistique approfondi ;
- pas encore de multi-fichiers dans une seule commande ;
- pas encore de métriques PnL agrégées ;
- pas encore de comparateur lab/live.

## 8. SUITE NATURELLE

Suite recommandée :
- ouvrir une passe **batch reporting / stats** pour agréger les sorties LAB ;
- garder le focus strict `XAUUSD`.

## 9. TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_LAB_V1_BATCH_REPORTING_PASS_01`
