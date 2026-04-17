# TRADING_DUAL_STACK_V1_0_CLARIFIED

## STATUS
PROPOSED_CANONICAL_V1_0

## PURPOSE
Définir une architecture canonique à deux niveaux pour les stratégies de trading disciplinées :

- un niveau LAB pour backtest / simulation / comparaison
- un niveau REALTIME pour observation / validation / exécution
- un cadre trader humain partagé
- des logs comparables
- une progression propre de la recherche vers l’application réelle

## DESIGN DECISION
La V1.0 clarifiée retient :
- une architecture duale LAB + REALTIME
- un noyau commun
- des contrats explicites minimums
- un réalisme minimal du LAB
- des guards live obligatoires
- une promotion par gates

La V1.0 rejette :
- la complexification prématurée
- le full auto large immédiat
- l’ouverture trop tôt de V1.1
- la dérive d’implémentation sans contrats

---

## 1. CANONICAL PRINCIPLES

### 1.1 DUAL STACK
Le système est structuré en deux niveaux distincts :
- LAB
- REALTIME

### 1.2 SHARED CORE
Le LAB et le REALTIME partagent le même noyau logique :
- même cadre trader
- même stratégie
- mêmes journaux
- mêmes identifiants de variantes

### 1.3 HUMAN TRADER FRAME
Le système doit pouvoir exprimer un cadre proche d’un trader humain discipliné :
- horaires
- sessions
- kill zones
- boring trader
- max trades par session
- max trades par jour
- risk management
- stop après pertes
- interdictions disciplinaires

### 1.4 PROMOTION BY GATES
Le passage du LAB au REALTIME ne doit jamais être implicite.
Toute promotion doit passer par des états de qualification définis.

### 1.5 COMPARABLE LOGGING
Le LAB et le REALTIME doivent produire des journaux compatibles pour :
- audit
- comparaison
- analyse des écarts
- qualification continue

---

## 2. SCOPE OF V1.0

### INCLUDED IN V1.0
- séparation LAB / REALTIME
- noyau commun
- cadre trader commun
- contrats explicites minimum
- réalisme minimal du LAB
- guards live minimum
- modes observe / confirm / auto
- promotion gates minimum

### EXCLUDED FROM V1.0
- setup quality score avancé
- explainability opérateur enrichie
- realism tiers multiples
- ranking multi-critères avancé
- contexte marché enrichi
- orchestration multi-stratégies complexe

---

## 3. CONTRACTS

### 3.1 MARKET DATA CONTRACT
Le système doit figer au minimum :
- timezone canonique
- granularités autorisées
- sources de données autorisées
- politique de bougie incomplète
- politique de replay historique
- gestion minimale des trous de données

### 3.2 TRADER FRAME CONTRACT
Le frame trader décrit la discipline commune :
- timezone
- sessions
- kill zones
- limites journalières
- limites par session
- règles de risque
- règles disciplinaires
- cooldowns éventuels

### 3.3 STRATEGY CONTRACT
La stratégie décrit :
- setup
- conditions d’activation
- direction
- entrée
- invalidation
- stop
- TP
- BE
- conditions de sortie

### 3.4 EXECUTION MODE CONTRACT
Le REALTIME doit supporter :
- observe
- confirm
- auto

### 3.5 LOGGING AND EVENT CONTRACT
Le système doit produire :
- event logs
- trade logs
- summaries comparables

### 3.6 PROMOTION / QUALIFICATION CONTRACT
Le système doit pouvoir affecter un état de qualification à chaque stratégie / variante.

---

## 4. LAB LAYER

### 4.1 PURPOSE
Le LAB sert à :
- backtester
- simuler
- comparer
- classer
- qualifier

### 4.2 MANDATORY BEHAVIOR
Le LAB doit :
- respecter le Trader Frame
- rejouer les données historiques
- appliquer la stratégie
- simuler les résultats
- journaliser chaque événement utile
- produire des métriques comparables

### 4.3 MINIMAL REALISM IN V1.0
Le LAB ne doit pas être purement idéal.
V1.0 impose au minimum :
- spread pris en compte
- slippage minimal simulé
- politique claire d’exécution/replay
- hypothèses explicites sur les fills

---

## 5. REALTIME LAYER

### 5.1 PURPOSE
Le REALTIME sert à :
- observer
- détecter
- proposer
- exécuter
- journaliser la réalité live

### 5.2 MODES

#### OBSERVE
- détection
- log
- aucune exécution

#### CONFIRM
- détection
- proposition
- validation humaine
- exécution si validé

#### AUTO
- détection
- exécution autonome
- réservé aux variantes qualifiées

---

## 6. HUMAN TRADER FRAME

Le système doit pouvoir exprimer un cadre du type :
- timezone = America/Montreal
- sessions autorisées
- kill zones autorisées
- max_trades_per_session
- max_trades_per_day
- stop_day_after_x_losses
- risk_per_trade
- rr_min
- no_trade_outside_session
- no_immediate_reentry_same_setup

Ce cadre doit être partagé entre LAB et REALTIME.

---

## 7. LIVE OPERATIONAL GUARDS

V1.0 impose des garde-fous minimums pour le REALTIME :
- max_daily_loss
- max_consecutive_losses
- spread_guard
- data_gap_guard
- kill_switch
- fallback_mode

Aucune exécution autonome ne doit être considérée propre sans ces protections.

---

## 8. PROMOTION GATES

Le système doit permettre au minimum les états suivants :
- research
- shadow_observe
- confirm_ready
- auto_limited
- auto_approved

La promotion ne doit jamais dépendre d’un jugement implicite non tracé.

---

## 9. LOGGING REQUIREMENTS

### 9.1 EVENT LOG
Événements minimaux recommandés :
- session_open
- session_closed
- setup_detected
- setup_rejected
- entry_triggered
- trade_opened
- be_moved
- tp_hit
- sl_hit
- trade_closed
- day_stopped

### 9.2 TRADE LOG
Chaque trade doit pouvoir contenir au minimum :
- strategy_id
- variant_id
- mode
- session_name
- timestamp_open
- timestamp_close
- direction
- entry
- sl
- tp
- risk_pct
- rr_planned
- result
- r_realized
- mae
- mfe
- reason_entry
- reason_exit

---

## 10. CANONICAL ARBITRATION RESULT

La V1 initiale a été conservée sur le fond.
La clarification a ajouté les éléments nécessaires pour éviter une implémentation trop philosophique ou trop floue.

Le résultat retenu est :
- même vision générale
- meilleure séparation des responsabilités
- guards et gates rendus explicites
- V1.0 et V1.1 séparées proprement

---

## 11. V1.1 CANDIDATE TOPICS
Sujets retenus plus tard :
- setup quality score
- operator explainability
- realism profiles (optimistic / realistic / stressed)
- ranking multi-critères
- contexte marché enrichi

---

## 12. CANONICAL RESUMPTION POINT
Après validation documentaire V1.0 :
- détailler les contrats
- choisir le premier périmètre concret
- cadrer le premier couple LAB / REALTIME sur Gold / Session / FVG

END_OF_DOCUMENT
