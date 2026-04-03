# TRADING LAB V1 — MARKET INPUT PASS 01

Date (America/Montreal) : 2026-04-03

## 1. RÔLE

Ce document clôt la première passe **input marché LAB**.

Le but de cette passe est de remplacer les features purement simulées par une **source de chandelles M1** lisible par le runner LAB.

## 2. MODIFICATIONS APPORTÉES

### Runner Python enrichi
- `modules/trading_lab_v1/app/trading_lab_v1.py`

### Wrapper CLI enrichi
- `modules/trading_lab_v1/scripts/cmd.sh`

### Donnée d’entrée exemple
- `modules/trading_lab_v1/data/sample_xauusd_m1.csv`

## 3. CAPACITÉS AJOUTÉES

Le module sait maintenant :
- charger un CSV M1 OHLCV ;
- sélectionner les lignes correspondant à une session du profil ;
- analyser la fenêtre d’ouverture de session ;
- détecter de manière simple :
  - séquence complète ou non,
  - sweep ou non,
  - FVG ou non,
  - direction contextuelle,
  - variante mécanique correspondante ;
- écrire un `event` dans `events_v1.jsonl` ;
- écrire un `trade` virtuel dans `trades_v1.jsonl` si la séquence est complète ;
- écrire une trace de run dans `market_runs_v1.jsonl`.

## 4. COMMANDE PRINCIPALE AJOUTÉE

Commande :
- `cmd-trading_lab_v1 analyze-market-input [csv_path] [session_id] [local_date]`

Exemple nominal :
- sans argument : utilise le CSV sample du module ;
- avec `session_id` : cible explicitement `gold_open_18h` ou `midnight_00h` ;
- avec `local_date` : cible une date précise présente dans le CSV.

## 5. DÉCISION DE DESIGN

Cette passe reste volontairement simple :
- source = CSV local ;
- granularité = M1 ;
- logique = open/session de base ;
- classification = mécanique ;
- exécution = virtuelle.

## 6. LIMITES RÉELLES

- le CSV sample n’est qu’une entrée de démonstration ;
- aucune connexion marché live n’est ouverte ;
- la détection FVG/sweep reste minimale ;
- aucun PnL réel ni backtest exhaustif n’est encore calculé.

## 7. DÉCISION

La passe **market input** est considérée comme **ouverte et matérialisée au niveau minimal utile**.

## 8. SUITE NATURELLE

Suite recommandée :
- ouvrir une passe “feature engine” plus métier ;
- brancher une source de données LAB plus réaliste ;
- garder le focus strict `XAUUSD`, sessions `18:00` et `00:00`.

## 9. TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_LAB_V1_FEATURE_ENGINE_PASS_01`
