# TRADING LAB V1 — FIRST RUNNER PASS 01

Date (America/Montreal) : 2026-04-03

## 1. RÔLE

Ce document clôt la **première passe utile du runner LAB V1**.

Cette passe ne lance pas encore un backtest métier complet.
Elle rend cependant le module capable de produire de **vrais journaux JSONL simples** à partir du profil V1.

## 2. MODIFICATIONS APPORTÉES

### Runner Python enrichi
- `modules/trading_lab_v1/app/trading_lab_v1.py`

### Wrapper CLI enrichi
- `modules/trading_lab_v1/scripts/cmd.sh`

## 3. CAPACITÉS AJOUTÉES

Le runner sait maintenant :
- lire le profil YAML V1 de façon minimale ;
- lister les sessions actives du profil ;
- exécuter un `run-once` ;
- écrire un `event` dans `state/trading_lab_v1/events_v1.jsonl` ;
- écrire un `trade` dans `state/trading_lab_v1/trades_v1.jsonl` si la session est active au moment du run ;
- afficher un `journal-status` simple.

## 4. DÉCISION DE DESIGN

Cette passe reste volontairement **sobre** :
- pas de dépendance externe YAML ;
- parsing minimal adapté au profil V1 actuel ;
- pas de logique de marché réelle ;
- pas de boucle sessionnelle continue.

## 5. CE QUI EST MAINTENANT PROUVABLE PAR LE MODULE

- le module peut consommer les artefacts V1 ;
- le module peut générer des journaux JSONL cohérents ;
- le module peut distinguer un cas `session active` d’un cas `blocked_by_frame` ;
- le module peut servir de base à une passe métier plus réaliste.

## 6. LIMITES RÉELLES

- le parsing YAML est minimal et lié au profil V1 actuel ;
- aucune donnée de marché réelle n’est encore consommée ;
- le `trade` produit reste virtuel ;
- la logique FVG/sweep n’est pas encore calculée à partir de chandelles réelles.

## 7. SUITE NATURELLE

Suite recommandée :
- ouvrir une passe métier qui remplace les features simulées par une vraie source de données LAB ;
- garder le focus strict `XAUUSD`, sessions `18:00` et `00:00`.

## 8. TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_LAB_V1_MARKET_INPUT_PASS_01`

## RISKS

- À qualifier.
