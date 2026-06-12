# TRADING LAB V1 — SKELETON 01

Date (America/Montreal) : 2026-04-03

## 1. RÔLE

Ce document clôt l’ouverture du **squelette LAB V1**.

Le but de cette passe n’est pas encore de backtester réellement.
Le but est de poser une base standard minimale, raccordée au cadrage, à la spec opératoire et aux schémas machine-lisibles.

## 2. MODULE OUVERT

Module créé :
- `modules/trading_lab_v1/`

## 3. STRUCTURE POSÉE

### Docs
- `modules/trading_lab_v1/docs/README.md`
- `modules/trading_lab_v1/docs/ETABLI.txt`
- `modules/trading_lab_v1/docs/RUNBOOK.txt`

### Scripts standards
- `modules/trading_lab_v1/scripts/cmd.sh`
- `modules/trading_lab_v1/scripts/menu.sh`
- `modules/trading_lab_v1/scripts/sanity.sh`
- `modules/trading_lab_v1/scripts/install_shortcuts.sh`

### App minimale
- `modules/trading_lab_v1/app/trading_lab_v1.py`

## 4. CAPACITÉS ACTUELLES DU SQUELETTE

Le module sait déjà :
- afficher son état ;
- pointer vers le profil YAML V1 ;
- pointer vers les schémas JSON V1 ;
- émettre un exemple `event` ;
- émettre un exemple `trade` ;
- matérialiser ces exemples dans `state/trading_lab_v1/`.

## 5. CE QUI N’EST PAS ENCORE FAIT

- aucun backtest réel ;
- aucun parsing métier complet des données de marché ;
- aucune boucle sessionnelle ;
- aucune comparaison statistique réelle ;
- aucun runner live.

## 6. DÉCISION

Le **squelette LAB V1** est considéré comme **posé** au niveau module standard minimal.

## 7. SUITE NATURELLE

Suite recommandée :
- ouvrir une première passe de runner LAB qui consomme les fenêtres `18:00` et `00:00` ;
- matérialiser une boucle simple de génération de journaux `event` / `trade` ;
- garder le périmètre strictement `XAUUSD`.

## 8. TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_LAB_V1_FIRST_RUNNER_PASS_01`

## RISKS

- À qualifier.
