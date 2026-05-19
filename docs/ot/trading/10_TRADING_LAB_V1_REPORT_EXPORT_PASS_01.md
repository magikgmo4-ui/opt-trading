# TRADING LAB V1 — REPORT EXPORT PASS 01

Date (America/Montreal) : 2026-04-03

## 1. RÔLE

Ce document clôt la première passe **report export LAB**.

Le but de cette passe est de produire des sorties lisibles et transportables à partir des rapports batch déjà présents dans le LAB.

## 2. MODIFICATIONS APPORTÉES

### Exporter dédié
- `modules/trading_lab_v1/app/report_export_v1.py`

### Wrapper CLI enrichi
- `modules/trading_lab_v1/scripts/cmd.sh`

## 3. CAPACITÉS AJOUTÉES

Le module sait maintenant :
- relire le dernier rapport batch ;
- générer un nouveau rapport batch à la demande avant export ;
- exporter les rapports en **JSON** et en **Markdown** ;
- écrire ces exports dans `state/trading_lab_v1/exports/`.

## 4. COMMANDES AJOUTÉES

### Exporter le dernier rapport batch existant
- `cmd-trading_lab_v1 export-last-batch-report`

### Générer puis exporter un rapport batch filtré
- `cmd-trading_lab_v1 export-batch-report [session_id] [start_date] [end_date]`

### Voir l’état de l’exporter
- `cmd-trading_lab_v1 export-status`

## 5. SORTIES PRODUITES

Les exports produits sont :
- un fichier `.json`
- un fichier `.md`

Dossier de sortie :
- `state/trading_lab_v1/exports/`

## 6. DÉCISION DE DESIGN

Cette passe garde une séparation propre :
- le runner LAB produit les journaux et rapports ;
- l’exporter dédié produit les formats lisibles/transportables.

Cela évite de surcharger le runner principal avec des responsabilités de rendu.

## 7. LIMITES RÉELLES

- pas encore d’export CSV dédié ;
- pas encore de rendu tabulaire enrichi ;
- pas encore de PDF export ;
- pas encore de comparateur lab/live exporté.

## 8. SUITE NATURELLE

Suite recommandée :
- ouvrir une passe **lab/live comparator** ou une passe **export enrichi** selon la priorité.

## 9. TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_LAB_V1_COMPARATOR_PASS_01`
