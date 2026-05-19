# TRADING LAB V1 — BATCH REPORTING PASS 01

Date (America/Montreal) : 2026-04-03

## 1. RÔLE

Ce document clôt la première passe **batch reporting LAB**.

Le but de cette passe est de rendre les sorties batch plus lisibles sans devoir relire directement tous les JSONL bruts.

## 2. MODIFICATIONS APPORTÉES

### Runner Python enrichi
- `modules/trading_lab_v1/app/trading_lab_v1.py`

### Wrapper CLI enrichi
- `modules/trading_lab_v1/scripts/cmd.sh`

## 3. CAPACITÉS AJOUTÉES

Le module sait maintenant :
- agréger les sorties `features`, `trades`, `market_runs` et `batch_runs` ;
- produire un **rapport batch** lisible ;
- écrire ce rapport dans `state/trading_lab_v1/batch_reports_v1.jsonl` ;
- relire le dernier rapport produit.

## 4. COMMANDES AJOUTÉES

### Générer un rapport batch
- `cmd-trading_lab_v1 batch-report [session_id] [start_date] [end_date]`

### Voir le dernier rapport
- `cmd-trading_lab_v1 show-last-batch-report`

## 5. CONTENU DU RAPPORT

Le rapport batch agrège au minimum :
- `features_count`
- `trades_count`
- `market_runs_count`
- `batch_runs_count`
- `sequence_complete_count`
- `dates`
- distribution des `variants`
- distribution des `directions`
- `avg_open_range_points`
- `avg_open_body_points`
- `avg_first5_range_points`
- `avg_first5_body_delta`
- `avg_fvg_gap_points`
- `avg_rr_planned`
- distribution des `trade_results`

## 6. DÉCISION DE DESIGN

Cette passe reste volontairement simple :
- pas encore de dashboard ;
- pas encore de rendu tabulaire avancé ;
- pas encore de comparateur lab/live.

Mais elle fournit déjà une **lecture agrégée exploitable** du LAB.

## 7. LIMITES RÉELLES

- pas encore de métriques PnL avancées ;
- pas encore de drawdown agrégé ;
- pas encore de reporting multi-profils ;
- pas encore de reporting export CSV dédié.

## 8. SUITE NATURELLE

Suite recommandée :
- ouvrir une passe **summary export / reporting enrichi** ou une passe **comparateur lab/live** selon la priorité.

## 9. TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_LAB_V1_REPORT_EXPORT_PASS_01`
